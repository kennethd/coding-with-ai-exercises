// Yotta Roots landing page — minimal vanilla JS.
// Smooth scrolling itself is handled by CSS (scroll-behavior + scroll-padding-top).
(function () {
  'use strict';

  var root = document.documentElement;
  var header = document.getElementById('site-header');
  var nav = document.getElementById('site-nav');
  var navToggle = document.getElementById('nav-toggle');

  /* ---------- Theme toggle (remembers choice) ---------- */
  function currentTheme() {
    if (root.dataset.theme) return root.dataset.theme;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  document.getElementById('theme-toggle').addEventListener('click', function () {
    var next = currentTheme() === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('yr-theme', next); } catch (e) {}
  });

  /* ---------- Mobile nav ---------- */
  function setNav(open) {
    nav.classList.toggle('open', open);
    navToggle.setAttribute('aria-expanded', String(open));
  }
  navToggle.addEventListener('click', function () {
    setNav(navToggle.getAttribute('aria-expanded') !== 'true');
  });
  // Close the menu after following any in-page link
  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href^="#"]');
    if (link && nav.classList.contains('open')) setNav(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') setNav(false);
  });

  /* ---------- Header border once scrolled ---------- */
  function onScroll() { header.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Highlight the nav link for the section in view ---------- */
  var navLinks = Array.prototype.slice.call(nav.querySelectorAll('ul a'));
  var sections = navLinks
    .map(function (a) { return document.querySelector(a.getAttribute('href')); })
    .filter(Boolean);

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navLinks.forEach(function (a) {
          a.classList.toggle('active', a.getAttribute('href') === '#' + entry.target.id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { observer.observe(s); });
  }

  /* ---------- Hero mock: live confidence slider ---------- */
  var slider = document.getElementById('hero-conf');
  var out = document.getElementById('hero-conf-out');
  var bornPill = document.querySelector('.modal .fact .pill');
  slider.addEventListener('input', function () {
    var v = Number(slider.value);
    out.textContent = v + '%';
    bornPill.textContent = v + '%';
    bornPill.className = 'pill ' + (v >= 80 ? 'pill-hi' : v > 40 ? 'pill-mid' : 'pill-lo');
  });

  /* ---------- Pricing buttons preselect the plan in the form ---------- */
  var planSelect = document.getElementById('join-plan');
  document.querySelectorAll('[data-plan]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (btn.getAttribute('href') === '#join') planSelect.value = btn.dataset.plan;
    });
  });

  /* ---------- Early-access form (prototype: nothing is sent) ---------- */
  var form = document.getElementById('join-form');
  var email = document.getElementById('join-email');
  var msg = document.getElementById('form-msg');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!email.value || !email.checkValidity()) {
      email.classList.add('invalid');
      msg.className = 'form-msg err';
      msg.textContent = 'Please enter a valid email address.';
      email.focus();
      return;
    }
    email.classList.remove('invalid');
    var planName = planSelect.options[planSelect.selectedIndex].text;
    msg.className = 'form-msg ok';
    msg.textContent = 'Thanks! You\'re on the list for ' + planName + '. (This is a preview page, so nothing was actually sent.)';
    form.reset();
  });

  /* ---------- Footer year ---------- */
  document.getElementById('year').textContent = new Date().getFullYear();
})();
