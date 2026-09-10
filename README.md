# RoomStay UI (Condo & Apartment Rental System)

Static UI design only. Plain HTML, CSS and a few lines of JavaScript. No backend, no database, no build step.

Open `ui/index.html` in a browser to see every screen on one board. Click a screen to open it full size.

## Folders

- `renter/` mobile screens shown inside a phone frame (welcome, sign up, log in, home, search, filters, room detail, chat, request viewing, favorites, bookings, booking details, review, profile, messages, notifications)
- `owner/` desktop screens with a sidebar (dashboard, listings, add property, booking requests, viewing requests, booking details, messages, reviews, profile)
- `admin/` desktop screens (dashboard, users, listings, reports)
- `css/style.css` all colours, type and components. Change the design here.
- `js/ui.js` small click interactions only (favorite toggle, pills, tabs, star rating, calendar day)

## Design tokens

- Primary: `#5B4FE9` (buttons, active nav, prices)
- Background: `#F3F4F8`, cards white, borders `#E6E8EF`
- Status colours: green Available/Confirmed, amber Pending/Reserved, red Rented/Rejected/Cancelled, blue Completed/Suggested, grey Unavailable/Draft
- Font: Inter (loaded from Google Fonts, falls back to system font)

## Notes

- Room photos load from Unsplash. Replace the URLs in the pages, or drop your own images in an `img/` folder, when you have real photos.
- There is no deposit or payment screen. The owner confirms a booking directly.
- Every button and link points at another page in this folder so the flow can be clicked through in the demo.


Log in with one of the demo accounts. Password for all three is password123:

- renter@roomstay.test
- owner@roomstay.test
- admin@roomstay.test
