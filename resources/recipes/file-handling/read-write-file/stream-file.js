// Safe file read/write utilities for Node.js.
// Streaming line-by-line transforms with temp-file atomic writes.
// No dependencies — Node.js 18+.

const fs = require('fs');
const { pipeline } = require('stream');
const { promisify } = require('util');
const { createReadStream, createWriteStream } = fs;
const pipe = promisify(pipeline);

// Stream a file line by line through a transform, writing atomically.
async function streamFile(srcPath, destPath, transformFn) {
    const tmpPath = destPath + '.tmp';
    const readStream = createReadStream(srcPath, { encoding: 'utf-8' });
    const writeStream = createWriteStream(tmpPath, { encoding: 'utf-8' });

    let lineBuffer = '';
    const lineTransform = new (require('stream').Transform)({
        transform(chunk, encoding, callback) {
            lineBuffer += chunk;
            const lines = lineBuffer.split('\n');
            lineBuffer = lines.pop();
            for (const line of lines) {
                const result = transformFn(line);
                if (result !== null) this.push(result + '\n');
            }
            callback();
        },
        flush(callback) {
            if (lineBuffer) {
                const result = transformFn(lineBuffer);
                if (result !== null) this.push(result + '\n');
            }
            callback();
        },
    });

    try {
        await pipe(readStream, lineTransform, writeStream);
        await fs.promises.rename(tmpPath, destPath);
    } catch (err) {
        try { await fs.promises.unlink(tmpPath); } catch {}
        throw err;
    }
}

async function readLines(path) {
    const content = await fs.promises.readFile(path, 'utf-8');
    return content.split('\n').filter(l => l.trim());
}

async function appendLine(path, line) {
    await fs.promises.appendFile(path, line + '\n', 'utf-8');
}

module.exports = { streamFile, readLines, appendLine };

// Demo: node stream-file.js
if (require.main === module) {
    (async () => {
        await fs.promises.writeFile('input.log', 'first\nsecond\nthird\n');
        await streamFile('input.log', 'output.log', line => line.toUpperCase());
        console.log(await readLines('config.txt').catch(() => ['no config.txt']));
        await appendLine('app.log', `[${new Date().toISOString()}] Started`);
    })();
}
