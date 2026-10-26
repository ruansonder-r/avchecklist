(function () {
  "use strict";

  var STORAGE_KEY = "avchecklist.ticked";
  var LONG_PRESS_MS = 450;
  var MOVE_TOLERANCE = 10;   // px of drift before a press counts as a scroll

  var boxes = Array.prototype.slice.call(
    document.querySelectorAll('input[type="checkbox"][data-item-id]')
  );

  /* ---------------------------------------------------------------- ticks */

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

  /* -------------------------------------------------------- guidance pop-up
   *
   * Long-pressing an option that has guidance opens it; so does the ⓘ badge,
   * and a right-click on the desktop. The hard part is that an option is a
   * <label>, so the press that opens the pop-up would otherwise also tick the
   * box on the way out — hence swallowClick.
   */

  var dialog = document.getElementById("guidance");
  if (!dialog || typeof dialog.showModal !== "function") return;

  var titleEl = document.getElementById("guidance-title");
  var bodyEl = document.getElementById("guidance-body");

  var pressTimer = null;
  var pressRow = null;
  var pressX = 0;
  var pressY = 0;
  var swallowClick = false;
  var swallowTimer = null;
  var lastTrigger = null;

  // Keeps the fill animation on the row exactly as long as the press itself.
  document.documentElement.style.setProperty("--press-ms", LONG_PRESS_MS + "ms");

  function rowFor(target) {
    return target && target.closest ? target.closest(".row.has-guidance") : null;
  }

  function openGuidance(row, trigger) {
    var template = row.querySelector("template[data-guidance]");
    var text = row.querySelector(".text");
    if (!template || dialog.open) return;

    titleEl.textContent = text ? text.textContent.trim() : "";
    bodyEl.innerHTML = template.innerHTML;
    bodyEl.scrollTop = 0;
    lastTrigger = trigger || null;
    dialog.showModal();
  }

  function cancelPress() {
    if (pressTimer) {
      clearTimeout(pressTimer);
      pressTimer = null;
    }
    if (pressRow) {
      pressRow.classList.remove("is-pressing");
      pressRow = null;
    }
  }

  // Eat the click that the finishing long-press produces, wherever it lands —
  // on the option (which would tick it) or on the backdrop of the pop-up we
  // just opened (which would close it again).
  function swallowNextClick() {
    swallowClick = true;
    clearTimeout(swallowTimer);
    swallowTimer = setTimeout(function () { swallowClick = false; }, 700);
  }

  document.addEventListener("pointerdown", function (e) {
    if (e.button !== 0) return;                            // right-click has its own path
    if (e.target.closest && e.target.closest("[data-guidance-open]")) return;

    var row = rowFor(e.target);
    if (!row) return;

    cancelPress();
    pressRow = row;
    pressX = e.clientX;
    pressY = e.clientY;
    row.classList.add("is-pressing");

    pressTimer = setTimeout(function () {
      var target = pressRow;
      pressTimer = null;
      cancelPress();
      swallowNextClick();
      if (navigator.vibrate) {
        try { navigator.vibrate(12); } catch (err) { /* not allowed here */ }
      }
      openGuidance(target, target.querySelector("[data-guidance-open]"));
    }, LONG_PRESS_MS);
  });

  document.addEventListener("pointermove", function (e) {
    if (!pressRow) return;
    if (Math.abs(e.clientX - pressX) < MOVE_TOLERANCE &&
        Math.abs(e.clientY - pressY) < MOVE_TOLERANCE) return;
    cancelPress();                                          // they're scrolling
  });

  document.addEventListener("pointerup", cancelPress);
  document.addEventListener("pointercancel", cancelPress);
  window.addEventListener("scroll", cancelPress, { passive: true });

  document.addEventListener("click", function (e) {
    if (!swallowClick) return;
    swallowClick = false;
    e.preventDefault();
    e.stopPropagation();
  }, true);

  document.addEventListener("click", function (e) {
    var button = e.target.closest && e.target.closest("[data-guidance-open]");
    if (!button) return;
    e.preventDefault();
    var row = button.closest(".row");
    if (row) openGuidance(row, button);
  });

  // Also stops the mobile text-selection menu hijacking the long press.
  document.addEventListener("contextmenu", function (e) {
    var row = rowFor(e.target);
    if (!row) return;
    e.preventDefault();
    cancelPress();
    openGuidance(row, row.querySelector("[data-guidance-open]"));
  });

  dialog.addEventListener("click", function (e) {
    var onBackdrop = e.target === dialog;
    if (onBackdrop || (e.target.closest && e.target.closest("[data-guidance-close]"))) {
      dialog.close();
    }
  });

  dialog.addEventListener("close", function () {
    bodyEl.innerHTML = "";
    if (lastTrigger && document.contains(lastTrigger)) lastTrigger.focus();
    lastTrigger = null;
  });
})();
