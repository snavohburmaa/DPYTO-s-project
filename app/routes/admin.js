const router = require('express').Router();
const db = require('../lib/db');
const S = require('../lib/services');
const { requireRole } = require('../lib/auth');

router.use(requireRole('admin'));
const byNewest = (a, b) => new Date(b.createdAt) - new Date(a.createdAt);

function reportRows(filter = () => true) {
  return db.find('reports', filter).map(r => {
    let target = null, label = '';
    if (r.targetType === 'listing') { target = db.get('properties', r.targetId); label = target ? target.title : 'Deleted listing'; }
    else if (r.targetType === 'user') { target = db.get('users', r.targetId); label = target ? target.name : 'Deleted user'; }
    else if (r.targetType === 'review') { target = db.get('reviews', r.targetId); label = target ? `Review #${target.id}` : 'Deleted review'; }
    return { ...r, reporter: db.get('users', r.reporterId), target, label };
  }).sort(byNewest);
}

router.get('/', (req, res) => {
  const users = db.all('users'), props = db.all('properties'), bookings = db.all('bookings'), reports = db.all('reports');
  const week = Date.now() - 7 * 86400000;
  const stats = {
    users: users.length, newUsers: users.filter(u => new Date(u.createdAt).getTime() > week).length,
    listings: props.length, published: props.filter(p => p.listingStatus === 'published').length,
    bookings: bookings.length, confirmed: bookings.filter(b => b.status === 'Confirmed').length,
    openReports: reports.filter(r => r.status === 'Open').length,
  };
  res.render('admin/dashboard', { title: 'Admin Dashboard', stats, reports: reportRows(r => r.status === 'Open').slice(0, 5), users: [...users].sort(byNewest).slice(0, 5) });
});

router.get('/users', (req, res) => {
  const tab = req.query.tab || 'all';
  let rows = [...db.all('users')].sort(byNewest);
  if (['renter', 'owner', 'admin'].includes(tab)) rows = rows.filter(u => u.role === tab);
  if (tab === 'suspended') rows = rows.filter(u => u.status === 'suspended');
  const q = (req.query.q || '').toLowerCase();
  if (q) rows = rows.filter(u => (u.name + ' ' + u.email).toLowerCase().includes(q));
  res.render('admin/users', { title: 'Users', rows, tab, q });
});
router.post('/users/:id/toggle', (req, res) => {
  const u = db.get('users', req.params.id);
  if (!u || u.id === req.user.id) { req.flash('error', 'You cannot change your own account here.'); return res.redirect('/admin/users'); }
  db.update('users', u.id, { status: u.status === 'suspended' ? 'active' : 'suspended' });
  req.flash('ok', `${u.name} is now ${u.status === 'suspended' ? 'active' : 'suspended'}.`);
  res.redirect(req.get('Referer') || '/admin/users');
});

router.get('/listings', (req, res) => {
  const tab = req.query.tab || 'all';
  let rows = db.all('properties').map(S.propertyWithMeta).sort(byNewest);
  if (['published', 'draft', 'disabled'].includes(tab)) rows = rows.filter(p => p.listingStatus === tab);
  res.render('admin/listings', { title: 'Listings', rows, tab });
});
router.post('/listings/:id/toggle', (req, res) => {
  const p = db.get('properties', req.params.id);
  if (!p) return res.redirect('/admin/listings');
  const next = p.listingStatus === 'disabled' ? 'published' : 'disabled';
  db.update('properties', p.id, { listingStatus: next });
  S.notify(p.ownerId, next === 'disabled' ? 'Listing disabled' : 'Listing enabled', `${p.title} was ${next === 'disabled' ? 'disabled' : 'enabled'} by an admin.`, '/owner/listings');
  req.flash('ok', `${p.title} is now ${next}.`);
  res.redirect(req.get('Referer') || '/admin/listings');
});

router.get('/reviews', (req, res) => {
  const rows = db.all('reviews').map(r => ({ ...r, renter: db.get('users', r.renterId), property: db.get('properties', r.propertyId) })).sort(byNewest);
  res.render('admin/reviews', { title: 'Reviews', rows });
});
router.post('/reviews/:id/toggle', (req, res) => {
  const r = db.get('reviews', req.params.id);
  if (r) db.update('reviews', r.id, { hidden: !r.hidden });
  req.flash('ok', r && !r.hidden ? 'Review hidden.' : 'Review visible again.');
  res.redirect(req.get('Referer') || '/admin/reviews');
});

router.get('/reports', (req, res) => {
  const tab = req.query.tab || 'Open';
  const rows = reportRows(r => tab === 'all' || r.status === tab);
  res.render('admin/reports', { title: 'Reports', rows, tab });
});
router.post('/reports/:id/status', (req, res) => {
  const r = db.get('reports', req.params.id);
  if (r && ['Open', 'Reviewed', 'Actioned'].includes(req.body.status)) db.update('reports', r.id, { status: req.body.status, adminNote: (req.body.note || '').trim() });
  req.flash('ok', 'Report updated.');
  res.redirect(req.get('Referer') || '/admin/reports');
});

router.get('/bookings', (req, res) => {
  const rows = db.all('bookings').map(b => S.withRefs(b)).sort(byNewest);
  res.render('admin/bookings', { title: 'Bookings', rows });
});

module.exports = router;
