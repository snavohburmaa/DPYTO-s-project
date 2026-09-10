const router = require('express').Router();
const path = require('path');
const fs = require('fs');
const multer = require('multer');
const db = require('../lib/db');
const S = require('../lib/services');
const H = require('../lib/helpers');
const { requireRole } = require('../lib/auth');

router.use(requireRole('owner'));

// Photo uploads go to /public/uploads. Only images, 5 MB each.
const uploadDir = path.join(__dirname, '..', 'public', 'uploads');
fs.mkdirSync(uploadDir, { recursive: true });
const upload = multer({
  storage: multer.diskStorage({ destination: uploadDir, filename: (req, f, cb) => cb(null, Date.now() + '-' + Math.round(Math.random() * 1e6) + path.extname(f.originalname).toLowerCase()) }),
  limits: { fileSize: 5 * 1024 * 1024 },
  fileFilter: (req, f, cb) => cb(null, /^image\//.test(f.mimetype)),
});

// Only the owner of a listing may touch it.
function ownListing(req, res, next) {
  const p = db.get('properties', req.params.id);
  if (!p || p.ownerId !== req.user.id) return res.status(403).render('error', { title: 'Access denied', message: 'You can only manage your own listings.', code: 403 });
  req.property = p; next();
}
function ownBooking(req, res, next) {
  const b = db.get('bookings', req.params.id);
  if (!b || b.ownerId !== req.user.id) return res.status(403).render('error', { title: 'Access denied', message: 'This booking belongs to another owner.', code: 403 });
  req.booking = b; next();
}
function ownViewing(req, res, next) {
  const v = db.get('viewings', req.params.id);
  if (!v || v.ownerId !== req.user.id) return res.status(403).render('error', { title: 'Access denied', message: 'This viewing belongs to another owner.', code: 403 });
  req.viewing = v; next();
}
const byNewest = (a, b) => new Date(b.createdAt) - new Date(a.createdAt);

router.get('/', (req, res) => {
  const stats = S.ownerStats(req.user.id);
  const recent = [
    ...db.find('bookings', b => b.ownerId === req.user.id && b.status === 'Pending').map(b => ({ kind: 'booking', ...S.withRefs(b) })),
    ...db.find('viewings', v => v.ownerId === req.user.id && v.status === 'Requested').map(v => ({ kind: 'viewing', ...S.withRefs(v) })),
  ].sort(byNewest).slice(0, 5);
  res.render('owner/dashboard', { title: 'Dashboard', stats, recent });
});

router.get('/listings', (req, res) => {
  const tab = req.query.tab || 'all';
  let rows = db.find('properties', p => p.ownerId === req.user.id).map(S.propertyWithMeta).sort(byNewest);
  const counts = { all: rows.length, published: rows.filter(p => p.listingStatus === 'published').length, draft: rows.filter(p => p.listingStatus === 'draft').length, disabled: rows.filter(p => p.listingStatus === 'disabled').length };
  if (tab !== 'all') rows = rows.filter(p => p.listingStatus === tab);
  res.render('owner/listings', { title: 'My Listings', rows, tab, counts });
});
router.get('/listings/new', (req, res) => res.render('owner/listing-form', { title: 'Add New Property', p: { facilities: [], photos: [], status: 'Available', type: 'Condo', bedrooms: 1, bathrooms: 1 }, facilities: H.FACILITIES, types: H.ROOM_TYPES, statuses: H.ROOM_STATUSES }));
router.get('/listings/:id/edit', ownListing, (req, res) => res.render('owner/listing-form', { title: 'Edit Property', p: req.property, facilities: H.FACILITIES, types: H.ROOM_TYPES, statuses: H.ROOM_STATUSES }));

function listingFromBody(body, files, existing = {}) {
  const errors = [];
  const p = {
    title: (body.title || '').trim(), type: H.ROOM_TYPES.includes(body.type) ? body.type : 'Condo',
    location: (body.location || '').trim(), address: (body.address || '').trim(),
    monthlyRent: Number(String(body.monthlyRent || '').replace(/[^\d.]/g, '')),
    bedrooms: Number(body.bedrooms) || 1, bathrooms: Number(body.bathrooms) || 1, sizeSqm: Number(body.sizeSqm) || 0,
    facilities: [].concat(body.facilities || []).filter(Boolean),
    description: (body.description || '').trim(), availableFrom: body.availableFrom || '',
    status: H.ROOM_STATUSES.includes(body.status) ? body.status : 'Available',
    listingStatus: body.action === 'draft' ? 'draft' : 'published',
    photos: [].concat(body.keepPhotos || []).filter(Boolean),
  };
  (files || []).forEach(f => p.photos.push('/uploads/' + f.filename));
  if (body.photoUrl && body.photoUrl.trim()) p.photos.push(body.photoUrl.trim());
  if (p.title.length < 3) errors.push('Give the property a title.');
  if (!p.location) errors.push('Enter the location.');
  if (!p.monthlyRent) errors.push('Enter the monthly rent.');
  if (!p.description) errors.push('Write a short description.');
  if (p.listingStatus === 'published' && !p.photos.length) errors.push('Add at least one photo before publishing. Save as draft if you do not have one yet.');
  return { p: { ...existing, ...p }, errors };
}
router.post('/listings', upload.array('photos', 8), (req, res) => {
  const { p, errors } = listingFromBody(req.body, req.files);
  if (errors.length) return res.render('owner/listing-form', { title: 'Add New Property', p, facilities: H.FACILITIES, types: H.ROOM_TYPES, statuses: H.ROOM_STATUSES, flash: { error: errors, ok: [] } });
  const saved = db.insert('properties', { ...p, ownerId: req.user.id, views: 0 });
  req.flash('ok', p.listingStatus === 'draft' ? 'Draft saved.' : 'Listing published.');
  res.redirect('/owner/listings');
});
router.post('/listings/:id', ownListing, upload.array('photos', 8), (req, res) => {
  const { p, errors } = listingFromBody(req.body, req.files, req.property);
  if (errors.length) return res.render('owner/listing-form', { title: 'Edit Property', p, facilities: H.FACILITIES, types: H.ROOM_TYPES, statuses: H.ROOM_STATUSES, flash: { error: errors, ok: [] } });
  if (req.property.listingStatus === 'disabled') p.listingStatus = 'disabled';
  db.update('properties', req.property.id, p);
  req.flash('ok', 'Listing saved.');
  res.redirect('/owner/listings');
});
router.post('/listings/:id/status', ownListing, (req, res) => {
  if (H.ROOM_STATUSES.includes(req.body.status)) db.update('properties', req.property.id, { status: req.body.status });
  if (['published', 'draft'].includes(req.body.listingStatus) && req.property.listingStatus !== 'disabled') db.update('properties', req.property.id, { listingStatus: req.body.listingStatus });
  req.flash('ok', 'Status updated.');
  res.redirect(req.get('Referer') || '/owner/listings');
});
router.post('/listings/:id/delete', ownListing, (req, res) => {
  const active = db.findOne('bookings', b => b.propertyId === req.property.id && ['Pending', 'Confirmed'].includes(b.status));
  if (active) { req.flash('error', 'This room has an active booking. Finish or cancel it before deleting.'); return res.redirect('/owner/listings'); }
  db.remove('properties', req.property.id);
  db.find('favorites', f => f.propertyId === req.property.id).forEach(f => db.remove('favorites', f.id));
  req.flash('ok', 'Listing deleted.');
  res.redirect('/owner/listings');
});

// ---- viewings
router.get('/viewings', (req, res) => {
  const tab = req.query.tab || 'all';
  let rows = db.find('viewings', v => v.ownerId === req.user.id).map(v => S.withRefs(v)).sort(byNewest);
  const counts = { all: rows.length, new: rows.filter(v => v.status === 'Requested').length, upcoming: rows.filter(v => v.status === 'Confirmed').length, done: rows.filter(v => ['Completed', 'Declined', 'Cancelled'].includes(v.status)).length };
  if (tab === 'new') rows = rows.filter(v => v.status === 'Requested');
  if (tab === 'upcoming') rows = rows.filter(v => ['Confirmed', 'Suggested'].includes(v.status));
  if (tab === 'done') rows = rows.filter(v => ['Completed', 'Declined', 'Cancelled'].includes(v.status));
  res.render('owner/viewings', { title: 'Viewing Requests', rows, tab, counts });
});
router.post('/viewings/:id/:action', ownViewing, (req, res) => {
  const a = req.params.action;
  const payload = { reason: (req.body.reason || '').trim() };
  if (a === 'suggest') {
    if (!req.body.date || !req.body.time) { req.flash('error', 'Pick the date and time you want to suggest.'); return res.redirect('/owner/viewings'); }
    payload.suggestedAt = new Date(`${req.body.date}T${req.body.time}:00`).toISOString();
  }
  if (a === 'decline' && !payload.reason) { req.flash('error', 'Give the renter a reason for declining.'); return res.redirect('/owner/viewings'); }
  if (!['approve', 'suggest', 'decline', 'complete'].includes(a)) return res.redirect('/owner/viewings');
  S.ownerRespondViewing(req.viewing, a, payload);
  req.flash('ok', { approve: 'Viewing approved.', suggest: 'New time sent to the renter.', decline: 'Viewing declined.', complete: 'Marked as completed.' }[a]);
  res.redirect('/owner/viewings');
});

// ---- bookings
router.get('/bookings', (req, res) => {
  const tab = req.query.tab || 'all';
  let rows = db.find('bookings', b => b.ownerId === req.user.id).map(b => S.withRefs(b)).sort(byNewest);
  const counts = { all: rows.length, pending: rows.filter(b => b.status === 'Pending').length, confirmed: rows.filter(b => b.status === 'Confirmed').length, history: rows.filter(b => ['Completed', 'Rejected', 'Cancelled'].includes(b.status)).length };
  if (tab === 'pending') rows = rows.filter(b => b.status === 'Pending');
  if (tab === 'confirmed') rows = rows.filter(b => b.status === 'Confirmed');
  if (tab === 'history') rows = rows.filter(b => ['Completed', 'Rejected', 'Cancelled'].includes(b.status));
  res.render('owner/bookings', { title: 'Booking Requests', rows, tab, counts });
});
router.get('/bookings/:id', ownBooking, (req, res) => {
  const booking = S.withRefs(req.booking);
  const viewing = db.find('viewings', v => v.renterId === booking.renterId && v.propertyId === booking.propertyId).sort(byNewest)[0] || null;
  const renterHistory = db.find('bookings', b => b.renterId === booking.renterId && b.status === 'Completed').length;
  const others = db.find('bookings', b => b.propertyId === booking.propertyId && b.id !== booking.id && b.status === 'Pending').length;
  const convo = db.findOne('conversations', c => c.renterId === booking.renterId && c.ownerId === req.user.id && c.propertyId === booking.propertyId);
  res.render('owner/booking-details', { title: 'Booking Details', booking, viewing, renterHistory, others, convo });
});
router.post('/bookings/:id/:action', ownBooking, (req, res) => {
  const b = req.booking, a = req.params.action;
  if (a === 'accept' && b.status === 'Pending') { S.acceptBooking({ ...b, property: db.get('properties', b.propertyId) }); req.flash('ok', 'Booking accepted. The room is now Rented.'); }
  else if (a === 'reject' && b.status === 'Pending') { S.rejectBooking(b, req.body.reason); req.flash('ok', 'Booking rejected.'); }
  else if (a === 'cancel' && b.status === 'Confirmed') { S.cancelBooking(b, 'owner'); req.flash('ok', 'Booking cancelled. The room is Available again.'); }
  else if (a === 'complete' && b.status === 'Confirmed') { S.completeBooking(b); req.flash('ok', 'Rental marked as completed. The renter can now leave a review.'); }
  else req.flash('error', 'That action is not possible for this booking.');
  res.redirect(`/owner/bookings/${b.id}`);
});
router.post('/bookings/:id/message', ownBooking, (req, res) => {
  const c = S.getOrCreateConversation(req.booking.renterId, req.user.id, req.booking.propertyId);
  res.redirect(`/messages/${c.id}`);
});

// ---- reviews, profile
router.get('/reviews', (req, res) => {
  const mine = db.find('properties', p => p.ownerId === req.user.id);
  const rows = db.find('reviews', r => mine.some(p => p.id === r.propertyId)).map(r => ({ ...r, renter: db.get('users', r.renterId), property: db.get('properties', r.propertyId) })).sort(byNewest);
  const stats = S.ownerStats(req.user.id);
  res.render('owner/reviews', { title: 'Reviews', rows, stats });
});
router.get('/profile', (req, res) => {
  const stats = S.ownerStats(req.user.id);
  res.render('owner/profile', { title: 'Profile', stats });
});

module.exports = router;
