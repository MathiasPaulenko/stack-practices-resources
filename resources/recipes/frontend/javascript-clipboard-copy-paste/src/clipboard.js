/**
 * Clipboard helpers — modern Async Clipboard API with execCommand fallback.
 *
 * Notes:
 * - `navigator.clipboard` only exists in secure contexts (HTTPS or localhost).
 * - Every method requires transient user activation; Firefox/Safari show an
 *   ephemeral "Paste" menu for reads instead of a permission dialog.
 * - `clipboard-read`/`clipboard-write` permission names are Chromium-only.
 */

/**
 * Copy text to the clipboard. Tries `navigator.clipboard.writeText` first,
 * then falls back to an off-screen textarea + `execCommand("copy")`.
 * Must be called inside a user gesture.
 * @param {string} text
 * @returns {Promise<boolean>} true if the text reached the clipboard
 */
export async function copyToClipboard(text) {
  if (navigator.clipboard && window.isSecureContext) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (err) {
      // Fall through to the legacy fallback
    }
  }
  return legacyCopy(text);
}

/**
 * Legacy copy path for engines without the Async Clipboard API.
 * @param {string} text
 * @returns {boolean}
 */
export function legacyCopy(text) {
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.style.position = "fixed";
  textarea.style.left = "-9999px";
  document.body.appendChild(textarea);
  textarea.focus();
  textarea.select();

  try {
    return document.execCommand("copy");
  } catch (err) {
    return false;
  } finally {
    document.body.removeChild(textarea);
  }
}

/**
 * Read plain text from the clipboard.
 * Firefox/Safari: shows an ephemeral "Paste" menu that the user must click.
 * Chromium: requests the `clipboard-read` permission on first use.
 * @returns {Promise<string|null>}
 */
export async function readClipboardText() {
  try {
    return await navigator.clipboard.readText();
  } catch (err) {
    console.error("Failed to read clipboard:", err);
    return null;
  }
}

/**
 * Read rich clipboard content (HTML, images) via ClipboardItem.
 * Always inspect `item.types` before calling `getType()` — the clipboard
 * may hold formats your app can't handle.
 * @returns {Promise<{html: string|null, imageBlob: Blob|null}>}
 */
export async function readRichClipboard() {
  const result = { html: null, imageBlob: null };
  const items = await navigator.clipboard.read();

  for (const item of items) {
    if (item.types.includes("text/html")) {
      const blob = await item.getType("text/html");
      result.html = await blob.text();
    } else if (item.types.includes("image/png")) {
      result.imageBlob = await item.getType("image/png");
    }
  }
  return result;
}

/**
 * Check the `clipboard-write` permission state.
 * Returns true (granted), null (prompt), or false (denied/unsupported).
 * The permission name is Chromium-only; `query()` throws elsewhere,
 * which we treat as "unknown — attempt inside a user gesture".
 * @returns {Promise<boolean|null>}
 */
export async function checkClipboardPermission() {
  try {
    const permission = await navigator.permissions.query({
      name: "clipboard-write",
    });
    if (permission.state === "granted") return true;
    if (permission.state === "prompt") return null;
    return false;
  } catch (err) {
    return null;
  }
}

/**
 * Attach "Copy" buttons to every `pre code` block under `root`.
 * @param {ParentNode} [root=document]
 */
export function addCopyButtons(root = document) {
  root.querySelectorAll("pre code").forEach((codeBlock) => {
    const button = document.createElement("button");
    button.className = "copy-btn";
    button.textContent = "Copy";
    button.style.position = "absolute";
    button.style.top = "8px";
    button.style.right = "8px";

    button.addEventListener("click", async () => {
      const ok = await copyToClipboard(codeBlock.textContent);
      if (ok) {
        button.textContent = "Copied!";
        setTimeout(() => (button.textContent = "Copy"), 2000);
      }
    });

    const pre = codeBlock.parentElement;
    pre.style.position = "relative";
    pre.appendChild(button);
  });
}

/**
 * Install a paste interceptor that strips HTML tags and collapses
 * whitespace before inserting plain text.
 * @param {HTMLElement} el - focusable element (input, textarea, contenteditable)
 */
export function interceptPasteAsPlainText(el) {
  el.addEventListener("paste", (event) => {
    event.preventDefault();
    const clipboardData = event.clipboardData || window.clipboardData;
    const pastedText = clipboardData.getData("text/plain");
    const cleanText = pastedText.replace(/<[^>]*>/g, "").replace(/\s+/g, " ").trim();
    document.execCommand("insertText", false, cleanText);
  });
}

/**
 * Install a paste handler that previews pasted images into `previewEl`.
 * @param {HTMLElement} el
 * @param {HTMLElement} previewEl
 */
export function interceptPasteImages(el, previewEl) {
  el.addEventListener("paste", (event) => {
    const items = event.clipboardData?.items;
    if (!items) return;

    for (const item of items) {
      if (item.type.startsWith("image/")) {
        const file = item.getAsFile();
        const reader = new FileReader();
        reader.onload = (e) => {
          const img = document.createElement("img");
          img.src = e.target.result;
          img.style.maxWidth = "300px";
          previewEl.appendChild(img);
        };
        reader.readAsDataURL(file);
      }
    }
  });
}
