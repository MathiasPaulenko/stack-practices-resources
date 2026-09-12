// Practical: scroll progress with throttle
const { throttle } = require('./throttle');

const updateScrollProgress = throttle(() => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (scrollTop / docHeight) * 100;
    const bar = document.querySelector('.progress-bar');
    if (bar) bar.style.width = `${progress}%`;
}, 16);  // ~60fps

window.addEventListener('scroll', updateScrollProgress, { passive: true });
