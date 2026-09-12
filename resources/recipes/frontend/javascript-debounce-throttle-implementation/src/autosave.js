// Practical: autosave with debounce
const { debounceCancelable } = require('./debounce-cancelable');

class AutoSave {
    constructor(saveFn, delay = 2000) {
        this.save = debounceCancelable(saveFn, delay);
    }

    onChange(data) {
        this.save(data);
    }

    forceSave(data) {
        this.save.flush(data);
    }

    cancel() {
        this.save.cancel();
    }
}

module.exports = { AutoSave };
