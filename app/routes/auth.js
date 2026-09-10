const router = require('express').Router();
const bcrypt = require('bcryptjs');
const db = require('../lib/db');
const { homeFor } = require('../lib/auth');

router.get('/', (req, res) => res.redirect(homeFor(req.user)));
router.get('/welcome', (req, res) => req.user ? res.redirect(homeFor(req.user)) : res.render('auth/welcome', { title: 'RoomStay' }));

router.get('/login', (req, res) => req.user ? res.redirect(homeFor(req.user)) : res.render('auth/login', { title: 'Log in', email: '' }));
router.post('/login', (req, res) => {
  const email = (req.body.email || '').trim().toLowerCase();
  const user = db.findOne('users', u => u.email.toLowerCase() === email);
  if (!user || !bcrypt.compareSync(req.body.password || '', user.passwordHash)) {
    req.flash('error', 'Email or password is incorrect.');
    return res.render('auth/login', { title: 'Log in', email, flash: { error: ['Email or password is incorrect.'], ok: [] } });
  }
  if (user.status === 'suspended') {
    return res.render('auth/login', { title: 'Log in', email, flash: { error: ['This account has been suspended. Contact support.'], ok: [] } });
  }
  req.session.userId = user.id;
  const to = req.session.returnTo || homeFor(user);
  delete req.session.returnTo;
  res.redirect(to);
});

router.get('/register', (req, res) => req.user ? res.redirect(homeFor(req.user)) : res.render('auth/register', { title: 'Create account', form: { role: 'renter' } }));
router.post('/register', (req, res) => {
  const form = { name: (req.body.name || '').trim(), email: (req.body.email || '').trim().toLowerCase(), role: req.body.role === 'owner' ? 'owner' : 'renter' };
  const errors = [];
  if (form.name.length < 2) errors.push('Enter your full name.');
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.email)) errors.push('Enter a valid email address.');
  if ((req.body.password || '').length < 8) errors.push('Password must be at least 8 characters.');
  if (db.findOne('users', u => u.email.toLowerCase() === form.email)) errors.push('An account with this email already exists.');
  if (!req.body.agree) errors.push('Please agree to the Terms of Service.');
  if (errors.length) return res.render('auth/register', { title: 'Create account', form, flash: { error: errors, ok: [] } });
  const user = db.insert('users', { ...form, passwordHash: bcrypt.hashSync(req.body.password, 10), phone: '', status: 'active' });
  req.session.userId = user.id;
  req.flash('ok', 'Welcome to RoomStay.');
  res.redirect(homeFor(user));
});

router.post('/logout', (req, res) => req.session.destroy(() => res.redirect('/welcome')));

module.exports = router;
