// Runnable CSV -> JSONL pipeline with correct line buffering and error cleanup.
// Usage: node csv-to-jsonl.js input.csv output.jsonl
// Sample input is generated if no file is given.

const fs = require("fs");
const readline = require("readline");
const { Transform } = require("stream");
const { pipeline } = require("stream/promises");

function createCsvParser() {
    let leftover = "";
    return new Transform({
        readableObjectMode: true, // reads bytes, pushes row arrays
        transform(chunk, encoding, callback) {
            const lines = (leftover + chunk.toString()).split("\n");
            leftover = lines.pop();
            for (const line of lines) {
                if (line.trim()) this.push(line.split(","));
            }
            callback();
        },
        flush(callback) {
            if (leftover.trim()) this.push(leftover.split(","));
            callback();
        },
    });
}

const createFilter = (fn) => new Transform({
    objectMode: true,
    transform(row, enc, cb) { if (fn(row)) this.push(row); cb(); },
});

const toJsonl = new Transform({
    objectMode: true,
    transform(row, enc, cb) { this.push(JSON.stringify(row) + "\n"); cb(); },
});

async function lineCount(filePath) {
    const rl = readline.createInterface({
        input: fs.createReadStream(filePath),
        crlfDelay: Infinity,
    });
    let n = 0;
    for await (const line of rl) n++;
    return n;
}

async function main() {
    const input = process.argv[2] || "sample.csv";
    const output = process.argv[3] || "output.jsonl";

    if (!fs.existsSync(input)) {
        const rows = ["id,name,status"];
        for (let i = 0; i < 10000; i++) {
            rows.push(`${i},user_${i},${i % 3 === 0 ? "active" : "inactive"}`);
        }
        fs.writeFileSync(input, rows.join("\n"));
        console.log(`Generated ${input} (${rows.length} rows)`);
    }

    await pipeline(
        fs.createReadStream(input),
        createCsvParser(),
        createFilter((row) => row[2] === "active"),
        toJsonl,
        fs.createWriteStream(output)
    );

    const out = await lineCount(output);
    console.log(`Done: ${out} active rows written to ${output}`);
}

main().catch((err) => { console.error(err); process.exit(1); });
