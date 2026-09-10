// Business rules live here so routes stay thin.
const db = require('./db');

function notify(userId, title, body, link) {
  return db.insert('notifications', { userId, title, body, link, read: false });
}

function withRefs(row, opts = {}) {
  if (!row) return row;
  const out = { ...row };
  if (opts.property !== false && row.propertyId) out.property = db.get('properties', row.propertyId);
  if (opts.renter !== false && row.renterId) out.renter = db.get('users', row.renterId);
  if (opts.owner !== false && row.ownerId) out.owner = db.get('users', row.ownerId);
  return out;
}

// ---- properties
function propertyWithMeta(p) {
  if (!p) return null;
  const reviews = db.find('reviews', r => r.propertyId === p.id && !r.hidden);
  const avg = reviews.length ? reviews.reduce((s, r) => s + r.rating, 0) / reviews.length : 0;
  const inquiries = db.find('conversations', c => c.propertyId === p.id).length;
  return { ...p, owner: db.get('users', p.ownerId), reviews, rating: Math.round(avg * 10) / 10, reviewCount: reviews.length, inquiries };
}
function visibleProperties() {
  return db.find('properties', p => p.listingStatus === 'published');
}

function searchProperties(q = {}) {
  let rows = visibleProperties();
  if (q.q) { const s = q.q.toLowerCase(); rows = rows.filter(p => (p.title + ' ' + p.location + ' ' + p.address + ' ' + p.description).toLowerCase().includes(s)); }
  if (q.type && q.type !== 'All') rows = rows.filter(p => p.type === q.type);
  if (q.min) rows = rows.filter(p => p.monthlyRent >= Number(q.min));
  if (q.max) rows = rows.filter(p => p.monthlyRent <= Number(q.max));
  if (q.bedrooms && q.bedrooms !== 'Any') rows = rows.filter(p => q.bedrooms === '3+' ? p.bedrooms >= 3 : p.bedrooms === Number(q.bedrooms));
  const fac = [].concat(q.facilities || []).filter(Boolean);
  if (fac.length) rows = rows.filter(p => fac.every(f => (p.facilities || []).includes(f)));
  if (q.availability === 'now') rows = rows.filter(p => p.status === 'Available');
  const sort = q.sort || 'newest';
  if (sort === 'price_asc') rows.sort((a, b) => a.monthlyRent - b.monthlyRent);
  else if (sort === 'price_desc') rows.sort((a, b) => b.monthlyRent - a.monthlyRent);
  else rows.sort((a, b) => (b.featured ? 1 : 0) - (a.featured ? 1 : 0) || new Date(b.createdAt) - new Date(a.createdAt));
  return rows;
}

// ---- favorites
function isFavorite(renterId, propertyId) {
  return !!db.findOne('favorites', f => f.renterId === renterId && f.propertyId === Number(propertyId));
}
function toggleFavorite(renterId, propertyId) {
  const f = db.findOne('favorites', f => f.renterId === renterId && f.propertyId === Number(propertyId));
  if (f) { db.remove('favorites', f.id); return false; }
  db.insert('favorites', { renterId, propertyId: Number(propertyId) });
  return true;
}

// ---- conversations
function getOrCreateConversation(renterId, ownerId, propertyId) {
  let c = db.findOne('conversations', c => c.renterId === renterId && c.ownerId === ownerId && c.propertyId === Number(propertyId));
  if (!c) c = db.insert('conversations', { renterId, ownerId, propertyId: Number(propertyId), updatedAt: new Date().toISOString() });
  return c;
}
function sendMessage(conversationId, senderId, text) {
  const m = db.insert('messages', { conversationId: Number(conversationId), senderId, text: text.trim(), sentAt: new Date().toISOString(), readBy: [senderId] });
  db.update('conversations', conversationId, { updatedAt: m.sentAt });
  return m;
}
function conversationsFor(userId) {
  return db.find('conversations', c => c.renterId === userId || c.ownerId === userId)
    .map(c => {
      const msgs = db.find('messages', m => m.conversationId === c.id);
      const last = msgs[msgs.length - 1] || null;
      const unread = msgs.filter(m => !m.readBy.includes(userId)).length;
      const otherId = c.renterId === userId ? c.ownerId : c.renterId;
      return { ...c, property: db.get('properties', c.propertyId), other: db.get('users', otherId), last, unread };
    })
    .sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt));
}
function markRead(conversationId, userId) {
  db.find('messages', m => m.conversationId === Number(conversationId) && !m.readBy.includes(userId))
    .forEach(m => db.update('messages', m.id, { readBy: [...m.readBy, userId] }));
}
function unreadCount(userId) {
  return conversationsFor(userId).reduce((s, c) => s + c.unread, 0);
}

