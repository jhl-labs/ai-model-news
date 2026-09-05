/* AI Model News — theme toggle + client-side filtering (no dependencies) */
(function () {
  "use strict";

  /* ---------- Theme ---------- */
  var root = document.documentElement;
  var toggle = document.getElementById("theme-toggle");

  function currentTheme() {
    var explicit = root.getAttribute("data-theme");
    if (explicit === "light" || explicit === "dark") return explicit;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) { /* storage unavailable */ }
      toggle.setAttribute("aria-label", next === "dark" ? "라이트 테마로 전환" : "다크 테마로 전환");
    });
    toggle.setAttribute("aria-label", currentTheme() === "dark" ? "라이트 테마로 전환" : "다크 테마로 전환");
  }

  /* ---------- Filters (index page only) ---------- */
  var cardsRoot = document.getElementById("cards");
  var filters = document.getElementById("filters");
  if (!cardsRoot || !filters) return;

  var cards = Array.prototype.slice.call(cardsRoot.querySelectorAll(".card"));
  var chips = Array.prototype.slice.call(filters.querySelectorAll(".chip"));
  var orgSelect = document.getElementById("org-filter");
  var searchInput = document.getElementById("search");
  var resetBtn = document.getElementById("reset-filters");
  var noMatch = document.getElementById("no-match");
  var visibleStat = document.getElementById("stat-visible");

  var state = { task: "", org: "", q: "" };

  function readHash() {
    var hash = window.location.hash.replace(/^#/, "");
    var next = { task: "", org: "", q: "" };
    if (hash) {
      hash.split("&").forEach(function (pair) {
        var idx = pair.indexOf("=");
        var key = idx >= 0 ? pair.slice(0, idx) : pair;
        var val = idx >= 0 ? pair.slice(idx + 1) : "";
        try { val = decodeURIComponent(val.replace(/\+/g, " ")); } catch (e) { /* keep raw */ }
        if (key === "task" || key === "org" || key === "q") next[key] = val;
      });
    }
    return next;
  }

  function writeHash() {
    var parts = [];
    if (state.task) parts.push("task=" + encodeURIComponent(state.task));
    if (state.org) parts.push("org=" + encodeURIComponent(state.org));
    if (state.q) parts.push("q=" + encodeURIComponent(state.q));
    var next = parts.length ? "#" + parts.join("&") : "";
    if (next !== window.location.hash) {
      var url = window.location.pathname + window.location.search + next;
      if (window.history && window.history.replaceState) {
        window.history.replaceState(null, "", url);
      } else {
        window.location.hash = next;
      }
    }
  }

  function syncControls() {
    chips.forEach(function (chip) {
      var active = (chip.getAttribute("data-task") || "") === state.task;
      chip.classList.toggle("is-active", active);
      chip.setAttribute("aria-pressed", active ? "true" : "false");
    });
    if (orgSelect && orgSelect.value !== state.org) {
      orgSelect.value = state.org;
      if (orgSelect.value !== state.org) { state.org = ""; orgSelect.value = ""; }
    }
    if (searchInput && searchInput.value !== state.q) searchInput.value = state.q;
  }

  function apply() {
    var q = state.q.trim().toLowerCase();
    var shown = 0;
    cards.forEach(function (card) {
      var ok = true;
      if (state.task && card.getAttribute("data-task") !== state.task) ok = false;
      if (ok && state.org && card.getAttribute("data-org") !== state.org) ok = false;
      if (ok && q && (card.getAttribute("data-search") || "").indexOf(q) === -1) ok = false;
      card.hidden = !ok;
      if (ok) shown++;
    });
    if (noMatch) noMatch.hidden = !(cards.length > 0 && shown === 0);
    if (visibleStat) visibleStat.textContent = String(shown);
  }

  function update() {
    syncControls();
    apply();
    writeHash();
  }

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      state.task = chip.getAttribute("data-task") || "";
      update();
    });
  });
  if (orgSelect) {
    orgSelect.addEventListener("change", function () { state.org = orgSelect.value; update(); });
  }
  if (searchInput) {
    var timer = null;
    searchInput.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(function () { state.q = searchInput.value; update(); }, 120);
    });
  }
  if (resetBtn) {
    resetBtn.addEventListener("click", function () {
      state = { task: "", org: "", q: "" };
      update();
      if (searchInput) searchInput.focus();
    });
  }
  window.addEventListener("hashchange", function () {
    state = readHash();
    syncControls();
    apply();
  });

  state = readHash();
  syncControls();
  apply();
})();
