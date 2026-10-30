/* Enhancement gates and CSS contract; real motion/layout is checked in-browser. */
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const source = fs.readFileSync(path.join(__dirname, "../assets/home.js"), "utf8");
const html = fs.readFileSync(path.join(__dirname, "../index.html"), "utf8");

function setup({css = true, supports = true, timeline = true, range = true} = {}) {
  const classes = new Set();
  const context = {
    document: {documentElement: {classList: {add(name) { classes.add(name); }}}},
    window: {},
  };
  if (css) context.window.CSS = {};
  if (css && supports) context.window.CSS.supports = (property, value) => {
    if (property === "animation-timeline") {
      assert.equal(value, "view(block)");
      return timeline;
    }
    assert.equal(property, "animation-range");
    assert.equal(value, "entry 0% entry 100%");
    return range;
  };
  vm.runInNewContext(source, context);
  return classes;
}

assert.ok(setup().has("scroll-motion"));
for (const options of [{css: false}, {supports: false}, {timeline: false}, {range: false}]) {
  assert.equal(setup(options).size, 0, "unsupported browsers stay static");
}
assert.match(html, /@media screen and \(prefers-reduced-motion:no-preference\)/);
assert.match(html, /\.scroll-motion \.takeaway-card\{animation:takeaway-enter 1ms linear backwards,takeaway-exit 1ms linear forwards;animation-timeline:view\(block\),view\(block\);animation-range:entry 0% entry 100%,exit 0% exit 100%\}/);
assert.match(html, /@keyframes takeaway-enter\{from\{transform:translate\(var\(--card-x\),var\(--card-y\)\) rotate\(var\(--card-angle\)\)\}to\{transform:none\}\}/);
assert.match(html, /@keyframes takeaway-exit\{from\{transform:none\}to\{transform:translate\(var\(--card-x\),calc\(-1 \* var\(--card-y\)\)\) rotate\(calc\(-1 \* var\(--card-angle\)\)\)\}\}/);
assert.match(html, /--card-x:0px;--card-y:72px;--card-angle:0deg/);
assert.doesNotMatch(html, /is-arriving|takeaway-arrive|--motion-card|--motion-ease/);
assert.doesNotMatch(source, /fetch\(|XMLHttpRequest|localStorage|sessionStorage|innerHTML|setInterval|setTimeout|requestAnimationFrame|IntersectionObserver|preventDefault|addEventListener/);
console.log("PASS: native scroll-linked entry/exit, stable reading interval, reversible position-only motion, unsupported API fallbacks, local-only enhancement");
