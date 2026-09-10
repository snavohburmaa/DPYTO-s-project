// Route guards.
function requireLogin(req, res, next) {
  if (!req.user) { req.session.returnTo = req.originalUrl; req.flash('error', 'Please log in first.'); return res.redirect('/login'); }
  next();
}
function requireRole(...roles) {
  return (req, res, next) => {
    if (!req.user) { req.session.returnTo = req.originalUrl; req.flash('error', 'Please log in first.'); return res.redirect('/login'); }
    if (!roles.includes(req.user.role)) return res.status(403).render('error', { title: 'Access denied', message: `This page is only for ${roles.join(' or ')} accounts.`, code: 403 });
    next();
  };
}
function homeFor(user) {
  if (!user) return '/welcome';
  return { renter: '/home', owner: '/owner', admin: '/admin' }[user.role] || '/home';
}
module.exports = { requireLogin, requireRole, homeFor };
