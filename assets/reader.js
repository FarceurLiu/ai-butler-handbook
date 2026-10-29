/* Reading feedback only: no storage, tracking, network calls or permissions. */
(() => {
  "use strict";
  const links = [...document.querySelectorAll(".toc-link")];
  const mobile = document.querySelector(".mobile-toc");
  const chapters = [...new Set(links.map(link => link.hash))]
    .map(hash => document.getElementById(decodeURIComponent(hash.slice(1))))
    .filter(Boolean);
  let scheduled = false;

  function update() {
    scheduled = false;
    const line = Math.min(160, window.innerHeight * 0.25);
    let current = null;
    for (const chapter of chapters) {
      if (chapter.getBoundingClientRect().top <= line) current = chapter.id;
      else break;
    }
    for (const link of links) {
      if (decodeURIComponent(link.hash.slice(1)) === current) {
        link.setAttribute("aria-current", "location");
      } else {
        link.removeAttribute("aria-current");
      }
    }
  }

  function schedule() {
    if (!scheduled) {
      scheduled = true;
      window.requestAnimationFrame(update);
    }
  }

  if (mobile) mobile.addEventListener("click", event => {
    const link = event.target.closest("a.toc-link");
    if (!link) return;
    // Close before the browser resolves the native anchor position. The link
    // still works without JS, and native navigation owns focus and history.
    mobile.open = false;
    schedule();
  });
  window.addEventListener("scroll", schedule, {passive: true});
  window.addEventListener("resize", schedule);
  window.addEventListener("hashchange", schedule);
  window.addEventListener("pageshow", schedule);
  window.addEventListener("load", schedule);
  schedule();
})();
