// Mini: debounce utility (ES module)
// Usage (browser/Node with ESM):
// const debounced = debounce(fn, 200);
// debounced();
// debounced.cancel(); // discard a pending call
// debounced.flush();  // run a pending call immediately

export function debounce(fn, wait = 200) {
  if (typeof fn !== "function") {
    throw new TypeError("fn must be a function");
  }
  if (typeof wait !== "number") {
    throw new TypeError("wait must be a number");
  }
  if (!Number.isFinite(wait) || wait < 0) {
    throw new RangeError("wait must be a finite, non-negative number");
  }

  let timer = null;
  let lastArgs;
  let lastThis;
  let result;

  function invoke() {
    timer = null;
    const args = lastArgs;
    const thisArg = lastThis;
    lastArgs = undefined;
    lastThis = undefined;
    result = fn.apply(thisArg, args);
    return result;
  }

  function debounced(...args) {
    if (timer !== null) clearTimeout(timer);
    lastArgs = args;
    lastThis = this;
    timer = setTimeout(invoke, wait);
  }

  debounced.cancel = function () {
    if (timer !== null) clearTimeout(timer);
    timer = null;
    lastArgs = undefined;
    lastThis = undefined;
  };

  debounced.flush = function () {
    if (timer === null) return result;
    clearTimeout(timer);
    return invoke();
  };

  return debounced;
}
