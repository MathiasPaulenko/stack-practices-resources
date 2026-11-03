// Chain of Responsibility — Express/Koa-style compose() (runnable, no dependencies)
// Usage: node express-compose.js
//
// Same dispatch loop koa-compose uses: dispatch(i) runs middleware i and each
// next() resumes index i+1. The i <= index guard catches "double next" bugs.

function compose(middlewares) {
  return function run(req, finalNext) {
    let index = -1;

    function dispatch(i) {
      if (i <= index) throw new Error('next() called multiple times');
      index = i;
      const fn = i < middlewares.length ? middlewares[i] : finalNext;
      if (!fn) return;
      fn(req, () => dispatch(i + 1));
    }

    dispatch(0);
  };
}

const pipeline = compose([
  (req, next) => {
    req.trace = [];
    req.trace.push('auth');
    console.log('auth');
    next();
  },
  (req, next) => {
    req.trace.push('rate-limit');
    console.log('rate-limit');
    next();
  },
  (req, next) => {
    req.trace.push('logging');
    console.log('logging');
    next();
  },
]);

const req = { path: '/orders', method: 'POST' };
pipeline(req, () => console.log('endpoint reached, trace:', req.trace.join(' -> ')));

// Uncomment to see the double-next guard trigger:
// const buggy = compose([(r, n) => { n(); n(); }]);
// buggy({}, () => {});
