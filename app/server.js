const path = require('path');
const express = require('express');
const session = require('express-session');
const flash = require('connect-flash');
const db = require('./lib/db');
const H = require('./lib/helpers');
const S = require('./lib/services');

const app = express();
const PORT = process.env.PORT || 3000;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));
app.use(session({ secret: process.env.SESSION_SECRET || 'roomstay-dev-secret', resave: false, saveUninitialized: false, cookie: { maxAge: 7 * 86400000 } }));
app.use(flash());

// Current user + helpers available in every view.
app.use((req, res, next) => {
  req.user = req.session.userId ? db.get('users', req.session.userId) : null;
  if (req.user && req.user.status === 'suspended') { req.session.destroy(() => {}); req.user = null; }
  res.locals.user = req.user;
  res.locals.H = H;
  res.locals.path = req.path;
  res.locals.flash = { ok: req.flash('ok'), error: req.flash('error') };
  res.locals.unreadMessages = req.user ? S.unreadCount(req.user.id) : 0;
  res.locals.unreadNotes = req.user ? db.find('notifications', n => n.userId === req.user.id && !n.read).length : 0;
  next();
});

app.use('/', require('./routes/auth'));
app.use('/', require('./routes/renter'));
app.use('/owner', require('./routes/owner'));
app.use('/admin', require('./routes/admin'));

app.use((req, res) => res.status(404).render('error', { title: 'Page not found', message: 'That page does not exist.', code: 404 }));
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).render('error', { title: 'Something went wrong', message: err.message, code: 500 });
});

app.listen(PORT, () => console.log(`RoomStay running at http://localhost:${PORT}`));
