(function () {
  'use strict';
  var root = document.documentElement;

  /* ---- theme toggle: system by default, explicit choice wins and persists ---- */
  var toggle = document.querySelector('.nav__theme');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var current = root.dataset.theme;
      if (!current) {
        current = window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
      }
      var next = current === 'light' ? 'dark' : 'light';
      root.dataset.theme = next;
      try { localStorage.setItem('theme', next); } catch (e) {}
    });
  }

  /* ---- mobile menu ---- */
  var burger = document.querySelector('.nav__burger');
  var links = document.getElementById('nav-links');
  if (burger && links) {
    burger.addEventListener('click', function () {
      var open = links.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', String(open));
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        links.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---- assemble the address so scrapers reading raw HTML find nothing ---- */
  Array.prototype.forEach.call(document.querySelectorAll('.js-mail'), function (a) {
    var addr = a.dataset.u + String.fromCharCode(64) + a.dataset.d;
    a.href = 'mailto:' + addr + (a.dataset.s ? '?subject=' + encodeURIComponent(a.dataset.s) : '');
  });

  /* ---- portrait placeholder if the image is missing ---- */
  var shot = document.querySelector('.portrait img');
  if (shot) {
    var markEmpty = function () { shot.parentNode.classList.add('is-empty'); };
    shot.addEventListener('error', markEmpty);
    if (shot.complete && shot.naturalWidth === 0) markEmpty();
  }

  /* ---- highlight the section you are reading ---- */
  var navAnchors = Array.prototype.slice.call(document.querySelectorAll('.nav__links a[href^="#"]'));
  var sections = navAnchors
    .map(function (a) { return document.querySelector(a.getAttribute('href')); })
    .filter(Boolean);
  if (sections.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navAnchors.forEach(function (a) {
          a.toggleAttribute('aria-current', a.getAttribute('href') === '#' + entry.target.id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { io.observe(s); });
  }

  var year = document.querySelector('.js-year');
  if (year) year.textContent = String(new Date().getFullYear());

  /* ---- visitor counter ----
     One request to a small Worker on count.knez.dev. No cookie, nothing
     stored in the browser. The Worker counts each visitor once per day and
     ignores crawlers. Browsers sending Do Not Track / Global Privacy Control
     only read the number and are not counted. Headless browsers are skipped. */
  var visits = document.querySelector('.js-visits');
  if (visits && !navigator.webdriver) {
    var optedOut = navigator.doNotTrack === '1' || navigator.globalPrivacyControl === true;
    var base = 'https://count.knez.dev';
    var req = optedOut
      ? fetch(base + '/count', { mode: 'cors' })
      : fetch(base + '/hit', { method: 'POST', mode: 'cors', keepalive: true });
    req.then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        if (!d || typeof d.total !== 'number' || d.total < 1) return;
        visits.textContent = d.total.toLocaleString('en');
        visits.closest('.visits').hidden = false;
      })
      .catch(function () {});

    // no hover on touch screens: a tap on the copyright toggles it instead
    var who = document.querySelector('.foot__who');
    if (who && window.matchMedia('(hover: none)').matches) {
      who.addEventListener('click', function () { who.classList.toggle('is-shown'); });
    }
  }
})();
