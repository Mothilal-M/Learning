import assert from "node:assert/strict";
import { setTimeout as delay } from "node:timers/promises";
import test from "node:test";

import { debounce } from "./0003-js_debounce.js";

test("debounce invokes only the latest call after the wait", async () => {
  const calls = [];
  const run = debounce((value) => calls.push(value), 15);

  run("first");
  run("latest");
  await delay(40);

  assert.deepEqual(calls, ["latest"]);
});

test("debounce preserves this and the latest arguments", async () => {
  let actual;
  const receiver = {
    prefix: "hello",
    run: debounce(function (suffix) {
      actual = `${this.prefix}${suffix}`;
    }, 5),
  };

  receiver.run("!");
  await delay(25);

  assert.equal(actual, "hello!");
});

test("cancel discards a pending call", async () => {
  let calls = 0;
  const run = debounce(() => calls++, 15);

  run();
  run.cancel();
  await delay(30);

  assert.equal(calls, 0);
});

test("flush invokes a pending call immediately and only once", async () => {
  const calls = [];
  const run = debounce((value) => {
    calls.push(value);
    return value * 2;
  }, 100);

  run(4);
  assert.equal(run.flush(), 8);
  assert.equal(run.flush(), 8);
  await delay(120);

  assert.deepEqual(calls, [4]);
});

test("debounce validates its callback and wait", () => {
  assert.throws(() => debounce(null), TypeError);
  assert.throws(() => debounce(() => {}, "10"), TypeError);
  assert.throws(() => debounce(() => {}, -1), RangeError);
  assert.throws(() => debounce(() => {}, Infinity), RangeError);
  assert.throws(() => debounce(() => {}, NaN), RangeError);
});
