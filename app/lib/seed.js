// Fills /data with demo users, rooms, bookings and messages.
// Run: npm run seed   (this overwrites the data files)
const bcrypt = require('bcryptjs');
const db = require('./db');

const hash = p => bcrypt.hashSync(p, 10);
const daysAgo = n => new Date(Date.now() - n * 86400000).toISOString();
const daysAhead = n => new Date(Date.now() + n * 86400000).toISOString();
const PW = 'password123';

const users = [
  { id: 1, name: 'Admin User', email: 'admin@roomstay.test', passwordHash: hash(PW), role: 'admin', phone: '', status: 'active', createdAt: daysAgo(400) },
  { id: 2, name: 'Thana Kittipong', email: 'owner@roomstay.test', passwordHash: hash(PW), role: 'owner', phone: '+66 81 234 5678', status: 'active', createdAt: daysAgo(380) },
  { id: 3, name: 'Su Yi Nandar', email: 'renter@roomstay.test', passwordHash: hash(PW), role: 'renter', phone: '+66 89 000 1111', status: 'active', createdAt: daysAgo(120) },
  { id: 4, name: 'Alice Johnson', email: 'alice@roomstay.test', passwordHash: hash(PW), role: 'renter', phone: '', status: 'active', createdAt: daysAgo(90) },
  { id: 5, name: 'Michael Brown', email: 'michael@roomstay.test', passwordHash: hash(PW), role: 'renter', phone: '', status: 'active', createdAt: daysAgo(200) },
  { id: 6, name: 'Kanya Srisuk', email: 'kanya@roomstay.test', passwordHash: hash(PW), role: 'owner', phone: '+66 82 555 9999', status: 'active', createdAt: daysAgo(300) },
  { id: 7, name: 'Peter Tan', email: 'peter@roomstay.test', passwordHash: hash(PW), role: 'owner', phone: '', status: 'suspended', createdAt: daysAgo(40) },
];

const U = 'https://images.unsplash.com/';
const P = (i, extra = '') => `${U}${i}?w=900&q=70${extra}`;
const PH = {
  a: P('photo-1522708323590-d24dbb6b0267'), b: P('photo-1502672260266-1c1ef2d93688'),
  c: P('photo-1560448204-e02f11c3d0e2'), d: P('photo-1536376072261-38c75010e6c9'),
  e: P('photo-1493809842364-78817add7ffb'), f: P('photo-1484154218962-a197022b5858'),
  g: P('photo-1554995207-c18c203602cb'), h: P('photo-1505693416388-ac5ce068fe85'),
};

