/* ARS PERSICA — site.js (no dependencies, no network calls) */
(function(){
  "use strict";
  var root = document.documentElement;
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var RTL = root.dir === 'rtl';
  var CH = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  var DUR = 400;

  /* 1. DECODE LABELS — Latin scripts only (Arabic shaping must never be scrambled) */
  var labels = [].slice.call(document.querySelectorAll('.t'));
  labels.forEach(function(el){ el.dataset.text = el.textContent; });
  function reserve(){
    if (RTL) return;
    var w = [];
    labels.forEach(function(el){ el.style.width = ''; });
    labels.forEach(function(el){ w.push(el.getBoundingClientRect().width); });
    labels.forEach(function(el,i){ if (w[i]) el.style.width = (Math.ceil(w[i]*100)/100) + 'px'; });
  }
  function settle(el){
    if (el._raf){ cancelAnimationFrame(el._raf); el._raf = 0; }
    if (el._t){ clearTimeout(el._t); el._t = 0; }
    el.textContent = el.dataset.text;
  }
  function decode(el, dur){
    settle(el);
    if (RM || RTL) return;
    var text = el.dataset.text, n = text.length, D = dur || DUR;
    var t0 = performance.now(), lastRoll = 0, rand = new Array(n);
    function roll(){ for (var i=0;i<n;i++) rand[i] = CH.charAt((Math.random()*26)|0); }
    roll();
    function step(now){
      var p = Math.min(1, (now - t0) / D), front = p * n, out = '', i;
      if (now - lastRoll > 45){ roll(); lastRoll = now; }
      for (i = 0; i < n; i++){
        var c = text.charAt(i);
        if (i < front) out += c;
        else if (i < front + 3.6) out += (c === ' ' ? ' ' : rand[i]);
        else break;
      }
      el.textContent = out;
      if (p < 1) el._raf = requestAnimationFrame(step); else settle(el);
    }
    el._raf = requestAnimationFrame(step);
    el._t = setTimeout(function(){ settle(el); }, D + 500);
  }
  [].forEach.call(document.querySelectorAll('a, button'), function(el){
    var t = el.querySelector('.t'); if (!t) return;
    el.addEventListener('pointerenter', function(){ decode(t); });
  });

  /* 2. SCENE PARALLAX — mouse only, long ease, stops when settled */
  var bg = document.querySelector('.bg');
  var stage = document.querySelector('.stage');
  var tx = 0, ty = 0, cx = 0, cy = 0, running = false, heroVisible = true;
  function tick(){
    cx += (tx - cx) * 0.045; cy += (ty - cy) * 0.045;
    var w = innerWidth, h = innerHeight;
    var dx = -cx * w * 0.01, dy = -cy * h * 0.01;
    var sc = 1 + 2 * Math.max(Math.abs(dx) / w, Math.abs(dy) / h) + 0.014 * Math.max(0, cy);
    bg.style.transform = 'translate3d(' + dx.toFixed(2) + 'px,' + dy.toFixed(2) + 'px,0) scale(' + sc.toFixed(4) + ')';
    if (Math.abs(tx - cx) < 0.0004 && Math.abs(ty - cy) < 0.0004){ running = false; return; }
    requestAnimationFrame(tick);
  }
  function wake(){ if (!running && !RM && bg){ running = true; requestAnimationFrame(tick); } }
  addEventListener('pointermove', function(e){
    if (e.pointerType === 'touch' || !heroVisible) return;
    tx = (e.clientX / innerWidth) * 2 - 1; ty = (e.clientY / innerHeight) * 2 - 1; wake();
  }, {passive:true});
  document.addEventListener('pointerleave', function(){ tx = 0; ty = 0; wake(); });

  /* 3. CHAPTERS — each rail item has its own photograph, headline and paragraph */
  var dataEl = document.getElementById('chapters');
  var COPY = dataEl ? JSON.parse(dataEl.textContent) : {};
  var hero = document.querySelector('.hero');
  var rises = hero ? [].slice.call(hero.querySelectorAll('.hrise')) : [];
  var blurb = hero ? hero.querySelector('.blurb') : null;
  var scenes = [].slice.call(document.querySelectorAll('.bg figure'));
  var order = scenes.map(function(f){ return f.dataset.chapter; });
  var chapter = order[0], swapT = 0, autoT = 0, userTook = false;

  function load(fig){
    var img = fig.querySelector('img');
    if (img && img.dataset.srcset){ img.srcset = img.dataset.srcset; img.removeAttribute('data-srcset'); }
    return img;
  }
  function showScene(fig){
    var img = load(fig);
    function go(){
      if (fig.dataset.chapter !== chapter) return;
      scenes.forEach(function(o){ o.classList.toggle('on', o === fig); });
    }
    if (!img || (img.complete && img.naturalWidth)) go();
    else { img.addEventListener('load', go, {once:true}); img.addEventListener('error', go, {once:true}); }
  }
  var cur = document.querySelector('.dock .cur'), bar = document.querySelector('.dock .track i');
  function setRail(id){
    var i = order.indexOf(id);
    if (cur) cur.textContent = '0' + (i + 1);
    if (bar) bar.style.width = ((i + 1) / order.length * 100) + '%';
    [].forEach.call(document.querySelectorAll('.index li'), function(li){
      var a = li.querySelector('a'), on = a.getAttribute('href') === '#' + id;
      li.classList.toggle('on', on);
      if (on){ a.setAttribute('aria-current','true'); decode(a.querySelector('.t')); } else a.removeAttribute('aria-current');
    });
  }
  function showChapter(id){
    if (!COPY[id] || id === chapter) return;
    chapter = id; setRail(id);
    scenes.forEach(function(f){ if (f.dataset.chapter === id) showScene(f); });
    var c = COPY[id];
    clearTimeout(swapT);
    hero.classList.add('swapping');
    swapT = setTimeout(function(){
      rises[0].textContent = c.h[0]; rises[1].textContent = c.h[1];
      blurb.textContent = '';
      c.p.forEach(function(line, i){
        if (i) blurb.appendChild(document.createElement('br'));
        blurb.appendChild(document.createTextNode(i ? ' ' + line : line));
      });
      void hero.offsetWidth;
      hero.classList.remove('swapping');
    }, RM ? 0 : 500);
  }
  [].forEach.call(document.querySelectorAll('.index a'), function(a){
    a.addEventListener('click', function(e){
      e.preventDefault(); userTook = true; clearInterval(autoT);
      showChapter(a.getAttribute('href').slice(1));
    });
  });
  /* gentle auto-advance until the visitor takes over; paused off-screen and when the tab is hidden */
  function advance(){
    if (userTook || !heroVisible || document.hidden) return;
    var i = order.indexOf(chapter); showChapter(order[(i + 1) % order.length]);
  }
  if (!RM && order.length > 1){
    autoT = setInterval(advance, 8000);
    /* warm the next photograph once the page is idle */
    (window.requestIdleCallback || function(f){ setTimeout(f, 2500); })(function(){ if (scenes[1]) load(scenes[1]); });
  }

  /* 4. HEADER STATE + MENU */
  if ('IntersectionObserver' in window && stage){
    new IntersectionObserver(function(es){
      es.forEach(function(e){
        heroVisible = e.isIntersecting;
        root.classList.toggle('scrolled', e.intersectionRatio < 0.9);
      });
    }, {threshold:[0, 0.9, 1]}).observe(stage);
  }
  var menu = document.querySelector('.menu');
  var navset = document.getElementById('navset');
  if (menu && navset){
    var menuLabel = menu.querySelector('.t');
    var setMenu = function(open){
      root.classList.toggle('nav-open', open);
      menu.setAttribute('aria-expanded', String(open));
      menuLabel.dataset.text = open ? menu.dataset.close : menu.dataset.open;
      if (RTL) menuLabel.textContent = menuLabel.dataset.text; else decode(menuLabel);
      if (open) requestAnimationFrame(function(){ var f = navset.querySelector('a'); if (f) f.focus(); });
    };
    menu.addEventListener('click', function(e){ e.stopPropagation(); setMenu(!root.classList.contains('nav-open')); });
    navset.addEventListener('click', function(e){ if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && root.classList.contains('nav-open')){ setMenu(false); menu.focus(); } });
    document.addEventListener('click', function(e){ if (root.classList.contains('nav-open') && !navset.contains(e.target) && e.target !== menu) setMenu(false); });
    addEventListener('resize', function(){ if (innerWidth > 1040 && root.classList.contains('nav-open')) setMenu(false); });
  }

  /* 4b. GALLERY — filters and the story dialog */
  var chips = [].slice.call(document.querySelectorAll('.chip'));
  var crafts = [].slice.call(document.querySelectorAll('.craft'));
  chips.forEach(function(ch){
    ch.addEventListener('click', function(){
      var f = ch.dataset.filter;
      chips.forEach(function(c){ c.setAttribute('aria-pressed', String(c === ch)); });
      crafts.forEach(function(a){ var show = f === 'all' || a.dataset.cat === f; a.hidden = !show; if (show) a.classList.add('in'); });
    });
  });
  var dlg = document.getElementById('story');
  var curCraft = null;
  function visible(){ return crafts.filter(function(a){ return !a.hidden; }); }
  function openStory(a){
    if (!dlg) return;
    curCraft = a;
    var img = a.querySelector('.ph img'), di = dlg.querySelector('figure img');
    di.srcset = img.getAttribute('srcset'); di.sizes = '(max-width:1040px) 94vw, 46vw'; di.src = img.currentSrc || img.src; di.alt = img.alt;
    dlg.querySelector('#story-h').textContent = a.querySelector('h3').textContent;
    dlg.querySelector('.reg').textContent = a.querySelector('.reg').textContent;
    var body = dlg.querySelector('.story-body'); body.textContent = '';
    var p = document.createElement('p'); p.textContent = a.querySelector('.desc').textContent; body.appendChild(p);
    var h = a.querySelector('.hist'); body.appendChild(h.cloneNode(true)); body.lastChild.style.display = 'block';
    dlg.querySelector('.story-wa').href = a.dataset.wa;
    if (!dlg.open){ if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open',''); }
    dlg.querySelector('.story-tx').scrollTop = 0;
    if (history.replaceState) history.replaceState(null, '', '#' + a.id);
  }
  function step(d){ var v = visible(), i = v.indexOf(curCraft); if (i < 0) return; openStory(v[(i + d + v.length) % v.length]); }
  crafts.forEach(function(a){
    a.querySelector('.more').addEventListener('click', function(){ openStory(a); });
    a.querySelector('.ph').addEventListener('click', function(){ openStory(a); });
  });
  if (dlg){
    dlg.querySelector('.story-x').addEventListener('click', function(){ dlg.close(); });
    dlg.querySelector('.story-prev').addEventListener('click', function(){ step(-1); });
    dlg.querySelector('.story-next').addEventListener('click', function(){ step(1); });
    dlg.addEventListener('click', function(e){ if (e.target === dlg) dlg.close(); });
    dlg.addEventListener('keydown', function(e){ if (e.key === 'ArrowRight') step(RTL ? -1 : 1); if (e.key === 'ArrowLeft') step(RTL ? 1 : -1); });
    dlg.addEventListener('close', function(){ if (history.replaceState) history.replaceState(null, '', location.pathname + location.search); if (curCraft) curCraft.querySelector('.more').focus(); });
    var m = /^#craft-[a-z]+$/.test(location.hash) && document.querySelector(location.hash);
    if (m) setTimeout(function(){ openStory(m); }, 600);
  }

  /* 5. REVEAL ON SCROLL */
  var rv = [].slice.call(document.querySelectorAll('.rv'));
  if ('IntersectionObserver' in window && !RM){
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
    }, {rootMargin:'0px 0px -8% 0px', threshold:0.08});
    rv.forEach(function(el){ io.observe(el); });
  } else rv.forEach(function(el){ el.classList.add('in'); });

  /* remember the chosen language for the root page */
  [].forEach.call(document.querySelectorAll('[data-lang]'), function(a){
    a.addEventListener('click', function(){ try { localStorage.setItem('ap-lang', a.dataset.lang); } catch(e){} });
  });
  try { localStorage.setItem('ap-lang', root.lang); } catch(e){}

  /* 6. BOOT — reserve label widths once faces are ready, then one decode pass */
  function boot(){
    reserve();
    if (RM) return;
    function at(sel, t0, step){
      [].slice.call(document.querySelectorAll(sel)).forEach(function(el, i){ setTimeout(function(){ decode(el); }, t0 + i * (step || 0)); });
    }
    at('.visit .t', 330); at('.menu .t', 390); at('.links a .t', 360, 45);
    at('.index li.on .t', 660); at('.index li:not(.on) .t', 720, 55);
    at('.cta .t', 900); at('.dock .t', 1000, 60);
    setTimeout(function(){ root.classList.remove('anim'); }, 2200);
    setTimeout(function(){ labels.forEach(settle); }, 2600);
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(boot); else addEventListener('load', boot);
  var rt; addEventListener('resize', function(){ clearTimeout(rt); rt = setTimeout(reserve, 160); });
})();
