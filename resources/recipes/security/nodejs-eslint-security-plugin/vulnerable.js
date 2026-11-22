// Deliberately insecure code — run `npx eslint .` to see the plugin flag every line.
import { exec } from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import http from 'node:http';

const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  const filename = url.searchParams.get('file');
  const pattern = url.searchParams.get('pattern');
  const expression = url.searchParams.get('expr');

  // security/detect-non-literal-fs-filename — path traversal
  const content = fs.readFileSync(filename, 'utf8');

  // security/detect-non-literal-regexp — user input into RegExp, ReDoS risk
  const regex = new RegExp(pattern);

  // security/detect-eval-with-expression — code injection
  const result = eval(expression);

  // security/detect-new-buffer — deprecated unsafe constructor
  const buf = new Buffer(filename);

  // security/detect-pseudoRandomBytes — weak randomness for tokens
  const token = crypto.pseudoRandomBytes(16).toString('hex');

  // security/detect-child-process — shell injection
  exec(`ls ${filename}`, () => {});

  res.end(JSON.stringify({ content, result, token, match: regex.test('x'), buf: buf.length }));
});

server.listen(3000);
