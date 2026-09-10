// Small interactions only. No data, no backend.
document.addEventListener('click', function (e) {
  var fav = e.target.closest('[data-fav]');
  if (fav) { e.preventDefault(); fav.classList.toggle('on'); return; }
  var pill = e.target.closest('.pill');
  if (pill && pill.parentElement.classList.contains('pills')) {
    pill.parentElement.querySelectorAll('.pill').forEach(function (p) { p.classList.remove('on'); });
    pill.classList.add('on'); e.preventDefault(); return;
  }
  var tab = e.target.closest('.tabs > a');
  if (tab && tab.getAttribute('href') === '#') {
    tab.parentElement.querySelectorAll('a').forEach(function (t) { t.classList.remove('on'); });
    tab.classList.add('on'); e.preventDefault(); return;
  }
  var star = e.target.closest('.star-input b');
  if (star) {
    var all = Array.prototype.slice.call(star.parentElement.children), idx = all.indexOf(star);
    all.forEach(function (s, i) { s.classList.toggle('on', i <= idx); });
  }
  var seg = e.target.closest('.seg button');
  if (seg) { seg.parentElement.querySelectorAll('button').forEach(function (b) { b.classList.remove('on'); }); seg.classList.add('on'); e.preventDefault(); }
  var day = e.target.closest('.cal-grid button');
  if (day && !day.classList.contains('dim')) { day.parentElement.querySelectorAll('button').forEach(function (b) { b.classList.remove('on'); }); day.classList.add('on'); }
});
