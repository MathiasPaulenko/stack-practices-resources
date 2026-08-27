const fs = require('fs');
const readline = require('readline');

const LOG_PATTERN = /^(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) ([^"]+)" (\d{3}) (\S+)/;

async function parseApacheLog(filePath) {
    const stream = fs.createReadStream(filePath);
    const rl = readline.createInterface({ input: stream });
    const statusCounts = {};
    let total = 0;
    let parseErrors = 0;

    for await (const line of rl) {
        total += 1;
        const match = LOG_PATTERN.exec(line);
        if (match) {
            const status = match[6];
            statusCounts[status] = (statusCounts[status] || 0) + 1;
        } else {
            parseErrors += 1;
            console.log(`malformed line ${total}: ${line.slice(0, 120)}`);
        }
    }

    console.log('\nStatus counts:', statusCounts);
    console.log(`Parse errors: ${parseErrors}/${total} (${(100 * parseErrors / total).toFixed(2)}%)`);
}

parseApacheLog('access.log').catch(console.error);