const properties = [
  { id: 1, ownerId: 2, title: 'Cozy Condo Near BTS', type: 'Condo', location: 'Ari, Bangkok', address: '45 Phahon Yothin 7, Phaya Thai, Bangkok 10400', monthlyRent: 10000, bedrooms: 1, bathrooms: 1, sizeSqm: 30, facilities: ['wifi', 'aircon', 'furnished', 'elevator', 'pets'], description: 'A cozy and comfortable condo near BTS Ari. Fully furnished with bed, wardrobe, desk, air conditioner, and free Wi-Fi. Suitable for students and working professionals.', photos: [PH.a, PH.b, PH.f], status: 'Available', listingStatus: 'published', availableFrom: daysAhead(10), views: 245, featured: true, createdAt: daysAgo(60) },
  { id: 2, ownerId: 2, title: 'Modern Studio', type: 'Condo', location: 'Phahon Yothin, Bangkok', address: '123 Phahon Yothin Rd, Chatuchak, Bangkok 10900', monthlyRent: 8500, bedrooms: 1, bathrooms: 1, sizeSqm: 25, facilities: ['wifi', 'aircon', 'furnished', 'security'], description: 'Modern and cozy studio near BTS. Fully furnished with bed, wardrobe, desk, air conditioner and free Wi-Fi.', photos: [PH.b, PH.d], status: 'Reserved', listingStatus: 'published', availableFrom: daysAhead(20), views: 312, createdAt: daysAgo(55) },
  { id: 3, ownerId: 2, title: 'Spacious Apartment', type: 'Apartment', location: 'Chatuchak, Bangkok', address: '9 Ratchadaphisek 3, Chatuchak, Bangkok 10900', monthlyRent: 12000, bedrooms: 1, bathrooms: 1, sizeSqm: 20, facilities: ['wifi', 'aircon', 'parking', 'elevator'], description: 'Bright apartment with a large window, 5 minutes to MRT Chatuchak Park. Quiet building with 24 hour security.', photos: [PH.c, PH.a], status: 'Rented', listingStatus: 'published', availableFrom: daysAgo(30), views: 198, createdAt: daysAgo(50) },
  { id: 4, ownerId: 2, title: 'Condo One Bedroom', type: 'Condo', location: 'Sukhumvit, Bangkok', address: '88 Sukhumvit 24, Khlong Toei, Bangkok 10110', monthlyRent: 15000, bedrooms: 1, bathrooms: 1, sizeSqm: 35, facilities: ['wifi', 'aircon', 'furnished', 'gym', 'pool'], description: 'One bedroom condo with pool and gym, walking distance to BTS Phrom Phong.', photos: [PH.d, PH.e], status: 'Unavailable', listingStatus: 'draft', availableFrom: daysAhead(45), views: 0, createdAt: daysAgo(5) },
  { id: 5, ownerId: 2, title: 'Luxury Room', type: 'Room', location: 'Asoke, Bangkok', address: '12 Sukhumvit 21, Watthana, Bangkok 10110', monthlyRent: 18000, bedrooms: 1, bathrooms: 1, sizeSqm: 28, facilities: ['wifi', 'aircon', 'furnished', 'elevator', 'security', 'gym'], description: 'Premium room in a new building at Asoke. City view, high floor, fully furnished.', photos: [PH.e, PH.g], status: 'Available', listingStatus: 'published', availableFrom: daysAhead(3), views: 176, featured: true, createdAt: daysAgo(30) },
  { id: 6, ownerId: 6, title: 'Garden House', type: 'House', location: 'Ladprao, Bangkok', address: '210 Ladprao 41, Chatuchak, Bangkok 10900', monthlyRent: 15000, bedrooms: 2, bathrooms: 1, sizeSqm: 48, facilities: ['wifi', 'parking', 'pets', 'furnished'], description: 'Two bedroom house with a small garden. Parking for one car. Pets welcome.', photos: [PH.f, PH.h], status: 'Available', listingStatus: 'published', availableFrom: daysAhead(7), views: 88, createdAt: daysAgo(25) },
  { id: 7, ownerId: 6, title: 'Student Room near Kasetsart', type: 'Room', location: 'Kasetsart, Bangkok', address: '5 Ngamwongwan 2, Chatuchak, Bangkok 10900', monthlyRent: 5500, bedrooms: 1, bathrooms: 1, sizeSqm: 22, facilities: ['wifi', 'aircon'], description: 'Budget room 5 minutes from Kasetsart University. Shared laundry on the ground floor.', photos: [PH.g, PH.c], status: 'Available', listingStatus: 'published', availableFrom: daysAhead(1), views: 140, createdAt: daysAgo(20) },
  { id: 8, ownerId: 7, title: 'Riverside Loft', type: 'Apartment', location: 'Charoen Krung, Bangkok', address: '30 Charoen Krung 30, Bang Rak, Bangkok 10500', monthlyRent: 22000, bedrooms: 2, bathrooms: 2, sizeSqm: 70, facilities: ['wifi', 'aircon', 'furnished', 'parking', 'pool'], description: 'Loft apartment by the river. Photos may not match the current furniture.', photos: [PH.h, PH.d], status: 'Available', listingStatus: 'disabled', availableFrom: daysAhead(2), views: 40, createdAt: daysAgo(15) },
];

