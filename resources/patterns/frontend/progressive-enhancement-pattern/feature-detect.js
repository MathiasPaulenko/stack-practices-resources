// feature-detect.js — check capabilities before enhancing.
// Each check is a capability test, not a browser sniff.
const features = {
  fetch: typeof fetch !== 'undefined',
  intersectionObserver: 'IntersectionObserver' in window,
  customElements: 'customElements' in window,
  serviceWorker: 'serviceWorker' in navigator,
};

window.peFeatures = features;
