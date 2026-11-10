/**
 * Context-aware HTML escaping helpers (JavaScript, zero dependencies).
 *
 * Companion to https://stackpractices.com/recipes/escape-html-entities/
 * Covers three output contexts: HTML body, <script>-embedded JSON, and URLs.
 */

const HTML_ENTITY_MAP = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#x27;'
};

const ALLOWED_PROTOCOLS = ['http:', 'https:', 'mailto:', 'tel:'];

/**
 * Escape text for an HTML body or quoted-attribute context.
 * Converts & < > " ' into entity references.
 */
function escapeHtml(text) {
  return text.replace(/[&<>"']/g, char => HTML_ENTITY_MAP[char]);
}

/**
 * Escape text using the browser's own parser (browser environments only).
 * Note: innerHTML escapes < > & but leaves quotes as-is, since they can't
 * break out of a text node. Fine for body content, not for attributes.
 */
function escapeHtmlDom(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Serialize JSON so it is safe to embed inside a <script> tag.
 * HTML entities can't protect a script block — the parser looks for the
 * literal </script> string, so < (and --> for comment contexts) are
 * neutralized as unicode escapes instead.
 */
function safeJsonInScript(data) {
  let json = JSON.stringify(data);
  json = json.replace(/</g, '\\u003c');
  json = json.replace(/-->/g, '--\\u003e');
  return json;
}

/**
 * Validate a URL for use in an href/src attribute.
 * The attack is the protocol, not the characters: 'javascript:alert(1)'
 * has nothing HTML-escapable yet executes on click. Returns '' for
 * disallowed protocols, otherwise the resolved href.
 *
 * baseUrl lets the same function run under Node (tests) or the browser.
 */
function safeUrl(url, baseUrl) {
  const base = baseUrl || (typeof window !== 'undefined'
    ? window.location.origin
    : 'https://example.com');
  try {
    const parsed = new URL(url, base);
    if (!ALLOWED_PROTOCOLS.includes(parsed.protocol)) {
      return '';
    }
    return parsed.href;
  } catch {
    return '';
  }
}

module.exports = { escapeHtml, escapeHtmlDom, safeJsonInScript, safeUrl };
