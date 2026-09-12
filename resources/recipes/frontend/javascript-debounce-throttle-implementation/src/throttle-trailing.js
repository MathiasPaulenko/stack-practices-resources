// Throttle with trailing edge — final call after activity stops
function throttleTrailing(fn, interval) {
    let lastTime = 0;
    let timeoutId;
    let lastArgs;

    return function (...args) {
        const now = Date.now();
        const remaining = interval - (now - lastTime);
        lastArgs = args;

        if (remaining <= 0) {
            clearTimeout(timeoutId);
            timeoutId = null;
            lastTime = now;
            fn.apply(this, args);
        } else if (!timeoutId) {
            timeoutId = setTimeout(() => {
                lastTime = Date.now();
                timeoutId = null;
                fn.apply(this, lastArgs);
            }, remaining);
        }
    };
}

module.exports = { throttleTrailing };