const favorites = [
  { id: 1, renterId: 3, propertyId: 1, createdAt: daysAgo(10) },
  { id: 2, renterId: 3, propertyId: 5, createdAt: daysAgo(8) },
  { id: 3, renterId: 3, propertyId: 6, createdAt: daysAgo(4) },
  { id: 4, renterId: 4, propertyId: 1, createdAt: daysAgo(3) },
];

const viewings = [
  { id: 1, renterId: 3, propertyId: 1, ownerId: 2, requestedAt: daysAgo(12), suggestedAt: null, message: 'I would like to see the room this weekend.', status: 'Completed', responseReason: '', createdAt: daysAgo(15) },
  { id: 2, renterId: 3, propertyId: 5, ownerId: 2, requestedAt: daysAhead(4), suggestedAt: daysAhead(5), message: '', status: 'Suggested', responseReason: 'I am not free on that day.', createdAt: daysAgo(2) },
  { id: 3, renterId: 4, propertyId: 1, ownerId: 2, requestedAt: daysAhead(3), suggestedAt: null, message: 'Can I bring my partner?', status: 'Requested', responseReason: '', createdAt: daysAgo(1) },
  { id: 4, renterId: 5, propertyId: 2, ownerId: 2, requestedAt: daysAhead(2), suggestedAt: null, message: '', status: 'Confirmed', responseReason: '', createdAt: daysAgo(3) },
  { id: 5, renterId: 3, propertyId: 6, ownerId: 6, requestedAt: daysAgo(6), suggestedAt: null, message: '', status: 'Declined', responseReason: 'The house is being repainted that week.', createdAt: daysAgo(8) },
];

const bookings = [
  { id: 1, renterId: 3, propertyId: 3, ownerId: 2, moveInDate: daysAgo(365), months: 12, note: '', status: 'Completed', createdAt: daysAgo(380), decidedAt: daysAgo(378), completedAt: daysAgo(20) },
  { id: 2, renterId: 3, propertyId: 2, ownerId: 2, moveInDate: daysAhead(20), months: 12, note: 'I work near Ari and would like to move in at the start of next month.', status: 'Confirmed', createdAt: daysAgo(5), decidedAt: daysAgo(4) },
  { id: 3, renterId: 3, propertyId: 1, ownerId: 2, moveInDate: daysAhead(15), months: 6, note: '', status: 'Pending', createdAt: daysAgo(1) },
  { id: 4, renterId: 4, propertyId: 1, ownerId: 2, moveInDate: daysAhead(12), months: 12, note: 'Ready to move in any time.', status: 'Pending', createdAt: daysAgo(2) },
  { id: 5, renterId: 5, propertyId: 3, ownerId: 2, moveInDate: daysAgo(10), months: 12, note: '', status: 'Confirmed', createdAt: daysAgo(18), decidedAt: daysAgo(16) },
  { id: 6, renterId: 4, propertyId: 5, ownerId: 2, moveInDate: daysAgo(40), months: 6, note: '', status: 'Rejected', createdAt: daysAgo(45), decidedAt: daysAgo(44), decisionReason: 'Room was already reserved.' },
  { id: 7, renterId: 5, propertyId: 6, ownerId: 6, moveInDate: daysAgo(30), months: 12, note: '', status: 'Cancelled', createdAt: daysAgo(35), decidedAt: daysAgo(34), cancelledAt: daysAgo(31), cancelledBy: 'renter' },
];

const reviews = [
  { id: 1, bookingId: 1, renterId: 3, propertyId: 3, rating: 5, comment: 'The room is clean and comfortable. The owner is very kind and responsive. Highly recommend!', hidden: false, createdAt: daysAgo(18) },
  { id: 2, bookingId: 6, renterId: 4, propertyId: 1, rating: 4, comment: 'Good value. Wi-Fi is fast. Slightly noisy on weekends.', hidden: false, createdAt: daysAgo(30) },
];

