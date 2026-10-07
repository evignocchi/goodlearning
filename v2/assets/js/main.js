(function () {
  "use strict";

  /* Where the contact forms post. Leave empty to open the visitor's mail client
     with the request prefilled (mailto fallback). Set it to a form endpoint
     (a Formspree, Basin or own server URL) to send the request from the page. */
  var CONTACT_ENDPOINT = "";
  var CONTACT_EMAIL = "info@goodlearning.it";

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Mobile menu */
  var menuBtn = $(".menu-btn");
  var menu = $("#menu");
  if (menuBtn && menu) {
    var setMenu = function (open) {
      menu.classList.toggle("is-open", open);
      menuBtn.setAttribute("aria-expanded", String(open));
      menuBtn.textContent = open ? "Chiudi" : "Menu";
    };
    menuBtn.addEventListener("click", function () { setMenu(menuBtn.getAttribute("aria-expanded") !== "true"); });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.classList.contains("is-open")) { setMenu(false); menuBtn.focus(); }
    });
  }

  /* Header gets a glass backing once the page scrolls */
  var header = $("[data-header]");
  if (header) {
    var onScroll = function () { header.classList.toggle("is-stuck", window.scrollY > 24); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* Dock: the contact action stays level in the corner once the first screen is gone,
     and steps aside when the contact section is on screen. */
  var dock = $("[data-dock]");
  if (dock) {
    var contact = $("#contatto");
    var contactVisible = false;
    var syncDock = function () { dock.classList.toggle("is-on", window.scrollY > 640 && !contactVisible); };
    if (contact && "IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) { contactVisible = entries[0].isIntersecting; syncDock(); }, { threshold: 0.05 }).observe(contact);
    }
    window.addEventListener("scroll", syncDock, { passive: true });
    syncDock();
  }

  /* Reveal on entry. Content is visible by default; this only adds the settle. */
  var revealables = $$("[data-reveal]");
  if (revealables.length && "IntersectionObserver" in window && !reduced) {
    document.documentElement.classList.add("has-reveal");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    revealables.forEach(function (el) { io.observe(el); });
  } else {
    revealables.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* Spine progress (linea): sets --p from 0 to 1 as the spine's section scrolls through */
  var spine = $("[data-spine]");
  if (spine) {
    var ticking = false;
    var update = function () {
      ticking = false;
      var r = spine.getBoundingClientRect();
      var vh = window.innerHeight;
      var p = (vh * 0.62 - r.top) / r.height;
      spine.style.setProperty("--p", Math.max(0, Math.min(1, p)).toFixed(4));
      $$("[data-station]", spine).forEach(function (st) {
        var y = st.getBoundingClientRect().top;
        st.classList.toggle("is-reached", y < vh * 0.62);
      });
    };
    var request = function () { if (!ticking) { ticking = true; window.requestAnimationFrame(update); } };
    if (reduced) {
      spine.style.setProperty("--p", "1");
      $$("[data-station]", spine).forEach(function (st) { st.classList.add("is-reached"); });
    } else {
      update();
      window.addEventListener("scroll", request, { passive: true });
      window.addEventListener("resize", request);
    }
  }

  /* Tabs (module selector): arrow keys, Home, End */
  $$("[role=tablist]").forEach(function (list) {
    var tabs = $$("[role=tab]", list);
    var select = function (tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        var panel = document.getElementById(t.getAttribute("aria-controls"));
        if (panel) panel.hidden = !on;
      });
      if (focus) tab.focus();
    };
    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () { select(tab, false); });
      tab.addEventListener("keydown", function (e) {
        var next = null;
        if (e.key === "ArrowDown" || e.key === "ArrowRight") next = tabs[(i + 1) % tabs.length];
        if (e.key === "ArrowUp" || e.key === "ArrowLeft") next = tabs[(i - 1 + tabs.length) % tabs.length];
        if (e.key === "Home") next = tabs[0];
        if (e.key === "End") next = tabs[tabs.length - 1];
        if (next) { e.preventDefault(); select(next, true); }
      });
    });
  });

  /* Contact forms */
  $$("[data-contact-form]").forEach(function (form) {
    var status = $(".form-status", form);
    var button = $('button[type="submit"]', form);
    var say = function (text, state) {
      if (!status) return;
      status.textContent = text;
      status.dataset.state = state || "";
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); say("Controlla i campi evidenziati.", "error"); return; }

      var data = new FormData(form);
      say("", "");

      if (CONTACT_ENDPOINT) {
        button.disabled = true;
        say("Invio in corso…", "");
        fetch(CONTACT_ENDPOINT, { method: "POST", body: data, headers: { Accept: "application/json" } })
          .then(function (res) {
            if (!res.ok) throw new Error("HTTP " + res.status);
            form.reset();
            say("Richiesta inviata. Ti rispondiamo presto.", "ok");
          })
          .catch(function () { say("Invio non riuscito. Scrivici a " + CONTACT_EMAIL + ".", "error"); })
          .then(function () { button.disabled = false; });
        return;
      }

      var lines = [];
      data.forEach(function (value, key) {
        if (value) lines.push(key.charAt(0).toUpperCase() + key.slice(1) + ": " + value);
      });
      window.location.href = "mailto:" + CONTACT_EMAIL +
        "?subject=" + encodeURIComponent("Richiesta di contatto dalla landing") +
        "&body=" + encodeURIComponent(lines.join("\n"));
      say("Si apre il tuo programma di posta con la richiesta pronta da inviare.", "ok");
    });
  });
})();
