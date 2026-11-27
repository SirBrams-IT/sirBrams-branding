/* SirBrams Tech Solutions: site behaviour. No dependencies. */
(function () {
  'use strict';

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function store(op, key, val) {
    try {
      if (op === 'get') return window.localStorage.getItem(key);
      if (op === 'set') window.localStorage.setItem(key, val);
      if (op === 'sget') return window.sessionStorage.getItem(key);
      if (op === 'sset') window.sessionStorage.setItem(key, val);
    } catch (e) { /* storage can be blocked; the page still works */ }
    return null;
  }

  /* ---------- Toasts ---------- */
  var toastBox = $('#toasts');
  var icons = { success: 'bi-check-circle-fill', info: 'bi-info-circle-fill', error: 'bi-exclamation-circle-fill' };

  function toast(message, type) {
    if (!toastBox || !message) return;
    type = type || 'success';
    while (toastBox.children.length >= 3) toastBox.removeChild(toastBox.firstChild);

    var el = document.createElement('div');
    el.className = 'toast toast-' + type;
    el.setAttribute('role', type === 'error' ? 'alert' : 'status');
    el.innerHTML = '<i class="bi ' + (icons[type] || icons.info) + '"></i><p></p>' +
      '<button type="button" aria-label="Dismiss"><i class="bi bi-x-lg"></i></button>';
    el.querySelector('p').textContent = message;
    toastBox.appendChild(el);

    var timer;
    function close() {
      clearTimeout(timer);
      el.classList.add('is-leaving');
      setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 250);
    }
    function start() { timer = setTimeout(close, type === 'error' ? 7000 : 4500); }
    el.querySelector('button').addEventListener('click', close);
    el.addEventListener('mouseenter', function () { clearTimeout(timer); });
    el.addEventListener('mouseleave', start);
    start();
  }
  window.sbToast = toast;

  $$('#djangoMessages span').forEach(function (m) {
    toast(m.textContent.trim(), /error/.test(m.getAttribute('data-level') || '') ? 'error' : 'success');
  });

  /* ---------- Mobile navigation ---------- */
  var navToggle = $('#navToggle');
  var nav = $('#nav');
  function setNav(open) {
    document.body.classList.toggle('nav-open', open);
    navToggle.setAttribute('aria-expanded', String(open));
    navToggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    navToggle.firstElementChild.className = open ? 'bi bi-x-lg' : 'bi bi-list';
  }
  if (navToggle && nav) {
    navToggle.addEventListener('click', function () { setNav(!document.body.classList.contains('nav-open')); });
    $$('a', nav).forEach(function (a) { a.addEventListener('click', function () { setNav(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setNav(false); });
  }

  /* ---------- Header shadow ---------- */
  var header = $('#header');
  function onScroll() { if (header) header.classList.toggle('is-scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Copy to clipboard ---------- */
  $$('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-copy');
      function done() { toast('Email address copied: ' + text, 'success'); }
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done, function () { toast('Could not copy. Please select the address manually.', 'error'); });
      } else {
        var ta = document.createElement('textarea');
        ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
        document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); done(); } catch (e) { toast('Could not copy. Please select the address manually.', 'error'); }
        document.body.removeChild(ta);
      }
    });
  });

  /* ---------- Count-up numbers ----------
     The real value is already in the HTML, so the page never shows "0"
     if scripts are slow or blocked. We only animate when it is safe to. */
  var counters = $$('.count[data-target]');
  if (counters.length && 'IntersectionObserver' in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        io.unobserve(entry.target);
        var el = entry.target;
        var target = parseInt(el.getAttribute('data-target'), 10) || 0;
        var start = null, dur = 1400;
        function tick(ts) {
          if (start === null) start = ts;
          var p = Math.min((ts - start) / dur, 1);
          el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
          if (p < 1) requestAnimationFrame(tick); else el.textContent = target;
        }
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.4 });
    counters.forEach(function (el) { el.textContent = '0'; io.observe(el); });
  }

  /* ---------- Chat dialog ---------- */
  var chat = $('#chatDialog');
  var chatIntro = $('#chatIntro');
  var chatFormWrap = $('#chatFormWrap');
  var chatTitle = $('#chatTitle');
  var chatSub = $('#chatSub');
  var nudge = $('#chatNudge');

  function showIntro() {
    chatIntro.hidden = false; chatFormWrap.hidden = true;
    chatTitle.textContent = "Let's talk";
    chatSub.textContent = 'Have a question or need a digital solution?';
  }
  function showForm(subject) {
    chatIntro.hidden = true; chatFormWrap.hidden = false;
    chatTitle.textContent = 'Send us a message';
    chatSub.textContent = 'Tell us how we can help.';
    if (subject) { var s = $('#chat-subject'); if (s && !s.value) s.value = subject; }
    var first = $('#chat-name'); if (first) setTimeout(function () { first.focus(); }, 30);
  }
  function openChat(mode, subject) {
    if (!chat) return;
    if (nudge) nudge.hidden = true;
    if (mode === 'form') showForm(subject); else showIntro();
    if (!chat.open) chat.showModal();
  }
  window.openContactPopup = function (showFormFirst) { openChat(showFormFirst ? 'form' : 'intro'); };

  if (chat) {
    $('#chatLauncher').addEventListener('click', function () { openChat('intro'); });
    $('#chatShowForm').addEventListener('click', function () { showForm(); });
    $('#chatBack').addEventListener('click', showIntro);
    $$('[data-chat-close]', chat).forEach(function (b) { b.addEventListener('click', function () { chat.close(); }); });
    chat.addEventListener('click', function (e) { if (e.target === chat) chat.close(); });
  }
  $$('[data-open-chat]').forEach(function (b) {
    b.addEventListener('click', function () { openChat(b.getAttribute('data-open-chat'), b.getAttribute('data-subject')); });
  });

  // A quiet nudge once per visit instead of a pop-up that takes over the screen.
  if (nudge && !store('sget', 'sb-nudge')) {
    setTimeout(function () {
      if (chat && chat.open) return;
      nudge.hidden = false;
      store('sset', 'sb-nudge', '1');
      setTimeout(function () { nudge.hidden = true; }, 6500);
    }, 7000);
  }

  /* ---------- Form submit feedback ---------- */
  $$('form.form').forEach(function (form) {
    form.addEventListener('submit', function () {
      var btn = $('button[type="submit"]', form);
      if (btn) { btn.disabled = true; btn.setAttribute('aria-busy', 'true'); btn.firstChild.textContent = 'Sending '; }
      toast('Sending your message…', 'info');
    });
  });
  // Browsers may restore a disabled button when coming back to the page.
  window.addEventListener('pageshow', function () {
    $$('form.form button[type="submit"]').forEach(function (b) { b.disabled = false; b.removeAttribute('aria-busy'); });
  });

  /* ---------- Portfolio tabs ---------- */
  var tabs = $$('.tab');
  var blocks = $$('.pf-block');
  function applyFilter(name) {
    tabs.forEach(function (t) {
      var on = t.getAttribute('data-filter') === name;
      t.classList.toggle('is-active', on);
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
    });
    blocks.forEach(function (b) {
      var show = name === 'all' || b.getAttribute('data-cat') === name;
      b.hidden = !show;
      if (show) { b.classList.remove('is-in'); void b.offsetWidth; b.classList.add('is-in'); }
    });
  }

  if (tabs.length) {
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { applyFilter(t.getAttribute('data-filter')); });
      t.addEventListener('keydown', function (e) {
        var dir = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (!dir) return;
        e.preventDefault();
        var next = tabs[(i + dir + tabs.length) % tabs.length];
        next.focus(); next.click();
      });
    });
    var hash = (location.hash || '').replace('#', '');
    if (hash === 'design') applyFilter('design');
    else if (hash === 'websites') applyFilter('web');
    else applyFilter('all');
  }

  /* ---------- Design lightbox ---------- */
  var lb = $('#lightbox');
  var designs = $$('.design');
  var current = 0;

  function fillLightbox(i) {
    var d = designs[i]; if (!d) return;
    current = i;
    var img = $('#lbImg');
    img.src = d.getAttribute('data-src');
    img.alt = d.getAttribute('data-title');
    $('#lbType').textContent = d.getAttribute('data-type');
    $('#lbTitle').textContent = d.getAttribute('data-title');
    $('#lbBrief').textContent = d.getAttribute('data-brief');
    var notes = d.getAttribute('data-notes') || '';
    $('#lbNotes').textContent = notes;
    $('#lbNotesWrap').hidden = !notes.trim();
  }
  function step(dir) { fillLightbox((current + dir + designs.length) % designs.length); }

  if (lb && designs.length) {
    designs.forEach(function (d, i) {
      d.addEventListener('click', function () { fillLightbox(i); lb.showModal(); });
    });
    if (designs.length < 2) { $('#lbPrev').hidden = true; $('#lbNext').hidden = true; }
    $('#lbPrev').addEventListener('click', function () { step(-1); });
    $('#lbNext').addEventListener('click', function () { step(1); });
    $$('[data-lb-close]', lb).forEach(function (b) { b.addEventListener('click', function () { lb.close(); }); });
    lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
    lb.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') step(-1);
      if (e.key === 'ArrowRight') step(1);
    });
  }
})();