const conversations = [
  { id: 1, renterId: 3, ownerId: 2, propertyId: 1, createdAt: daysAgo(14), updatedAt: daysAgo(0.1) },
  { id: 2, renterId: 4, ownerId: 2, propertyId: 2, createdAt: daysAgo(2), updatedAt: daysAgo(1) },
  { id: 3, renterId: 3, ownerId: 6, propertyId: 6, createdAt: daysAgo(9), updatedAt: daysAgo(6) },
];
const h = (d, hrs) => new Date(new Date(d).getTime() + hrs * 3600000).toISOString();
const messages = [
  { id: 1, conversationId: 1, senderId: 3, text: 'Hi! Is the room still available?', sentAt: daysAgo(0.2), readBy: [3, 2] },
  { id: 2, conversationId: 1, senderId: 2, text: 'Yes, it is still available. When would you like to see it?', sentAt: h(daysAgo(0.2), 0.05), readBy: [3, 2] },
  { id: 3, conversationId: 1, senderId: 3, text: 'Can I visit this weekend?', sentAt: h(daysAgo(0.2), 0.1), readBy: [3, 2] },
  { id: 4, conversationId: 1, senderId: 2, text: 'Sure! How about Saturday at 2 PM?', sentAt: h(daysAgo(0.2), 0.15), readBy: [3, 2] },
  { id: 5, conversationId: 1, senderId: 3, text: 'That works for me. See you then!', sentAt: h(daysAgo(0.2), 0.2), readBy: [3] },
  { id: 6, conversationId: 2, senderId: 4, text: 'Is the studio still available?', sentAt: daysAgo(1), readBy: [4] },
  { id: 7, conversationId: 3, senderId: 3, text: 'Is parking included?', sentAt: daysAgo(6.1), readBy: [3, 6] },
  { id: 8, conversationId: 3, senderId: 6, text: 'Yes, parking is included.', sentAt: daysAgo(6), readBy: [3, 6] },
];

const reports = [
  { id: 1, reporterId: 4, targetType: 'listing', targetId: 8, reason: 'Photos do not match the room.', status: 'Open', createdAt: daysAgo(3) },
  { id: 2, reporterId: 3, targetType: 'user', targetId: 7, reason: 'Asked for payment before viewing.', status: 'Open', createdAt: daysAgo(4) },
  { id: 3, reporterId: 5, targetType: 'listing', targetId: 4, reason: 'Listing is outdated.', status: 'Reviewed', createdAt: daysAgo(6) },
];

const notifications = [
  { id: 1, userId: 3, title: 'Booking confirmed', body: 'Thana Kittipong accepted your booking for Modern Studio.', link: '/bookings/2', read: false, createdAt: daysAgo(4) },
  { id: 2, userId: 3, title: 'New time suggested', body: 'The owner suggested another time for your Luxury Room viewing.', link: '/bookings', read: false, createdAt: daysAgo(2) },
  { id: 3, userId: 3, title: 'Viewing declined', body: 'Garden House viewing was declined: the house is being repainted that week.', link: '/bookings', read: true, createdAt: daysAgo(6) },
  { id: 4, userId: 2, title: 'New booking request', body: 'Su Yi Nandar requested to book Cozy Condo Near BTS.', link: '/owner/bookings/3', read: false, createdAt: daysAgo(1) },
  { id: 5, userId: 2, title: 'New viewing request', body: 'Alice Johnson requested a viewing for Cozy Condo Near BTS.', link: '/owner/viewings', read: false, createdAt: daysAgo(1) },
];

db.reset('users', users);
db.reset('properties', properties);
db.reset('favorites', favorites);
db.reset('viewings', viewings);
db.reset('bookings', bookings);
db.reset('reviews', reviews);
db.reset('conversations', conversations);
db.reset('messages', messages);
db.reset('reports', reports);
db.reset('notifications', notifications);

console.log('Seeded data/ with demo records.');
console.log('Log in with password "password123":');
console.log('  renter@roomstay.test   (Renter)');
console.log('  owner@roomstay.test    (Owner)');
console.log('  admin@roomstay.test    (Admin)');
