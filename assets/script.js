(function () {
  document.querySelectorAll("[data-today]").forEach(function (node) {
    node.textContent = new Date().toLocaleDateString("en-US", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric"
    });
  });

  document.querySelectorAll("[data-project-filters]").forEach(function (bar) {
    var items = Array.prototype.slice.call(document.querySelectorAll(".project-list li[data-category]"));
    var status = document.querySelector("[data-filter-status]");
    var buttons = Array.prototype.slice.call(bar.querySelectorAll("button[data-filter]"));
    var valid = buttons.map(function (button) {
      return button.dataset.filter;
    });

    function applyFilter(filter, updateUrl) {
      var shown = 0;
      items.forEach(function (item) {
        var match = filter === "all" || item.dataset.category.split(" ").indexOf(filter) !== -1;
        item.hidden = !match;
        if (match) shown += 1;
      });
      buttons.forEach(function (button) {
        button.setAttribute("aria-pressed", button.dataset.filter === filter ? "true" : "false");
      });
      if (status) status.textContent = shown + (shown === 1 ? " project" : " projects");
      if (updateUrl) {
        var params = new URLSearchParams(window.location.search);
        if (filter === "all") params.delete("filter");
        else params.set("filter", filter);
        var query = params.toString();
        window.history.replaceState({}, "", window.location.pathname + (query ? "?" + query : ""));
      }
    }

    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        applyFilter(button.dataset.filter, true);
      });
    });

    var requested = new URLSearchParams(window.location.search).get("filter");
    applyFilter(valid.indexOf(requested) !== -1 ? requested : "all", false);
  });

  document.querySelectorAll('a[target="_blank"][href^="http"]').forEach(function (link) {
    link.addEventListener("click", function (event) {
      var opened = window.open(link.getAttribute("href"), "_blank", "noopener,noreferrer");
      if (opened) {
        event.preventDefault();
      }
    });
  });

  document.querySelectorAll("[data-contact-form]").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var name = form.elements.name ? form.elements.name.value.trim() : "";
      var email = form.elements.email ? form.elements.email.value.trim() : "";
      var message = form.elements.message ? form.elements.message.value.trim() : "";
      var body = ["Name: " + name, "Email: " + email, "", message].join("\n");
      var url =
        "https://mail.google.com/mail/?view=cm&fs=1&to=liancataytayjk%40gmail.com&su=" +
        encodeURIComponent("Portfolio inquiry") +
        "&body=" +
        encodeURIComponent(body);
      var opened = window.open(url, "_blank", "noopener,noreferrer");
      if (!opened) {
        window.location.href = url;
      }
    });
  });
})();
