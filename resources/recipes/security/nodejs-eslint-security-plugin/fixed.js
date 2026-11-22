// The same endpoints, rewritten so the plugin reports zero findings.
import { execFile } from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';

const ALLOWED_DIR = path.resolve('./data');

const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  const filename = url.searchParams.get('file');
  const pattern = url.searchParams.get('pattern');

  // Validate and confine the requested path to a known directory
  const requested = path.resolve(ALLOWED_DIR, filename ?? '');
  if (!requested.startsWith(ALLOWED_DIR + path.sep)) {
    res.writeHead(400).end('bad path');
    return;
  }
  const content = fs.readFileSync(requested, 'utf8');

  // Escape user input before it reaches RegExp
  const escaped = (pattern ?? '').replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(escaped);

  // eval removed — evaluate JSON or use a real parser instead
  const buf = Buffer.from(filename ?? '', 'utf8'); // safe constructor
  const token = crypto.randomBytes(16).toString('hex'); // crypto-grade random

  execFile('ls', ['-la', requested], () => {}); // args array, no shell

  res.end(JSON.stringify({ content, token, match: regex.test('x'), buf: buf.length }));
});

server.listen(3000);
