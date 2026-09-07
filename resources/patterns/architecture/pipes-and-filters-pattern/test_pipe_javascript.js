// Tests for the Pipes and Filters Pattern — JavaScript implementation.
// Run: node test_pipe_javascript.js

const {
    pipe, parseCsv, filterActive, normalizeEmails, deduplicate, toJson,
} = require('./pipe_javascript.js');

function assert(condition, message) {
    if (!condition) throw new Error(`FAIL: ${message}`);
    console.log(`PASS: ${message}`);
}

function testParseCsv() {
    const raw = "name,email\nAlice,a@x.com\nBob,b@x.com";
    const result = parseCsv(raw);
    assert(result.length === 2, 'parseCsv returns 2 records');
    assert(result[0].name === 'Alice', 'first record name is Alice');
}

function testFilterActive() {
    const records = [
        { name: 'Alice', status: 'active' },
        { name: 'Bob', status: 'inactive' },
    ];
    const result = filterActive(records);
    assert(result.length === 1, 'filterActive keeps only active');
    assert(result[0].name === 'Alice', 'active record is Alice');
}

function testNormalizeEmails() {
    const records = [{ email: '  ALICE@X.COM  ' }];
    const result = normalizeEmails(records);
    assert(result[0].email === 'alice@x.com', 'email normalized to lowercase trimmed');
}

function testDeduplicate() {
    const records = [
        { email: 'a@x.com' },
        { email: 'a@x.com' },
        { email: 'b@x.com' },
    ];
    const result = deduplicate(records);
    assert(result.length === 2, 'deduplicate removes 1 duplicate');
}

function testPipeComposability() {
    const double = (x) => x * 2;
    const addOne = (x) => x + 1;
    const pipeline = pipe(double, addOne);
    assert(pipeline(3) === 7, 'pipe composes double then addOne: (3*2)+1=7');
}

testParseCsv();
testFilterActive();
testNormalizeEmails();
testDeduplicate();
testPipeComposability();
console.log('\nAll tests passed!');
