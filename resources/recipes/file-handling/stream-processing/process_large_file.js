const fs = require('fs');
const { pipeline } = require('stream');
const { Transform, Writable } = require('stream');
const { promisify } = require('util');
const pipelineAsync = promisify(pipeline);

async function processLargeFile(inputPath, outputPath, transformFn) {
    const readStream = fs.createReadStream(inputPath, { highWaterMark: 64 * 1024 });
    const writeStream = fs.createWriteStream(outputPath + '.tmp', { highWaterMark: 64 * 1024 });

    let lineBuffer = '';
    let count = 0;
    const startTime = Date.now();

    const lineTransform = new Transform({
        highWaterMark: 64 * 1024,
        transform(chunk, encoding, callback) {
            lineBuffer += chunk.toString('utf-8');
            const lines = lineBuffer.split('\n');
            lineBuffer = lines.pop();  // Keep incomplete last line

            for (const line of lines) {
                const transformed = transformFn(line);
                if (transformed !== null) {
                    this.push(transformed + '\n');
                    count++;
                    if (count % 10000 === 0) {
                        const elapsed = (Date.now() - startTime) / 1000;
                        const rate = (count / elapsed).toFixed(0);
                        process.stdout.write(`\r  Processed ${count} lines (${rate}/s)`);
                    }
                }
            }
            callback();
        },
        flush(callback) {
            // Process remaining buffer
            if (lineBuffer) {
                const transformed = transformFn(lineBuffer);
                if (transformed !== null) {
                    this.push(transformed + '\n');
                    count++;
                }
            }
            callback();
        },
    });

    try {
        await pipelineAsync(readStream, lineTransform, writeStream);
        await fs.promises.rename(outputPath + '.tmp', outputPath);
        const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
        console.log(`\nDone: ${count} lines in ${elapsed}s`);
    } catch (err) {
        // Cleanup temp file on error
        try { await fs.promises.unlink(outputPath + '.tmp'); } catch {}
        throw err;
    }
}

// Usage
// processLargeFile('input.log', 'output.log', line => {
//     if (line.includes('ERROR')) return null;
//     return line.replace(/DEBUG:/g, 'INFO:');
// });
