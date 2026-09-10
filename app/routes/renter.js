const router = require('express').Router();
const bcrypt = require('bcryptjs');
const db = require('../lib/db');
const S = require('../lib/services');
const H = require('../lib/helpers');
const { requireLogin, requireRole } = require('../lib/auth');

const renter = requireRole('renter');
const favIds = req => req.user ? db.find('favorites', f => f.renterId === req.user.id).map(f => f.propertyId) : [];

router.get('/home', (req, res) => {
  const all = S.searchProperties({});
  res.render('renter/home', { title: 'Home', featured: all.filter(p => p.featured).slice(0, 3), nearby: all.filter(p => !p.featured).slice(0, 4), favIds: favIds(req) });
});

router.get('/search', (req, res) => {
  const q = { ...req.query };
  q.facilities = [].concat(q.facilities || []);
  res.render('renter/search', { title: 'Search', q, results: S.searchProperties(q), favIds: favIds(req), facilities: H.FACILITIES, types: H.ROOM_TYPES });
});
router.get('/filters', (req, res) => res.redirect('/search?' + new URLSearchParams(req.query).toString()));

router.get('/rooms/:id', (req, res, next) => {
  const p = db.get('properties', req.params.id);
  if (!p || (p.listingStatus !== 'published' && !(req.user && (req.user.role === 'admin' || req.user.id === p.ownerId)))) return next();
  db.update('properties', p.id, { views: (p.views || 0) + 1 });
  const property = S.propertyWithMeta(p);
  property.reviews = property.reviews.map(r => ({ ...r, renter: db.get('users', r.renterId) }));
  res.render('renter/room', { title: property.title, property, fav: req.user ? S.isFavorite(req.user.id, p.id) : false, facilities: H.FACILITIES });
});

router.post('/favorites/:id/toggle', renter, (req, res) => {
  S.toggleFavorite(req.user.id, req.params.id);
  res.redirect(req.get('Referer') || '/favorites');
});
router.get('/favorites', renter, (req, res) => {
  const rooms = favIds(req).map(id => db.get('properties', id)).filter(p => p && p.listingStatus === 'published');
  res.render('renter/favorites', { title: 'Favorites', rooms });
});

// ---- messages (shared by renter and owner)
router.get('/messages', requireLogin, (req, res) => {
  res.render('renter/messages', { title: 'Messages', convos: S.conversationsFor(req.user.id) });
});
router.post('/rooms/:id/message', renter, (req, res) => {
  const p = db.get('properties', req.params.id);
  if (!p) return res.redirect('/home');
  const c = S.getOrCreateConversation(req.user.id, p.ownerId, p.id);
  if (req.body.text && req.body.text.trim()) S.sendMessage(c.id, req.user.id, req.body.text);
  res.redirect(`/messages/${c.id}`);
});
router.get('/messages/:id', requireLogin, (req, res, next) => {
  const c = db.get('conversations', req.params.id);
  if (!c || (c.renterId !== req.user.id && c.ownerId !== req.user.id && req.user.role !== 'admin')) return next();
  S.markRead(c.id, req.user.id);
  const otherId = c.renterId === req.user.id ? c.ownerId : c.renterId;
  const msgs = db.find('messages', m => m.conversationId === c.id);
  res.render('renter/chat', { title: 'Chat', convo: { ...c, property: db.get('properties', c.propertyId), other: db.get('users', otherId) }, msgs });
});
router.post('/messages/:id', requireLogin, (req, res, next) => {
  const c = db.get('conversations', req.params.id);
  if (!c || (c.renterId !== req.user.id && c.ownerId !== req.user.id)) return next();
  if (req.body.text && req.body.text.trim()) {
    S.sendMessage(c.id, req.user.id, req.body.text);
    const target = c.renterId === req.user.id ? c.ownerId : c.renterId;
    const p = db.get('properties', c.propertyId);
    S.notify(target, 'New message', `${req.user.name}: ${req.body.text.trim().slice(0, 80)}`, `/messages/${c.id}`);
  }
  res.redirect(`/messages/${c.id}`);
});

// ---- viewing
router.get('/rooms/:id/viewing', renter, (req, res, next) => {
  const property = db.get('properties', req.params.id);
  if (!property) return next();
  res.render('renter/request-viewing', { title: 'Request viewing', property, rerequest: null });
});
router.post('/rooms/:id/viewing', renter, (req, res, next) => {
  const property = db.get('properties', req.params.id);
  if (!property) return next();
  if (!req.body.date || !req.body.time) { req.flash('error', 'Pick a date and a time.'); return res.redirect(`/rooms/${property.id}/viewing`); }
  S.requestViewing(req.user, property, new Date(`${req.body.date}T${req.body.time}:00`).toISOString(), req.body.message);
  req.flash('ok', 'Viewing request sent. The owner will reply soon.');
  res.redirect('/bookings');
});
router.post('/viewings/:id/:action', renter, (req, res, next) => {
  const v = db.get('viewings', req.params.id);
  if (!v || v.renterId !== req.user.id) return next();
  const payload = {};
  if (req.params.action === 'rerequest') {
    if (!req.body.date || !req.body.time) { req.flash('error', 'Pick a date and a time.'); return res.redirect('/bookings'); }
    payload.requestedAt = new Date(`${req.body.date}T${req.body.time}:00`).toISOString();
  }
  S.renterRespondViewing(v, req.params.action, payload);
  req.flash('ok', req.params.action === 'accept' ? 'Viewing time confirmed.' : 'Sent to the owner.');
  res.redirect('/bookings');
});
router.get('/viewings/:id/rerequest', renter, (req, res, next) => {
  const v = db.get('viewings', req.params.id);
  if (!v || v.renterId !== req.user.id) return next();
  res.render('renter/request-viewing', { title: 'Request another time', property: db.get('properties', v.propertyId), rerequest: v });
});

