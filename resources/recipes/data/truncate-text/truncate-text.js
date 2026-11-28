// Text truncation helpers: character slice, word boundary, and grapheme-safe.

function truncate(text, maxLength = 100) {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength - 3).trimEnd() + '...';
}

function truncateWords(text, maxLength = 100) {
  if (text.length <= maxLength) return text;
  const truncated = text.slice(0, maxLength - 3);
  const lastSpace = truncated.lastIndexOf(' ');
  return (lastSpace > 0 ? truncated.slice(0, lastSpace) : truncated) + '...';
}

// Counts grapheme clusters, so emoji and combined marks count as one.
function truncateGraphemes(text, maxLength = 100) {
  const segments = [...new Intl.Segmenter().segment(text)];
  if (segments.length <= maxLength) return text;
  return segments.slice(0, maxLength - 1).map(s => s.segment).join('') + '…';
}

module.exports = { truncate, truncateWords, truncateGraphemes };

if (require.main === module) {
  const s = 'This is a very long sentence that needs to be shortened.';
  console.log(truncate(s, 50));
  console.log(truncateWords(s, 50));
  console.log(truncateGraphemes('Hello 👋🏽 world ' + 'x'.repeat(200), 20));
}
