// db.js — IndexedDB queue shared by the page (<script>) and sw.js (importScripts)
function openDB() {
    return new Promise((resolve, reject) => {
        const req = indexedDB.open("offline-forms", 1);
        req.onupgradeneeded = () =>
            req.result.createObjectStore("queue", { keyPath: "id", autoIncrement: true });
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
    });
}

async function storeFormData(data) {
    const db = await openDB();
    return new Promise((resolve, reject) => {
        const tx = db.transaction("queue", "readwrite");
        tx.objectStore("queue").add(data);
        tx.oncomplete = resolve;
        tx.onerror = () => reject(tx.error);
    });
}

async function getStoredFormData() {
    const db = await openDB();
    return new Promise((resolve, reject) => {
        const req = db.transaction("queue", "readonly")
            .objectStore("queue").getAll();
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => reject(req.error);
    });
}

async function removeStoredFormData(id) {
    const db = await openDB();
    return new Promise((resolve, reject) => {
        const tx = db.transaction("queue", "readwrite");
        tx.objectStore("queue").delete(id);
        tx.oncomplete = resolve;
        tx.onerror = () => reject(tx.error);
    });
}
