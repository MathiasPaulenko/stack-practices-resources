// Observer pattern: a subject notifies subscribed observers on every event.
class Subject {
  constructor() {
    this.observers = new Set();
  }

  // Subscribe and return an unsubscribe function — call it in teardown.
  subscribe(fn) {
    this.observers.add(fn);
    return () => this.observers.delete(fn);
  }

  notify(data) {
    this.observers.forEach((fn) => {
      try {
        fn(data);
      } catch (err) {
        // one bad observer must not break the rest
        console.error(`Observer error: ${err.message}`);
      }
    });
  }
}

const subject = new Subject();
subject.subscribe((data) => console.log("A received:", data));
const unsubscribeB = subject.subscribe((data) => console.log("B received:", data));

subject.notify("Hello observers!");
unsubscribeB();
subject.notify("B is gone");
