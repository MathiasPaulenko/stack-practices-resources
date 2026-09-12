// Basic throttle — runs at most once per interval
function throttle(fn, interval) {
    let lastTime = 0;

    return function (...args) {
        const now = Date.now();
        if (now - lastTime >= interval) {
            fn.apply(this, args);
            lastTime = now;
        }
    };
}

module.exports = { throttle };
