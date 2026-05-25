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
    document.querySelectorAll("[data-theme-choice]").forEach(function (button) {
      var isActive = button.getAttribute("data-theme-choice") === nextTheme;
      button.classList.toggle("is-active", isActive);
      button.setAttribute("aria-pressed", String(isActive));
    });
  }

  function saveTheme(theme) {
    try {
      localStorage.setItem(storageKey, theme);
    } catch (error) {
      return;
    }
    applyTheme(theme);
  }

  function icon(name) {
    var icons = {
      home: '<path d="M3.5 10.7 12 4l8.5 6.7v8.2a1.6 1.6 0 0 1-1.6 1.6h-4.4v-5.3h-5v5.3H5.1a1.6 1.6 0 0 1-1.6-1.6v-8.2Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>',
      about: '<path d="M12 12.1a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm7 8.4a7 7 0 0 0-14 0" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>',
      projects: '<path d="M5 6.5h14M5 12h14M5 17.5h14" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>',
      contact: '<path d="M4.5 6.8h15v10.4h-15V6.8Zm0 .2 7.5 6 7.5-6" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>',
      theme: '<path d="M12 3.8a8.2 8.2 0 1 0 0 16.4 6.3 6.3 0 0 1 0-16.4Z" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>'
    };
    return '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none">' + icons[name] + "</svg>";
  }

  function dockMarkup(prefix) {
    var items = [
      ["home", "Home", prefix + "index.html"],
      ["about", "About", prefix + "about.html"],
      ["projects", "Projects", prefix + "projects.html"],
      ["contact", "Contact", prefix + "contact.html"],
      ["theme", "Theme", prefix + "theme.html"]
    ];

    return items
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
      .join("");
  }

  applyTheme(preferredTheme());

  document.querySelectorAll(".dock").forEach(function (dock) {
    var prefix = body.dataset.depth === "project" ? "../" : "";
    dock.innerHTML = dockMarkup(prefix);
  });

  document.querySelectorAll("[data-theme-choice]").forEach(function (button) {
    button.addEventListener("click", function () {
      saveTheme(button.getAttribute("data-theme-choice"));
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
