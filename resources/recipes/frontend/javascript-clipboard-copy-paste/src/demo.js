import {
  copyToClipboard,
  readClipboardText,
  readRichClipboard,
  checkClipboardPermission,
  addCopyButtons,
  interceptPasteAsPlainText,
  interceptPasteImages,
} from "./clipboard.js";

const status = (msg) => (document.getElementById("status").textContent = msg);

document.getElementById("copy-btn").addEventListener("click", async () => {
  const ok = await copyToClipboard(document.getElementById("copy-input").value);
  status(ok ? "Copied!" : "Copy failed — check permissions/context");
});

document.getElementById("paste-btn").addEventListener("click", async () => {
  const text = await readClipboardText();
  document.getElementById("output").value = text ?? "(read failed or denied)";
});

document.getElementById("rich-btn").addEventListener("click", async () => {
  try {
    const { html, imageBlob } = await readRichClipboard();
    if (html) document.getElementById("rich-out").textContent = html;
    if (imageBlob) {
      document.getElementById("preview").src = URL.createObjectURL(imageBlob);
    }
    status("Rich clipboard read OK");
  } catch (err) {
    status(`read() failed: ${err.name}`);
  }
});

checkClipboardPermission().then((state) => {
  status(
    state === null
      ? "clipboard-write: prompt/unsupported — will ask on first use"
      : `clipboard-write: ${state ? "granted" : "denied"}`,
  );
});

interceptPasteAsPlainText(document.getElementById("editor"));
interceptPasteImages(document.getElementById("editor"), document.getElementById("paste-area"));
addCopyButtons();
