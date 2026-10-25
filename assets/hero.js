/* Front-page plate: three schematic figures draw themselves in turn as the
   reader scrolls (find the pattern, ask what would have happened, decide
   where to act). The scrollcraft engine pins the plate and publishes its
   progress as --sc-p; this file reads that one number and moves one clip
   rectangle (the pen) across each panel. Under reduced motion every panel
   is shown complete. */
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
  var WINDOWS = [[0.06, 0.32], [0.34, 0.60], [0.62, 0.88]];
  var steps = Array.prototype.map.call(plate.querySelectorAll("[data-step]"), function (li, i) {
    var svg = li.querySelector("svg");
    return { li: li, pen: li.querySelector("[data-pen]"), width: svg.viewBox.baseVal.width, win: WINDOWS[i] };
  });

  function render(p) {
    var state = [];
    steps.forEach(function (s) {
      var d = Math.min(Math.max((p - s.win[0]) / (s.win[1] - s.win[0]), 0), 1);
      s.pen.setAttribute("width", (d * s.width).toFixed(1));
      s.li.classList.toggle("is-drawing", d > 0 && d < 1);
      s.li.classList.toggle("is-done", d >= 1);
      state.push(d.toFixed(3));
    });
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
