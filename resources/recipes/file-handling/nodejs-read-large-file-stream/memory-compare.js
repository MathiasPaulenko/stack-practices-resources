// Compare memory usage: fs.readFile vs streaming line count.
// Usage: node memory-compare.js <file>
// Prints heap delta for both approaches — run with a big file to see the difference.

const fs = require("fs");
const readline = require("readline");

const heap = () => process.memoryUsage().heapUsed / 1024 / 1024;

async function streamCount(path) {
    const before = heap();
    const rl = readline.createInterface({
        input: fs.createReadStream(path, { highWaterMark: 64 * 1024 }),
        crlfDelay: Infinity,
    });
    let n = 0;
    for await (const line of rl) n++;
    return { lines: n, mb: (heap() - before).toFixed(1) };
}

function readFileCount(path) {
    const before = heap();
    const data = fs.readFileSync(path, "utf8");
    const n = data.split("\n").length;
    return { lines: n, mb: (heap() - before).toFixed(1) };
}

async function main() {
    const file = process.argv[2];
    if (!file || !fs.existsSync(file)) {
        console.log("Usage: node memory-compare.js <file>");
        console.log('Generate one: node -e "require(\'fs\').writeFileSync(\'big.log\', \'x\\n\'.repeat(5e6))"');
        process.exit(0);
    }
    const s = await streamCount(file);
    console.log(`stream:   ${s.lines} lines, heap delta ${s.mb} MB`);
    const r = readFileCount(file);
    console.log(`readFile: ${r.lines} lines, heap delta ${r.mb} MB`);
}

main();
