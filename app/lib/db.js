// Tiny JSON file database. One file per table in /data.
// Every table is an array of objects with a numeric `id`.
// Reads are cached in memory, writes go straight to disk.
const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', 'data');
const TABLES = ['users', 'properties', 'favorites', 'viewings', 'bookings', 'reviews',
  'conversations', 'messages', 'reports', 'notifications'];

const cache = {};

function file(table) { return path.join(DATA_DIR, `${table}.json`); }

function load(table) {
  if (!TABLES.includes(table)) throw new Error(`Unknown table: ${table}`);
  if (!cache[table]) {
    if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
    if (!fs.existsSync(file(table))) fs.writeFileSync(file(table), '[]');
    cache[table] = JSON.parse(fs.readFileSync(file(table), 'utf8'));
  }
  return cache[table];
}

function save(table) {
  fs.writeFileSync(file(table), JSON.stringify(cache[table], null, 2));
}

function nextId(rows) {
  return rows.reduce((m, r) => Math.max(m, r.id || 0), 0) + 1;
}

const db = {
  all(table) { return load(table); },
  find(table, fn) { return load(table).filter(fn); },
  findOne(table, fn) { return load(table).find(fn) || null; },
  get(table, id) { return load(table).find(r => r.id === Number(id)) || null; },
  insert(table, row) {
    const rows = load(table);
    const record = { id: nextId(rows), createdAt: new Date().toISOString(), ...row };
    rows.push(record);
    save(table);
    return record;
  },
  update(table, id, patch) {
    const rows = load(table);
    const i = rows.findIndex(r => r.id === Number(id));
    if (i === -1) return null;
    rows[i] = { ...rows[i], ...patch, updatedAt: new Date().toISOString() };
    save(table);
    return rows[i];
  },
  remove(table, id) {
    const rows = load(table);
    const i = rows.findIndex(r => r.id === Number(id));
    if (i === -1) return false;
    rows.splice(i, 1);
    save(table);
    return true;
  },
  reset(table, rows) { cache[table] = rows; save(table); },
  TABLES,
};

module.exports = db;
