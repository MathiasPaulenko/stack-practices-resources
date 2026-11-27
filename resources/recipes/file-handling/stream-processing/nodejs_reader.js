const fs = require('fs');
const { Transform } = require('stream');

const upperCase = new Transform({
  transform(chunk, enc, cb) { this.push(chunk.toString().toUpperCase()); cb(); }
});
fs.createReadStream('input.txt')
  .pipe(upperCase)
  .pipe(fs.createWriteStream('output.txt'));
