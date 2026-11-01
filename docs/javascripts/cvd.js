// Color-vision deficiency preview for the palette and color pages.
//
// Replaces every <div class="cvd-toggle"></div> with buttons that recolor swatches and
// preview images through one SVG feColorMatrix filter. The matrices are Machado et al.
// (2009) at severity 1.0, applied in linear RGB (the SVG filter default), i.e. the same
// simulation as colorspacious / DaltonLens. Switching animates the matrix unless the
// user prefers reduced motion.
(() => {
  const IDENTITY = [1, 0, 0, 0, 1, 0, 0, 0, 1];
  const MODES = [
    { id: "normal", label: "Normal vision", matrix: IDENTITY },
    {
      id: "protan",
      label: "Protanopia",
      title: "No red cones (about 1 % of men)",
      matrix: [0.152286, 1.052583, -0.204868, 0.114503, 0.786281, 0.099216, -0.003882, -0.048116, 1.051998],
    },
    {
      id: "deutan",
      label: "Deuteranopia",
      title: "No green cones (about 1 % of men; milder forms affect about 5 %)",
      matrix: [0.367322, 0.860646, -0.227968, 0.280085, 0.672501, 0.047413, -0.01182, 0.04294, 0.968881],
    },
    {
      id: "tritan",
      label: "Tritanopia",
      title: "No blue cones (rare; this simulation is the least accurate)",
      matrix: [1.255528, -0.076749, -0.178779, -0.078411, 0.930809, 0.147602, 0.004733, 0.691367, 0.3039],
    },
    {
      id: "grey",
      label: "Greyscale",
      title: "Black-and-white print",
      matrix: [0.2126, 0.7152, 0.0722, 0.2126, 0.7152, 0.0722, 0.2126, 0.7152, 0.0722],
    },
  ];
  const DURATION = 400; // ms
  const STORAGE_KEY = "charite-plot-cvd";
  const ACTIVE_CLASS = "cvd-active";

  let current = IDENTITY.slice();
  let animation = 0;

  const toSvgValues = (m) => `${m[0]} ${m[1]} ${m[2]} 0 0 ${m[3]} ${m[4]} ${m[5]} 0 0 ${m[6]} ${m[7]} ${m[8]} 0 0 0 0 0 1 0`;
  const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2);
  const reducedMotion = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function ensureFilter() {
    let svg = document.getElementById("cvd-svg");
    if (!svg) {
      svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
      svg.id = "cvd-svg";
      svg.setAttribute("aria-hidden", "true");
      svg.setAttribute("width", "0");
      svg.setAttribute("height", "0");
      svg.style.position = "absolute";
      svg.innerHTML =
        '<filter id="cvd-filter" color-interpolation-filters="linearRGB">' +
        `<feColorMatrix type="matrix" values="${toSvgValues(current)}"/></filter>`;
      document.body.appendChild(svg);
    }
    return svg.querySelector("feColorMatrix");
  }

  function apply(matrix) {
    current = matrix;
    ensureFilter().setAttribute("values", toSvgValues(matrix));
  }

  function setMode(mode, animate) {
    const root = document.documentElement;
    const target = mode.matrix;
    cancelAnimationFrame(animation);
    for (const button of document.querySelectorAll(".cvd-toggle button")) {
      const pressed = button.dataset.mode === mode.id;
      button.setAttribute("aria-pressed", String(pressed));
      // On phones the buttons are one scrollable row: bring the selected one into view (horizontally only).
      const row = button.parentElement;
      if (pressed && row.scrollWidth > row.clientWidth) {
        row.scrollLeft = button.offsetLeft - row.offsetLeft - (row.clientWidth - button.offsetWidth) / 2;
      }
    }
    try {
      localStorage.setItem(STORAGE_KEY, mode.id);
    } catch {
      // Storage can be unavailable (private mode, blocked site data); the choice just isn't remembered.
    }

    const finish = () => {
      apply(target);
      // No filter at all for normal vision, so nothing is resampled unnecessarily.
      root.classList.toggle(ACTIVE_CLASS, mode.id !== "normal");
    };
    if (!animate || reducedMotion()) {
      finish();
      return;
    }
    root.classList.add(ACTIVE_CLASS);
    const start = current.slice();
    const t0 = performance.now();
    const step = (now) => {
      const t = Math.min((now - t0) / DURATION, 1);
      const k = ease(t);
      apply(start.map((v, i) => v + (target[i] - v) * k));
      if (t < 1) animation = requestAnimationFrame(step);
      else finish();
    };
    animation = requestAnimationFrame(step);
  }

  function init() {
    const placeholders = document.querySelectorAll(".cvd-toggle");
    if (!placeholders.length) {
      document.documentElement.classList.remove(ACTIVE_CLASS);
      return;
    }
    let saved = "normal";
    try {
      saved = localStorage.getItem(STORAGE_KEY) || "normal";
    } catch {
      // See setMode.
    }
    for (const placeholder of placeholders) {
      placeholder.setAttribute("role", "group");
      placeholder.setAttribute("aria-label", "Simulate color-vision deficiency");
      placeholder.replaceChildren(
        ...MODES.map((mode) => {
          const button = document.createElement("button");
          button.type = "button";
          button.dataset.mode = mode.id;
          button.textContent = mode.label;
          if (mode.title) button.title = mode.title;
          button.addEventListener("click", () => setMode(mode, true));
          return button;
        }),
      );
    }
    setMode(MODES.find((m) => m.id === saved) || MODES[0], false);
  }

  // Zensical / Material with instant navigation re-renders pages without a reload.
  if (window.document$) window.document$.subscribe(init);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
