// P.A.U.L.I. mockup logic — vanilla JS, no network, state in memory + localStorage.
(function () {
  "use strict";

  var SCREENS = ["onboarding", "ask", "library", "digest", "doctor", "settings"];

  var EXAMPLES = {
    pem: {
      type: "answer",
      simple: "In your saved papers, hard effort and bad sleep link to PEM. Rest helps some people. Studies are small.",
      standard: "Across your saved papers, post-exertional malaise (crash after effort) is associated with prior exertion and poor sleep; pacing (planned rest around activity) is commonly reported as management. Evidence comes from small observational studies.",
      means: "What this means: big effort today can mean a crash later. Rest and sleep matter.",
      glossary: [["PEM", "crash after effort"], ["pacing", "planned rest around activity"]],
      cites: [["PMC1234567", "Smith et al. 2024"], ["PMC7654321", "Lee et al. 2023"]]
    },
    unknown: {
      type: "unknown",
      text: "I don't know from your saved papers — what is missing: trials of treatment X in ME/CFS; term to add: the drug name + “randomized trial”; what to ask your doctor: “Is there any evidence for X in people like me?”"
    },
    conflict: {
      type: "answer",
      simple: "Papers disagree here. One small study links low heart-rate-variability to PEM. One other study finds no link. Both are small.",
      standard: "Evidence is conflicting: one small cohort (n=42) reports reduced heart-rate variability before post-exertional malaise (crash after effort), while a second small cohort (n=35) finds no association. Both are observational and underpowered.",
      means: "What this means: science does not agree yet. Both sides are weak evidence.",
      glossary: [],
      cites: [["PMC1111111", "Garcia et al. 2022, yes-link"], ["PMC2222222", "Kim et al. 2023, no-link"]]
    },
    gated: { type: "gated", category: "prognosis / mortality" }
  };

  // ---------- Router ----------
  function currentScreen() {
    var h = location.hash.replace("#/", "");
    return SCREENS.indexOf(h) >= 0 ? h : "onboarding";
  }
  function render() {
    var s = currentScreen();
    SCREENS.forEach(function (name) {
      var el = document.getElementById("screen-" + name);
      if (el) el.hidden = name !== s;
    });
    document.querySelectorAll("[data-nav]").forEach(function (a) {
      var active = a.getAttribute("href") === "#/" + s;
      if (active) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    });
    var main = document.getElementById("main");
    if (main && document.activeElement && document.activeElement.blur) {
      var h1 = document.querySelector("#screen-" + s + " h1");
      if (h1) { h1.setAttribute("tabindex", "-1"); }
    }
  }
  window.addEventListener("hashchange", render);

  // ---------- Text size ----------
  var fontBtns = document.querySelectorAll("[data-font]");
  function setFont(pct, save) {
    document.documentElement.style.fontSize = pct === 100 ? "" : (pct / 100 * 100) + "%";
    document.documentElement.style.fontSize = pct + "%";
    if (pct === 100) document.documentElement.style.fontSize = "";
    fontBtns.forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-font") === String(pct)));
    });
    if (save !== false) { try { localStorage.setItem("pauli-font", String(pct)); } catch (e) {} }
  }
  fontBtns.forEach(function (b) {
    b.addEventListener("click", function () { setFont(Number(b.getAttribute("data-font"))); });
  });
  try {
    var savedFont = localStorage.getItem("pauli-font");
    if (savedFont) setFont(Number(savedFont), false);
  } catch (e) {}

  // ---------- Onboarding: buzzwords ----------
  var buzzwords = ["myalgic encephalomyelitis", "PEM"];
  var chipsEl = document.getElementById("buzz-chips");
  var countEl = document.getElementById("buzz-count");
  var resultsEl = document.getElementById("buzz-results");

  function renderChips() {
    chipsEl.innerHTML = "";
    buzzwords.forEach(function (w, i) {
      var li = document.createElement("li");
      li.append(document.createTextNode(w + " "));
      var rm = document.createElement("button");
      rm.type = "button";
      rm.className = "secondary";
      rm.textContent = "Remove";
      rm.setAttribute("aria-label", "Remove buzzword " + w);
      rm.addEventListener("click", function () { buzzwords.splice(i, 1); renderChips(); });
      li.append(rm);
      chipsEl.append(li);
    });
    countEl.textContent = buzzwords.length + " of 5 buzzwords.";
  }
  document.getElementById("buzz-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var input = document.getElementById("buzz-input");
    var v = input.value.trim();
    if (!v) return;
    if (buzzwords.length >= 5) { countEl.textContent = "Maximum 5 buzzwords. Remove one first."; return; }
    if (v.length < 2) { countEl.textContent = "Too short — use at least 2 characters."; return; }
    buzzwords.push(v);
    input.value = "";
    renderChips();
  });

  // Ollama cloud key toggle
  var ollamaRadios = document.querySelectorAll('input[name="ollama"]');
  ollamaRadios.forEach(function (r) {
    r.addEventListener("change", function () {
      document.getElementById("cloud-key-wrap").hidden =
        document.querySelector('input[name="ollama"]:checked').value !== "cloud";
    });
  });

  // Fake Europe PMC validation + fetch progress
  document.getElementById("buzz-check").addEventListener("click", function () {
    resultsEl.innerHTML = "";
    var items = buzzwords.map(function (w) {
      if (w.toLowerCase() === "fatigue") return { w: w, cls: "warn", t: w + ": too broad (>50k hits) — narrow it down, e.g. “fatigue + PEM”." };
      if (w.length < 3) return { w: w, cls: "warn", t: w + ": too short — add more letters." };
      return { w: w, cls: "ok", t: w + ": looks good — papers found." };
    });
    if (!items.length) {
      var li = document.createElement("li");
      li.className = "warn";
      li.textContent = "Add at least 1 buzzword first.";
      resultsEl.append(li);
      return;
    }
    items.forEach(function (it) {
      var li = document.createElement("li");
      li.className = it.cls;
      li.textContent = it.t;
      resultsEl.append(li);
    });
    // progress demo
    var wrap = document.getElementById("fetch-wrap");
    var bar = document.getElementById("fetch-bar");
    var fill = bar.querySelector("span");
    wrap.hidden = false;
    var p = 0;
    bar.setAttribute("aria-valuenow", "0");
    var t = setInterval(function () {
      p = Math.min(100, p + 20);
      fill.style.width = p + "%";
      bar.setAttribute("aria-valuenow", String(p));
      if (p >= 100) {
        clearInterval(t);
        document.getElementById("fetch-label").textContent = "Done — papers cached locally (demo).";
      }
    }, 300);
  });

  // ---------- Ask ----------
  // Single simplicity slider controls wording (no separate grade/mode toggle).
  var simplicity = document.getElementById("simplicity");
  var simplicityOut = document.getElementById("simplicity-out");
  function simplicityText(v) {
    return v <= 11 ? "very short sentences + glossary" : v <= 13 ? "short sentences + glossary" : "longer sentences, less glossary";
  }
  function isSimple() { return Number(simplicity.value) <= 13; }
  function updateModeNote() {
    document.getElementById("mode-note").textContent =
      "Simplicity " + simplicity.value + ": " + simplicityText(Number(simplicity.value)) + ".";
  }
  simplicity.addEventListener("input", function () {
    var v = Number(simplicity.value);
    simplicityOut.textContent = simplicityText(v);
    updateModeNote();
    var gl = document.getElementById("answer-glossary");
    if (!document.getElementById("answer-card").hidden && gl.dataset.full && lastAnswer) showAnswer(lastAnswer, true);
    var ga = document.getElementById("gate-answer");
    if (ga && !ga.hidden) {
      document.getElementById("gate-answer-text").textContent = isSimple() ? gateRevealedText.simple : gateRevealedText.standard;
    }
  });

  var answerCard = document.getElementById("answer-card");
  var gateCard = document.getElementById("gate-card");
  var lastAnswer = null;

  var gateRevealedText = {
    simple: "Some papers talk about how long people live with this illness. Numbers are small. No one can say what happens to you.",
    standard: "A small number of cohort studies report mortality outcomes in ME/CFS populations; estimates vary and samples are small, so individual prognosis cannot be inferred."
  };

  function showAnswer(ex, keepFocus) {
    gateCard.hidden = true;
    document.getElementById("gate-answer").hidden = true;
    answerCard.hidden = false;
    document.getElementById("answer-heading").textContent = "Answer (simplicity " + simplicity.value + ")";
    var text = isSimple() ? ex.simple : ex.standard;
    document.getElementById("answer-text").textContent = text;
    var means = document.getElementById("answer-means");
    var gl = document.getElementById("answer-glossary");
    if (isSimple()) {
      means.hidden = false;
      means.textContent = ex.means || "";
      gl.dataset.full = JSON.stringify(ex.glossary || []);
      reRenderGlossary();
      gl.hidden = !(ex.glossary && ex.glossary.length);
    } else {
      means.hidden = true;
      gl.hidden = true;
    }
    var cites = document.getElementById("answer-cites");
    cites.innerHTML = "";
    (ex.cites || []).forEach(function (c) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = "https://europepmc.org/articles/" + c[0];
      a.target = "_blank";
      a.rel = "noopener";
      a.textContent = "[" + c[0] + "] " + c[1];
      li.append(a);
      cites.append(li);
    });
    var unk = document.getElementById("answer-unknown");
    unk.hidden = true;
    lastAnswer = ex;
    if (!keepFocus) {
      answerCard.querySelector("h2").setAttribute("tabindex", "-1");
      answerCard.querySelector("h2").focus({ preventScroll: false });
    }
  }

  function reRenderGlossary() {
    var gl = document.getElementById("answer-glossary");
    var full = [];
    try { full = JSON.parse(gl.dataset.full || "[]"); } catch (e) {}
    var v = Number(simplicity.value);
    var showAll = v <= 13;
    gl.innerHTML = "";
    full.forEach(function (g) {
      var dt = document.createElement("dt"); dt.textContent = g[0];
      var dd = document.createElement("dd"); dd.textContent = "means “" + g[1] + "”";
      gl.append(dt, dd);
    });
    if (!showAll && full.length > 1) {
      while (gl.children.length > 2) gl.removeChild(gl.lastChild);
    }
  }

  function showUnknown(ex) {
    gateCard.hidden = true;
    answerCard.hidden = false;
    document.getElementById("answer-heading").textContent = "No answer in your papers";
    document.getElementById("answer-text").textContent = "No supporting paper was found above the threshold — so no guess.";
    document.getElementById("answer-means").hidden = true;
    document.getElementById("answer-glossary").hidden = true;
    document.getElementById("answer-cites").innerHTML = "";
    var unk = document.getElementById("answer-unknown");
    unk.hidden = false;
    unk.textContent = ex.text;
    lastAnswer = null;
  }

  function showGated(ex) {
    answerCard.hidden = true;
    gateCard.hidden = false;
    document.getElementById("gate-cat").textContent = ex.category;
    document.getElementById("gate-answer").hidden = true;
    document.getElementById("gate-blur").textContent = "Blurred preview — details stay hidden until you choose to show them.";
    var sens = document.querySelector('input[name="sensitivity"]:checked');
    var isHide = sens && sens.value === "hide";
    document.getElementById("gate-show").textContent = isHide ? "Show (confirm twice)" : "Show";
    document.getElementById("crisis-line").hidden = false;
    document.getElementById("gate-show").focus({ preventScroll: false });
  }

  var confirmCount = 0;
  document.getElementById("gate-show").addEventListener("click", function () {
    var sens = document.querySelector('input[name="sensitivity"]:checked');
    if (sens && sens.value === "hide") {
      confirmCount += 1;
      if (confirmCount < 2) {
        this.textContent = "Confirm again to show";
        return;
      }
    }
    confirmCount = 0;
    this.textContent = "Show";
    var ga = document.getElementById("gate-answer");
    ga.hidden = false;
    document.getElementById("gate-answer-text").textContent = isSimple() ? gateRevealedText.simple : gateRevealedText.standard;
    var cites = document.getElementById("gate-answer-cites");
    cites.innerHTML = "";
    [["PMC9999999", "Doe et al. 2021"]].forEach(function (c) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = "https://europepmc.org/articles/" + c[0];
      a.target = "_blank"; a.rel = "noopener";
      a.textContent = "[" + c[0] + "] " + c[1];
      li.append(a); cites.append(li);
    });
  });
  document.getElementById("gate-skip").addEventListener("click", function () {
    gateCard.hidden = true;
    document.getElementById("crisis-line").hidden = true;
  });
  document.getElementById("gate-why").addEventListener("click", function () {
    var t = document.getElementById("gate-why-text");
    var open = t.hidden;
    t.hidden = !open;
    this.setAttribute("aria-expanded", String(open));
  });

  function runExample(key) {
    var ex = EXAMPLES[key];
    if (!ex) return;
    if (ex.type === "unknown") showUnknown(ex);
    else if (ex.type === "gated") showGated(ex);
    else showAnswer(ex);
  }
  document.querySelectorAll("[data-example]").forEach(function (b) {
    b.addEventListener("click", function () { runExample(b.getAttribute("data-example")); });
  });
  document.getElementById("ask-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var q = document.getElementById("ask-input").value.trim().toLowerCase();
    if (!q) return;
    if (q.indexOf("cure") >= 0 || q.indexOf(" x ") >= 0) runExample("unknown");
    else if (q.indexOf("prognos") >= 0 || q.indexOf("die") >= 0 || q.indexOf("mortality") >= 0) runExample("gated");
    else if (q.indexOf("disagree") >= 0 || q.indexOf("conflict") >= 0) runExample("conflict");
    else runExample("pem");
    document.getElementById("sheet-q").textContent = document.getElementById("ask-input").value.trim();
  });

  // ---------- Library ----------
  var library = [
    { title: "What triggers PEM? — short answer + 2 papers", detail: "[PMC1234567] Smith et al. 2024 · [PMC7654321] Lee et al. 2023" }
  ];
  function renderLibrary() {
    var list = document.getElementById("library-list");
    list.innerHTML = "";
    document.getElementById("library-empty").hidden = library.length > 0;
    library.forEach(function (item, i) {
      var li = document.createElement("li");
      var strong = document.createElement("strong");
      strong.textContent = item.title;
      var p = document.createElement("p");
      p.textContent = item.detail;
      var rm = document.createElement("button");
      rm.type = "button"; rm.className = "secondary"; rm.textContent = "Remove";
      rm.setAttribute("aria-label", "Remove " + item.title);
      rm.addEventListener("click", function () { library.splice(i, 1); renderLibrary(); });
      li.append(strong, p, rm);
      list.append(li);
    });
  }
  document.getElementById("answer-save").addEventListener("click", function () {
    library.unshift({ title: "Saved answer (simplicity " + simplicity.value + ") — " + new Date().toISOString().slice(0, 10), detail: document.getElementById("answer-text").textContent.slice(0, 120) + "…" });
    renderLibrary();
    this.textContent = "Saved ✓";
    var btn = this;
    setTimeout(function () { btn.textContent = "Save for later"; }, 1500);
  });

  // ---------- Digest ----------
  document.getElementById("sync-btn").addEventListener("click", function () {
    var r = document.getElementById("sync-result");
    r.textContent = "Checking…";
    setTimeout(function () {
      r.textContent = "3 new papers since 2026-09-30.";
      document.getElementById("digest-text").textContent =
        "This week: 2 small studies on PEM triggers, 1 review on pacing. All Open Access. Save what matters for later.";
    }, 600);
  });

  // ---------- Settings sliders / print ----------
  var strict = document.getElementById("strictness");
  var strictOut = document.getElementById("strictness-out");
  strict.addEventListener("input", function () {
    var v = Number(strict.value);
    strictOut.textContent = v + " → threshold " + (v / 100 * 0.6).toFixed(2);
  });
  document.getElementById("print-btn").addEventListener("click", function () { window.print(); });

  // ---------- init ----------
  updateModeNote();
  renderChips();
  renderLibrary();
  render();
})();
