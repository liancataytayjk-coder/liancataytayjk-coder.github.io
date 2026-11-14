/* Front-page plate: three schematic figures build themselves in turn as the
   reader scrolls. 1: the dots appear, then the trend line draws. 2: the two
   lines draw, then the gap between them fills and is labelled. 3: the bars
   rise one by one, then the threshold appears and the bars above it fill.
   The scrollcraft engine pins the plate and publishes its progress as --sc-p;
   this file reads that one number. Under reduced motion every panel is shown
   complete. */
(function () {
  var main = document.getElementById("main");
  var plate = document.querySelector(".plate");
  if (!main || !plate) return;

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (window.ScrollCraft && !reduce) {
    window.ScrollCraft.mount(main);
  } else {
    // Static plate: no pinned scroll. Mark the page ready the way the engine would.
    plate.classList.add("plate--static");
    document.documentElement.classList.add("sc-ready");
  }

  // Each step owns a slice of the plate's scroll, back to back.
  var WINDOWS = [[0.04, 0.32], [0.36, 0.64], [0.68, 0.96]];

  function clamp(v) { return Math.min(Math.max(v, 0), 1); }
  function span(d, a, b) { return clamp((d - a) / (b - a)); }
  function all(root, sel) { return Array.prototype.slice.call(root.querySelectorAll(sel)); }

  var steps = all(plate, "[data-step]").map(function (li, i) {
    var svg = li.querySelector("svg");
    return {
      li: li,
      win: WINDOWS[i],
      width: svg.viewBox.baseVal.width,
      dots: all(svg, ".dot"),
      draw: svg.querySelector("[data-draw]"),
      pen: svg.querySelector("[data-pen]"),
      reveal: all(svg, "[data-reveal]"),
      bars: all(svg, "[data-bar]")
    };
  });

  function paint(s, d) {
    // 1. Dots appear left to right, then the trend line draws across them.
    s.dots.forEach(function (dot) {
      dot.style.opacity = span(d, 0, 0.55) >= parseFloat(dot.getAttribute("data-x")) ? 1 : 0;
    });
    if (s.draw) s.draw.style.strokeDashoffset = (1 - span(d, 0.5, 0.85)).toFixed(3);
    // 2. Both lines draw behind a moving clip.
    if (s.pen) s.pen.setAttribute("width", (span(d, 0, 0.6) * s.width).toFixed(1));
    // 3. Bars rise one after another.
    var n = s.bars.length;
    s.bars.forEach(function (bar, i) {
      var g = span(d, (i / n) * 0.6, ((i + 1) / n) * 0.6);
      bar.style.transform = "scaleY(" + g.toFixed(3) + ")";
      bar.classList.toggle("is-act", bar.hasAttribute("data-act") && d >= 0.9);
    });
    // The answer (trend label, effect, threshold) arrives last.
    var r = span(d, s.bars.length ? 0.65 : 0.7, s.bars.length ? 0.85 : 0.9);
    s.reveal.forEach(function (el) { el.style.opacity = r.toFixed(3); });
  }

  function render(p) {
    var state = [], current = 0;
    steps.forEach(function (s, i) {
      var d = clamp((p - s.win[0]) / (s.win[1] - s.win[0]));
      paint(s, d);
      s.li.classList.toggle("is-drawing", d > 0 && d < 1);
      s.li.classList.toggle("is-done", d >= 1);
      if (p >= s.win[0] - 0.02) current = i;
      state.push(d.toFixed(3));
    });
    // On phones only the current panel is shown.
    steps.forEach(function (s, i) { s.li.classList.toggle("is-current", i === current); });
    // Tell the scroll-craft verification harness what is visibly drawn (see its verify.md).
    plate.setAttribute("data-sc-verify-state", state.join("|"));
  }

  if (reduce || !window.ScrollCraft) {
    render(1);
    return;
  }

  var running = false;
  function frame() {
    render(parseFloat(plate.style.getPropertyValue("--sc-p")) || 0);
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
