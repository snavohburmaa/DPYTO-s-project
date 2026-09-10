// Formatting helpers shared by routes and views.
const AV_COLORS = ['#F6D6C8', '#CFE3F7', '#D8F0DC', '#F5E4B8', '#E3D6F5', '#F7D0DE'];

function initials(name = '') {
  return name.split(' ').filter(Boolean).slice(0, 2).map(w => w[0].toUpperCase()).join('');
}
function avatarColor(id = 0) { return AV_COLORS[id % AV_COLORS.length]; }

function money(n) { return '฿' + Number(n || 0).toLocaleString('en-US'); }

function fmtDate(iso, opts) {
  if (!iso) return '';
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString('en-GB', opts || { day: 'numeric', month: 'short', year: 'numeric' });
}
function fmtDateTime(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  return d.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' })
    + ', ' + d.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
}
function fmtTime(iso) {
  return new Date(iso).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
}
function ago(iso) {
  const s = Math.floor((Date.now() - new Date(iso).getTime()) / 1000);
  if (s < 60) return 'just now';
  if (s < 3600) return `${Math.floor(s / 60)} min ago`;
  if (s < 86400) return `${Math.floor(s / 3600)} h ago`;
  if (s < 86400 * 7) return `${Math.floor(s / 86400)} d ago`;
  return fmtDate(iso);
}

// Status colour classes used by badge partials.
const STATUS_KIND = {
  Available: 'ok', Reserved: 'warn', Rented: 'bad', Unavailable: 'neutral',
  Pending: 'warn', Confirmed: 'ok', Completed: 'info', Rejected: 'bad', Cancelled: 'bad',
  Requested: 'warn', Suggested: 'info', Declined: 'bad', Approved: 'ok',
  published: 'ok', draft: 'neutral', disabled: 'bad',
  Open: 'warn', Reviewed: 'info', Actioned: 'ok', active: 'ok', suspended: 'bad',
};
function kind(status) { return STATUS_KIND[status] || 'neutral'; }

const FACILITIES = [
  { key: 'wifi', label: 'Wi-Fi' }, { key: 'aircon', label: 'Air Conditioner' },
  { key: 'furnished', label: 'Furnished' }, { key: 'parking', label: 'Parking' },
  { key: 'elevator', label: 'Elevator' }, { key: 'security', label: 'Security' },
  { key: 'pets', label: 'Pet Friendly' }, { key: 'gym', label: 'Gym' }, { key: 'pool', label: 'Pool' },
];
const ROOM_TYPES = ['Apartment', 'Condo', 'House', 'Room'];
const ROOM_STATUSES = ['Available', 'Reserved', 'Rented', 'Unavailable'];

const { ic } = require('./icons');
function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }
function avatar(user, size = 40) {
  if (!user) return `<span class="avatar" style="width:${size}px;height:${size}px;background:#E6E8EF"></span>`;
  return `<span class="avatar" style="width:${size}px;height:${size}px;background:${avatarColor(user.id)};font-size:${Math.round(size * 0.36)}px">${esc(initials(user.name))}</span>`;
}
function stars(n) { n = Math.round(n || 0); return '\u2605'.repeat(n) + '\u2606'.repeat(5 - n); }
function facilityLabel(key) { const f = FACILITIES.find(f => f.key === key); return f ? f.label : key; }
function dateInput(iso) { return iso ? new Date(iso).toISOString().slice(0, 10) : ''; }
function timeInput(iso) { if (!iso) return ''; const d = new Date(iso); return String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0'); }

module.exports = { ic, esc, avatar, stars, facilityLabel, dateInput, timeInput, initials, avatarColor, money, fmtDate, fmtDateTime, fmtTime, ago, kind, FACILITIES, ROOM_TYPES, ROOM_STATUSES };
