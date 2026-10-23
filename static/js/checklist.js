(function () {
  "use strict";

  var STORAGE_KEY = "avchecklist.ticked";
  var boxes = Array.prototype.slice.call(
    document.querySelectorAll('input[type="checkbox"][data-item-id]')
  );

  function loadTicked() {
    try {
      var raw = window.localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (err) {
      return [];
    }
  }

  function saveTicked(ids) {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(ids));
    } catch (err) {
      /* private browsing / storage disabled — ticks just won't survive a reload */
    }
  }

  function persist() {
    saveTicked(
      boxes.filter(function (b) { return b.checked; })
           .map(function (b) { return b.dataset.itemId; })
    );
  }

  function render() {
    var done = 0;
    document.querySelectorAll("[data-section]").forEach(function (section) {
      var inputs = section.querySelectorAll('input[type="checkbox"]');
      var ticked = section.querySelectorAll('input[type="checkbox"]:checked');
      var label = section.querySelector("[data-count]");
      if (label) {
        label.textContent = inputs.length
          ? ticked.length + " / " + inputs.length
          : "";
      }
      done += ticked.length;
    });

    var overall = document.getElementById("overall-progress");
    if (overall) {
      overall.textContent = boxes.length
        ? done + " of " + boxes.length + " ticked"
        : "";
    }
  }

  var ticked = loadTicked();
  boxes.forEach(function (box) {
    box.checked = ticked.indexOf(box.dataset.itemId) !== -1;
    box.addEventListener("change", function () {
      persist();
      render();
    });
  });

  var clearButton = document.getElementById("clear-all");
  if (clearButton) {
    clearButton.addEventListener("click", function () {
      boxes.forEach(function (box) { box.checked = false; });
      persist();
      render();
    });
  }

  render();
})();
