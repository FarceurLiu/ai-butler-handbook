/* Progressive enhancement: the browser ties motion directly to scroll position. */
(() => {
  "use strict";
  if (!window.CSS || typeof window.CSS.supports !== "function") return;
  if (!window.CSS.supports("animation-timeline", "view(block)") ||
      !window.CSS.supports("animation-range", "entry 0% entry 100%")) return;
  document.documentElement.classList.add("scroll-motion");
})();