// ---- viewings
function requestViewing(renter, property, requestedAt, message) {
  const v = db.insert('viewings', { renterId: renter.id, propertyId: property.id, ownerId: property.ownerId, requestedAt, suggestedAt: null, message: message || '', status: 'Requested', responseReason: '' });
  notify(property.ownerId, 'New viewing request', `${renter.name} requested a viewing for ${property.title}.`, '/owner/viewings');
  return v;
}
function ownerRespondViewing(v, action, payload = {}) {
  const property = db.get('properties', v.propertyId);
  if (action === 'approve') {
    db.update('viewings', v.id, { status: 'Confirmed' });
    notify(v.renterId, 'Viewing approved', `Your viewing for ${property.title} is confirmed.`, '/bookings');
  } else if (action === 'suggest') {
    db.update('viewings', v.id, { status: 'Suggested', suggestedAt: payload.suggestedAt, responseReason: payload.reason || '' });
    notify(v.renterId, 'New time suggested', `The owner suggested another time for your ${property.title} viewing.`, '/bookings');
  } else if (action === 'decline') {
    db.update('viewings', v.id, { status: 'Declined', responseReason: payload.reason || '' });
    notify(v.renterId, 'Viewing declined', `${property.title} viewing was declined: ${payload.reason || 'no reason given'}.`, '/bookings');
  } else if (action === 'complete') {
    db.update('viewings', v.id, { status: 'Completed' });
  }
}
function renterRespondViewing(v, action, payload = {}) {
  const property = db.get('properties', v.propertyId);
  const renter = db.get('users', v.renterId);
  if (action === 'accept' && v.status === 'Suggested') {
    db.update('viewings', v.id, { status: 'Confirmed', requestedAt: v.suggestedAt });
    notify(v.ownerId, 'Viewing time agreed', `${renter.name} agreed to your suggested time for ${property.title}.`, '/owner/viewings');
  } else if (action === 'rerequest') {
    db.update('viewings', v.id, { status: 'Requested', requestedAt: payload.requestedAt, suggestedAt: null, responseReason: '' });
    notify(v.ownerId, 'New viewing time requested', `${renter.name} requested a different time for ${property.title}.`, '/owner/viewings');
  } else if (action === 'cancel') {
    db.update('viewings', v.id, { status: 'Cancelled' });
  }
}

// ---- bookings
function requestBooking(renter, property, moveInDate, months, note) {
  const b = db.insert('bookings', { renterId: renter.id, propertyId: property.id, ownerId: property.ownerId, moveInDate, months: Number(months) || 12, note: note || '', status: 'Pending' });
  notify(property.ownerId, 'New booking request', `${renter.name} requested to book ${property.title}.`, `/owner/bookings/${b.id}`);
  return b;
}
function acceptBooking(b) {
  const property = db.get('properties', b.propertyId);
  db.update('bookings', b.id, { status: 'Confirmed', decidedAt: new Date().toISOString() });
  db.update('properties', property.id, { status: 'Rented' });
  notify(b.renterId, 'Booking confirmed', `${property.owner ? property.owner.name : 'The owner'} accepted your booking for ${property.title}.`, `/bookings/${b.id}`);
  // Other pending requests for the same room are rejected automatically.
  db.find('bookings', o => o.propertyId === b.propertyId && o.id !== b.id && o.status === 'Pending').forEach(o => {
    db.update('bookings', o.id, { status: 'Rejected', decidedAt: new Date().toISOString(), decisionReason: 'The room was booked by another renter.' });
    notify(o.renterId, 'Booking not available', `${property.title} was booked by another renter.`, `/bookings/${o.id}`);
  });
}
function rejectBooking(b, reason) {
  const property = db.get('properties', b.propertyId);
  db.update('bookings', b.id, { status: 'Rejected', decidedAt: new Date().toISOString(), decisionReason: reason || '' });
  notify(b.renterId, 'Booking rejected', `Your booking request for ${property.title} was rejected${reason ? ': ' + reason : '.'}`, `/bookings/${b.id}`);
}
function releaseRoomIfFree(propertyId) {
  const stillRented = db.findOne('bookings', o => o.propertyId === propertyId && o.status === 'Confirmed');
  if (!stillRented) db.update('properties', propertyId, { status: 'Available' });
}
function cancelBooking(b, by) {
  const property = db.get('properties', b.propertyId);
  db.update('bookings', b.id, { status: 'Cancelled', cancelledAt: new Date().toISOString(), cancelledBy: by });
  releaseRoomIfFree(b.propertyId);
  const target = by === 'renter' ? b.ownerId : b.renterId;
  notify(target, 'Booking cancelled', `The booking for ${property.title} was cancelled by the ${by}.`, by === 'renter' ? `/owner/bookings/${b.id}` : `/bookings/${b.id}`);
}
function completeBooking(b) {
  const property = db.get('properties', b.propertyId);
  db.update('bookings', b.id, { status: 'Completed', completedAt: new Date().toISOString() });
  releaseRoomIfFree(b.propertyId);
  notify(b.renterId, 'Rental completed', `Your rental of ${property.title} is complete. You can now leave a review.`, `/bookings/${b.id}/review`);
}
function canReview(renterId, booking) {
  if (!booking || booking.renterId !== renterId || booking.status !== 'Completed') return false;
  return !db.findOne('reviews', r => r.bookingId === booking.id);
}

// ---- owner stats
function ownerStats(ownerId) {
  const listings = db.find('properties', p => p.ownerId === ownerId);
  const bookings = db.find('bookings', b => b.ownerId === ownerId);
  const viewings = db.find('viewings', v => v.ownerId === ownerId);
  const reviews = db.find('reviews', r => listings.some(p => p.id === r.propertyId) && !r.hidden);
  const avg = reviews.length ? reviews.reduce((s, r) => s + r.rating, 0) / reviews.length : 0;
  return {
    listings: listings.length, published: listings.filter(p => p.listingStatus === 'published').length,
    pendingBookings: bookings.filter(b => b.status === 'Pending').length,
    newViewings: viewings.filter(v => v.status === 'Requested').length,
    confirmed: bookings.filter(b => b.status === 'Confirmed').length,
    rating: Math.round(avg * 10) / 10, reviewCount: reviews.length,
    byStatus: ['Available', 'Reserved', 'Rented', 'Unavailable'].map(s => ({ status: s, n: listings.filter(p => p.status === s).length })),
  };
}

module.exports = { notify, withRefs, propertyWithMeta, visibleProperties, searchProperties, isFavorite, toggleFavorite, getOrCreateConversation, sendMessage, conversationsFor, markRead, unreadCount, requestViewing, ownerRespondViewing, renterRespondViewing, requestBooking, acceptBooking, rejectBooking, cancelBooking, completeBooking, canReview, ownerStats };
