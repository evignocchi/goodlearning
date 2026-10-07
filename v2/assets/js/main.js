(function () {
  "use strict";

  /* Where the contact forms post. Leave empty to open the visitor's mail client
     with the request prefilled (mailto fallback). Set to a form endpoint
     (for example a Formspree, Basin or own server URL) to send the request in the page. */
  var CONTACT_ENDPOINT = "";
  var CONTACT_EMAIL = "info@goodlearning.it";

  /* Mobile menu */
  var menuBtn = document.querySelector(".menu-btn");
  var menu = document.getElementById("menu");
  if (menuBtn && menu) {
    var setMenu = function (open) {
      menu.classList.toggle("is-open", open);
      menuBtn.setAttribute("aria-expanded", String(open));
      menuBtn.textContent = open ? "Chiudi" : "Menu";
    };
    menuBtn.addEventListener("click", function () {
      setMenu(menuBtn.getAttribute("aria-expanded") !== "true");
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) setMenu(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.classList.contains("is-open")) {
        setMenu(false);
        menuBtn.focus();
      }
    });
  }

  /* AI module selector: one tab selected, the others dimmed */
  var tabs = Array.prototype.slice.call(document.querySelectorAll(".ai__tab"));
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

  /* Contact forms */
  var forms = document.querySelectorAll("[data-contact-form]");
  Array.prototype.forEach.call(forms, function (form) {
    var status = form.querySelector(".form-status");
    var button = form.querySelector('button[type="submit"]');
    var say = function (text, state) {
      if (!status) return;
      status.textContent = text;
      status.dataset.state = state || "";
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        say("Controlla i campi evidenziati.", "error");
        return;
      }

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
          .catch(function () {
            say("Invio non riuscito. Scrivici a " + CONTACT_EMAIL + ".", "error");
          })
          .then(function () { button.disabled = false; });
        return;
      }

      var lines = [];
      data.forEach(function (value, key) {
        if (value) lines.push(key.charAt(0).toUpperCase() + key.slice(1) + ": " + value);
      });
      var href = "mailto:" + CONTACT_EMAIL +
        "?subject=" + encodeURIComponent("Richiesta di contatto dalla landing") +
        "&body=" + encodeURIComponent(lines.join("\n"));
      window.location.href = href;
      say("Si apre il tuo programma di posta con la richiesta pronta da inviare.", "ok");
    });
  });
})();
