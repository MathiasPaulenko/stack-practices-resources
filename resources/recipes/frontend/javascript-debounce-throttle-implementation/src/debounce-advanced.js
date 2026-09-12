// Debounce with leading and trailing edge options
function debounceAdvanced(fn, delay, { leading = false, trailing = true } = {}) {
    let timeoutId;
    let lastArgs;
    let invoked = false;

    return function (...args) {
        lastArgs = args;

        const shouldInvokeLeading = leading && !invoked;
        if (shouldInvokeLeading) {
            fn.apply(this, args);
            invoked = true;
        }

        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            if (trailing && (!leading || invoked)) {
                fn.apply(this, lastArgs);
            }
            invoked = false;
        }, delay);
    };
}

module.exports = { debounceAdvanced };
