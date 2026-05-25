(function () {
  var storageKey = "lian-portfolio-theme";
  var root = document.documentElement;
  var body = document.body;
  var currentPage = body.dataset.page || "home";

  function storedTheme() {
    try {
      return localStorage.getItem(storageKey);
    } catch (error) {
      return null;
    }
  }

  function preferredTheme() {
    if (storedTheme()) return storedTheme();
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function applyTheme(theme) {
    var nextTheme = theme === "dark" ? "dark" : "light";
    root.dataset.theme = nextTheme;
    document.querySelectorAll("[data-theme-toggle]").forEach(function (button) {
      var targetTheme = nextTheme === "dark" ? "light" : "dark";
      button.setAttribute("aria-label", "Switch to " + targetTheme + " mode");
      button.setAttribute("title", "Switch to " + targetTheme + " mode");
      button.innerHTML =
        icon(nextTheme === "dark" ? "sun" : "moon") +
        '<span class="dock-label">Theme</span><span class="visually-hidden">Switch theme</span>';
    });
  }

  function saveTheme(theme) {
    try {
      localStorage.setItem(storageKey, theme);
    } catch (error) {
      // Some file:// browser contexts block localStorage; the visual toggle should still work.
    }
    applyTheme(theme);
  }

  function icon(name) {
    var icons = {
      home: '<path d="M3.5 10.7 12 4l8.5 6.7v8.2a1.6 1.6 0 0 1-1.6 1.6h-4.4v-5.3h-5v5.3H5.1a1.6 1.6 0 0 1-1.6-1.6v-8.2Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>',
      about: '<path d="M12 12.1a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm7 8.4a7 7 0 0 0-14 0" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>',
      projects: '<path d="M5 6.5h14M5 12h14M5 17.5h14" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>',
      contact: '<path d="M4.5 6.8h15v10.4h-15V6.8Zm0 .2 7.5 6 7.5-6" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>',
      moon: '<path d="M12 3.8a8.2 8.2 0 1 0 0 16.4 6.3 6.3 0 0 1 0-16.4Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>',
      sun: '<path d="M12 4v1.7m0 12.6V20m8-8h-1.7M5.7 12H4m13.7-5.7-1.2 1.2M7.5 16.5l-1.2 1.2m11.4 0-1.2-1.2M7.5 7.5 6.3 6.3M12 15.4a3.4 3.4 0 1 0 0-6.8 3.4 3.4 0 0 0 0 6.8Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>'
    };
    return '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none">' + icons[name] + "</svg>";
  }

  function dockMarkup(prefix) {
    var items = [
      ["home", "Home", prefix + "index.html"],
      ["about", "About", prefix + "about.html"],
      ["projects", "Projects", prefix + "projects.html"],
      ["contact", "Contact", prefix + "contact.html"]
    ];

    return (
      items
      .map(function (item) {
        var key = item[0];
        var label = item[1];
        var href = item[2];
        var isActive = currentPage === key || (currentPage === "project" && key === "projects");
        return (
          '<a class="dock-link' +
          (isActive ? " is-active" : "") +
          '" href="' +
          href +
          '" data-dock="' +
          key +
          '" aria-label="' +
          label +
          '"' +
          (isActive ? ' aria-current="page"' : "") +
          ">" +
          icon(key) +
          '<span class="dock-label">' +
          label +
          "</span></a>"
        );
      })
      .join("") +
      '<button class="dock-link theme-toggle" type="button" data-theme-toggle aria-label="Switch theme"></button>'
    );
  }

  document.querySelectorAll(".dock").forEach(function (dock) {
    var prefix = body.dataset.depth === "project" ? "../" : "";
    dock.innerHTML = dockMarkup(prefix);
  });

  applyTheme(preferredTheme());

  document.querySelectorAll("[data-marquee-track]").forEach(function (track) {
    if (track.dataset.cloned === "true") return;
    Array.prototype.slice.call(track.children).forEach(function (slide) {
      var clone = slide.cloneNode(true);
      clone.setAttribute("aria-hidden", "true");
      clone.querySelectorAll("img").forEach(function (image) {
        image.setAttribute("alt", "");
      });
      track.appendChild(clone);
    });
    track.dataset.cloned = "true";
  });

  document.querySelectorAll("[data-theme-toggle]").forEach(function (button) {
    button.addEventListener("click", function () {
      saveTheme(root.dataset.theme === "dark" ? "light" : "dark");
    });
  });

  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches && "IntersectionObserver" in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.14 }
    );

    document.querySelectorAll(".reveal").forEach(function (item) {
      observer.observe(item);
    });
  } else {
    document.querySelectorAll(".reveal").forEach(function (item) {
      item.classList.add("is-visible");
    });
  }
})();
