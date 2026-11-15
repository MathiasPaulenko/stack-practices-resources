// main.js — registration, connection status, offline form queue
if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
        navigator.serviceWorker
            .register("/sw.js")
            .then((reg) => console.log("SW registered:", reg.scope))
            .catch((err) => console.error("SW registration failed:", err));
    });
}

const statusEl = document.getElementById("status");
const queueEl = document.getElementById("queue");

function renderStatus() {
    statusEl.querySelector("strong").textContent =
        navigator.onLine ? "online" : "offline";
}

async function renderQueue() {
    const items = await getStoredFormData();
    queueEl.innerHTML = items.length
        ? items.map((i) => `<li>#${i.id} — ${i.name}: ${i.message}</li>`).join("")
        : "<li><em>empty</em></li>";
}

async function submitForm(data) {
    if ("serviceWorker" in navigator && "SyncManager" in window) {
        const reg = await navigator.serviceWorker.ready;
        await storeFormData(data);
        reg.sync.register("submit-form");
        return "queued for background sync";
    }
    await fetch("/api/submit", {
        method: "POST",
        body: JSON.stringify(data)
    });
    return "sent directly";
}

document.getElementById("demo-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target));
    try {
        const result = await submitForm(data);
        console.log("submit:", result);
        e.target.reset();
    } catch (err) {
        console.error("submit failed:", err);
    }
    renderQueue();
});

window.addEventListener("online", renderStatus);
window.addEventListener("offline", renderStatus);
window.addEventListener("online", renderQueue);
renderStatus();
renderQueue();
