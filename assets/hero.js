/* Front-page plate: the CARP chart draws itself as the reader scrolls.
   The scrollcraft engine pins the plate and publishes its progress as --sc-p;
   this file reads that one number. One clip rectangle (the pen) reveals both
   lines and the hatched post-1988 gap up to the same year, and the ledger
   reads the real values at the pen. Under reduced motion the chart is shown
   complete. */
(function () {
  var main = document.getElementById("main");
  var plate = document.querySelector(".plate");
  var svg = plate && plate.querySelector("[data-proof]");
  if (!main || !plate || !svg) return;

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (window.ScrollCraft && !reduce) {
    window.ScrollCraft.mount(main);
  } else {
    // Static plate: no pinned scroll. Mark the page ready the way the engine would.
    plate.classList.add("plate--static");
    document.documentElement.classList.add("sc-ready");
  }

  var nums = function (name) { return svg.getAttribute(name).split(",").map(Number); };
  var years = nums("data-years");
  var ph = nums("data-ph");
  var synth = nums("data-synth");
  var phLine = svg.querySelector("[data-proof-line]");
  var pen = svg.querySelector("[data-proof-pen]");
  var dot = svg.querySelector("[data-proof-dot]");
  var ledger = {
    year: plate.querySelector("[data-ledger-year]"),
    ph: plate.querySelector("[data-ledger-ph]"),
    synth: plate.querySelector("[data-ledger-synth]"),
    gap: plate.querySelector("[data-ledger-gap]")
  };
  var archive = plate.querySelectorAll(".clip");
  var average = (function () {
    var sum = 0, n = 0;
    years.forEach(function (y, i) { if (y >= 1989) { sum += ph[i] / synth[i] - 1; n++; } });
    return (sum / n) * 100;
  })();

  var pts = phLine.getAttribute("points").trim().split(/\s+/).map(function (p) { return p.split(",").map(Number); });
  var right = svg.viewBox.baseVal.width;

  // Position on the Philippines line at a fractional year index.
  function at(t) {
    var i = Math.min(Math.floor(t), pts.length - 2);
    var f = t - i;
    return { x: pts[i][0] + f * (pts[i + 1][0] - pts[i][0]), y: pts[i][1] + f * (pts[i + 1][1] - pts[i][1]) };
  }

  var fmt = function (v) { return Math.round(v).toLocaleString("en-US"); };
  var smooth = function (x) { x = Math.min(Math.max(x, 0), 1); return x * x * (3 - 2 * x); };
  var last = -1;

  function render(p) {
    // Peak: the pen runs from 10% to 86% of the plate's scroll.
    var draw = Math.min(Math.max((p - 0.1) / 0.76, 0), 1);
    var t = draw * (years.length - 1);
    var head = at(t);
    pen.setAttribute("width", (draw >= 1 ? right : head.x).toFixed(1));
    dot.setAttribute("cx", head.x.toFixed(1));
    dot.setAttribute("cy", head.y.toFixed(1));
    dot.style.opacity = draw > 0 && draw < 1 ? 1 : 0;

    var i = Math.round(t);
    if (draw >= 1) {
      ledger.year.textContent = "1989 to 2008";
      ledger.ph.textContent = "";
      ledger.synth.textContent = "";
      ledger.gap.textContent = "Average gap " + average.toFixed(1) + "%";
    } else if (i !== last) {
      var gap = (ph[i] / synth[i] - 1) * 100;
      ledger.year.textContent = years[i];
      ledger.ph.textContent = "Philippines " + fmt(ph[i]);
      ledger.synth.textContent = "Synthetic " + fmt(synth[i]);
      ledger.gap.textContent = "Gap " + (gap > 0 ? "+" : "") + gap.toFixed(1) + "%";
    }
    last = draw >= 1 ? -1 : i;
    ledger.gap.classList.toggle("is-after", years[i] > 1988 || draw >= 1);

    // Archive plane: the clippings fan out from behind the portrait early in the act.
    var fan = smooth(p / 0.3);
    for (var c = 0; c < archive.length; c++) archive[c].style.setProperty("--fan", fan.toFixed(4));

    // Tell the scroll-craft verification harness what is visibly drawn (see its verify.md).
    plate.setAttribute("data-sc-verify-state", draw.toFixed(3) + "|" + ledger.year.textContent + "|" + fan.toFixed(3));
  }

  if (reduce || !window.ScrollCraft) {
    render(1);
    return;
  }

  var running = false;
  function frame() {
    var p = parseFloat(plate.style.getPropertyValue("--sc-p")) || 0;
    render(p);
    if (running) requestAnimationFrame(frame);
  }
  // Only animate while the plate is on screen.
  new IntersectionObserver(function (entries) {
    var visible = entries[0].isIntersecting;
    if (visible && !running) { running = true; requestAnimationFrame(frame); }
    running = visible;
  }).observe(plate);
  render(0);
})();