// ---- booking
router.get('/rooms/:id/book', renter, (req, res, next) => {
  const property = db.get('properties', req.params.id);
  if (!property) return next();
  if (property.status !== 'Available') { req.flash('error', 'This room is not available for booking right now.'); return res.redirect(`/rooms/${property.id}`); }
  const existing = db.findOne('bookings', b => b.renterId === req.user.id && b.propertyId === property.id && ['Pending', 'Confirmed'].includes(b.status));
  if (existing) { req.flash('error', 'You already have an active booking request for this room.'); return res.redirect(`/bookings/${existing.id}`); }
  res.render('renter/book', { title: 'Book this room', property: S.propertyWithMeta(property) });
});
router.post('/rooms/:id/book', renter, (req, res, next) => {
  const property = db.get('properties', req.params.id);
  if (!property || property.status !== 'Available') return next();
  if (!req.body.moveInDate) { req.flash('error', 'Choose a move-in date.'); return res.redirect(`/rooms/${property.id}/book`); }
  const b = S.requestBooking(req.user, property, req.body.moveInDate, req.body.months, req.body.note);
  req.flash('ok', 'Booking request sent. You will be notified when the owner decides.');
  res.redirect(`/bookings/${b.id}`);
});
router.get('/bookings', renter, (req, res) => {
  const bookings = db.find('bookings', b => b.renterId === req.user.id).map(b => S.withRefs(b)).sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  const viewings = db.find('viewings', v => v.renterId === req.user.id && !['Completed', 'Cancelled'].includes(v.status)).map(v => S.withRefs(v)).sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  const reviewed = new Set(db.all('reviews').map(r => r.bookingId));
  res.render('renter/bookings', { title: 'My Bookings', bookings, viewings, reviewed, tab: req.query.tab || 'all' });
});
router.get('/bookings/:id', renter, (req, res, next) => {
  const b = db.get('bookings', req.params.id);
  if (!b || b.renterId !== req.user.id) return next();
  const booking = S.withRefs(b);
  const review = db.findOne('reviews', r => r.bookingId === b.id);
  res.render('renter/booking-details', { title: 'Booking details', booking, review, canReview: S.canReview(req.user.id, b) });
});
router.post('/bookings/:id/cancel', renter, (req, res, next) => {
  const b = db.get('bookings', req.params.id);
  if (!b || b.renterId !== req.user.id || !['Pending', 'Confirmed'].includes(b.status)) return next();
  S.cancelBooking(b, 'renter');
  req.flash('ok', 'Booking cancelled.');
  res.redirect(`/bookings/${b.id}`);
});

// ---- review
router.get('/bookings/:id/review', renter, (req, res, next) => {
  const b = db.get('bookings', req.params.id);
  if (!b || !S.canReview(req.user.id, b)) { req.flash('error', 'Only a completed booking can be reviewed, once.'); return res.redirect('/bookings'); }
  res.render('renter/review', { title: 'Leave a review', booking: S.withRefs(b) });
});
router.post('/bookings/:id/review', renter, (req, res, next) => {
  const b = db.get('bookings', req.params.id);
  if (!b || !S.canReview(req.user.id, b)) return next();
  const rating = Math.min(5, Math.max(1, Number(req.body.rating) || 0));
  if (!rating) { req.flash('error', 'Choose a star rating.'); return res.redirect(`/bookings/${b.id}/review`); }
  db.insert('reviews', { bookingId: b.id, renterId: req.user.id, propertyId: b.propertyId, rating, comment: (req.body.comment || '').trim(), hidden: false });
  S.notify(b.ownerId, 'New review', `${req.user.name} left a ${rating} star review.`, '/owner/reviews');
  req.flash('ok', 'Review published. Thank you.');
  res.redirect(`/bookings/${b.id}`);
});

// ---- report
router.post('/report', requireLogin, (req, res) => {
  const targetType = ['listing', 'user', 'review'].includes(req.body.targetType) ? req.body.targetType : 'listing';
  if (!req.body.reason || !req.body.reason.trim()) { req.flash('error', 'Tell us why you are reporting this.'); return res.redirect(req.get('Referer') || '/home'); }
  db.insert('reports', { reporterId: req.user.id, targetType, targetId: Number(req.body.targetId), reason: req.body.reason.trim(), status: 'Open' });
  req.flash('ok', 'Report sent. An admin will review it.');
  res.redirect(req.get('Referer') || '/home');
});

// ---- notifications, profile
router.get('/notifications', requireLogin, (req, res) => {
  const notes = db.find('notifications', n => n.userId === req.user.id).sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  res.render('renter/notifications', { title: 'Notifications', notes });
});
router.post('/notifications/read', requireLogin, (req, res) => {
  db.find('notifications', n => n.userId === req.user.id && !n.read).forEach(n => db.update('notifications', n.id, { read: true }));
  res.redirect(req.get('Referer') || '/notifications');
});
router.get('/profile', requireLogin, (req, res) => res.render('renter/profile', { title: 'Profile' }));
router.post('/profile', requireLogin, (req, res) => {
  const patch = { name: (req.body.name || req.user.name).trim(), phone: (req.body.phone || '').trim() };
  if (req.body.password) {
    if (req.body.password.length < 8) { req.flash('error', 'Password must be at least 8 characters.'); return res.redirect('/profile'); }
    patch.passwordHash = bcrypt.hashSync(req.body.password, 10);
  }
  db.update('users', req.user.id, patch);
  req.flash('ok', 'Profile saved.');
  res.redirect(req.get('Referer') || '/profile');
});

module.exports = router;
