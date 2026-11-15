// Shared IntersectionObserver for the demo and for reuse.
// rootMargin starts the fetch before the element hits the viewport;
// unobserve() stops repeat work once the image has loaded.

const counter = document.getElementById('counter');
let fetched = 0;

const imageObserver = new IntersectionObserver((entries, observer) => {
  for (const entry of entries) {
    if (!entry.isIntersecting) continue;

    const img = entry.target;
    img.onerror = () => {
      // Fail visibly: swap in a placeholder instead of leaving a blank.
      img.src = 'images/fallback.svg';
      img.alt = 'Image failed to load';
    };
    img.src = img.dataset.src;
    img.removeAttribute('data-src');
    observer.unobserve(img);

    fetched += 1;
    if (counter) counter.textContent = `fetched: ${fetched}`;
  }
}, {
  rootMargin: '200px 0px', // start loading ~200px before the edge
  threshold: 0.01,
});

document.querySelectorAll('img[data-src]').forEach((img) => {
  imageObserver.observe(img);
});
