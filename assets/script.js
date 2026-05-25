(function () {
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var body = document.body;
  var dockLinks = Array.prototype.slice.call(document.querySelectorAll(".dock-link"));

  function setActiveDock(target) {
    dockLinks.forEach(function (link) {
      var isActive = link.getAttribute("data-dock") === target;
      link.classList.toggle("is-active", isActive);
      if (isActive) {
        link.setAttribute("aria-current", "page");
      } else {
        link.removeAttribute("aria-current");
      }
    });
  }

  if (body.dataset.page === "home") {
    var sections = Array.prototype.slice.call(document.querySelectorAll("[data-section]"));

    function syncDockToScroll() {
      var current = "home";
      var offset = window.innerHeight * 0.32;

      sections.forEach(function (section) {
        var rect = section.getBoundingClientRect();
        if (rect.top <= offset) {
          current = section.getAttribute("data-section");
        }
      });

      setActiveDock(current);
    }

    syncDockToScroll();
    window.addEventListener("scroll", syncDockToScroll, { passive: true });
    window.addEventListener("hashchange", function () {
      var hash = window.location.hash.replace("#", "");
      setActiveDock(hash || "home");
    });
  }

  if (!reduceMotion && "IntersectionObserver" in window) {
    var revealItems = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.16 }
    );

    revealItems.forEach(function (item) {
      observer.observe(item);
    });
  } else {
    document.querySelectorAll(".reveal").forEach(function (item) {
      item.classList.add("is-visible");
    });
  }
})();
