// Temporary file and directory patterns from the Generate Temporary Files recipe.
//
// Run: node temp_files.js   (after: npm install)

import os from 'node:os';
import fs from 'node:fs';
import path from 'node:path';
import { randomBytes } from 'node:crypto';
import tmp from 'tmp';

// Own the cleanup contract: whoever calls withTempDir gets a fresh dir and
// a guaranteed rm -rf afterwards, whatever the callback does.
async function withTempDir(fn) {
    const dir = await fs.promises.mkdtemp(path.join(os.tmpdir(), 'myapp-'));
    try {
        return await fn(dir);
    } finally {
        await fs.promises.rm(dir, { recursive: true, force: true });
    }
}

// Crypto-random name + exclusive create: 'wx' throws EEXIST if the path is
// already taken, so there is no pick-then-create race window.
async function exclusiveTempFile(dir, suffix = '.bin') {
    const filePath = path.join(dir, `part-${randomBytes(8).toString('hex')}${suffix}`);
    await fs.promises.writeFile(filePath, Buffer.from('payload'), { flag: 'wx' });
    return filePath;
}

async function main() {
    const files = await withTempDir(async (dir) => {
        const a = await exclusiveTempFile(dir, '.json');
        const b = await exclusiveTempFile(dir, '.json');
        console.log(`created in ${dir}: ${path.basename(a)}, ${path.basename(b)}`);
        return [a, b];
    });
    console.log(`dir swept on exit; first file still exists? ${fs.existsSync(files[0])}`);

    // The tmp package registers removal on process exit for you.
    const tmpObj = tmp.fileSync({ postfix: '.json' });
    fs.writeFileSync(tmpObj.name, '{"key": "value"}');
    console.log(`tmp package file: ${tmpObj.name}`);

    const tmpDir = tmp.dirSync({ unsafeCleanup: true });
    console.log(`tmp package dir: ${tmpDir.name}`);
    // Both are removed when the process exits (or call removeCallback()).
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});
