// Cancelable debounce with cancel() and flush() methods
function debounceCancelable(fn, delay) {
    let timeoutId;

    const debounced = function (...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => fn.apply(this, args), delay);
    };

    debounced.cancel = () => {
        clearTimeout(timeoutId);
        timeoutId = null;
    };

    debounced.flush = (...args) => {
        clearTimeout(timeoutId);
        fn.apply(this, args);
    };

    return debounced;
}

module.exports = { debounceCancelable };
