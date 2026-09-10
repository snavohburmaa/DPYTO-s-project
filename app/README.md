# RoomStay, Condo & Apartment Rental System

Web app for the Systems Analysis and Design semester project. Renters search rooms, chat with owners, request viewings, and book. Owners manage listings and respond to requests. Admins moderate users, listings, reviews and reports. There is no deposit or payment step: the owner's acceptance confirms the booking.

Stack: Node.js, Express, EJS views, express-session with bcrypt password hashing, multer for photo uploads. Data is stored in JSON files under `data/` (one file per table) so it runs with nothing installed except Node. Swap `lib/db.js` for a real database later without touching the routes.

## Run it

```
cd app
npm install
npm run seed      # creates demo data in data/ (safe to re-run, it resets the data)
npm start         # http://localhost:3000
```

`npm run dev` restarts the server when a file changes.

Demo accounts (password for all: `password123`):

| Role   | Email                 |
|--------|-----------------------|
| Renter | renter@roomstay.test  |
| Owner  | owner@roomstay.test   |
| Admin  | admin@roomstay.test   |

The login page has one-click buttons for each of these.

## Folders

```
server.js          app setup, sessions, global view helpers
lib/db.js          JSON file database (all, find, get, insert, update, remove)
lib/services.js    business rules (booking, viewing, messages, notifications)
lib/helpers.js     formatting helpers and icons used by views (H.money, H.fmtDate, H.ic, ...)
lib/seed.js        demo data
lib/auth.js        requireLogin / requireRole guards
routes/auth.js     /welcome /login /register /logout
routes/renter.js   /home /search /rooms/:id /favorites /messages /bookings /notifications /profile /report
routes/owner.js    /owner/... listings, viewings, bookings, reviews, profile
routes/admin.js    /admin/... users, listings, reviews, reports, bookings
views/             EJS templates. partials/web-open and desk-open are the two page shells
                   (renter and public pages use the top navigation bar, owner and admin use the sidebar).
public/css         style.css (the ../ui folder holds the earlier static mobile mockups, not used by the app)
public/uploads     photos uploaded by owners
data/              users, properties, favorites, viewings, bookings, reviews,
                   conversations, messages, reports, notifications (JSON)
```

## Business rules implemented

- A user must be logged in as a renter to favorite, message, request a viewing, or book.
- Viewing request: owner can approve, suggest another time, or decline with a reason. A suggested time becomes confirmed when the renter accepts it; the renter can also ask for a different time.
- Booking request: owner accepts or rejects. Accepting sets the room to Rented and automatically rejects other pending requests for that room. Rejecting keeps the room as it was.
- Renter or owner can cancel a Pending or Confirmed booking; the room returns to Available if no other confirmed booking exists.
- Owner marks a rental Completed; only then can that renter leave one review for that booking.
- Owners can only edit, delete, or change status on their own listings. A listing with an active booking cannot be deleted. Publishing requires at least one photo.
- Owner listing statuses: Available, Reserved, Rented, Unavailable (room) and published, draft, disabled (listing). Only published listings appear in search. Disabled is set by an admin.
- Anyone logged in can report a listing, user, or review. Admins mark reports Open, Reviewed, or Actioned and can disable listings, suspend users, or hide reviews.
- Suspended users cannot log in. Passwords are stored as bcrypt hashes.
- Every status change sends the other party an in-app notification.

## Notes for the report

The ERD in `../docs/charts` matches the JSON tables one to one, except that room photos are stored as an array on each property instead of a separate PropertyPhotos table. Conversations and Messages are separate tables as in the ERD.
