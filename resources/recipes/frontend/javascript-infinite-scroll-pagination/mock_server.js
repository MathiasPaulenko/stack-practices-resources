// Mock API + static file server for the demo — zero dependencies.
// Run: node mock_server.js  →  open http://127.0.0.1:8010/demo.html

import http from "node:http";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const TOTAL = 120;

const POSTS = Array.from({ length: TOTAL }, (_, i) => ({
    id: i + 1,
    title: `Post ${i + 1}`,
    excerpt: `Excerpt for post ${i + 1} — served by the mock API.`
}));

// Exported for tests
export function paginate({ page, limit }) {
    const start = (page - 1) * limit;
    const items = POSTS.slice(start, start + limit);
    return { items, page, hasMore: start + limit < TOTAL, total: TOTAL };
}

export function createServer() {
    return http.createServer(async (req, res) => {
        const url = new URL(req.url, "http://localhost");

        if (url.pathname === "/api/posts") {
            const page = parseInt(url.searchParams.get("page") || "1", 10);
            const limit = parseInt(url.searchParams.get("limit") || "12", 10);
            res.writeHead(200, { "Content-Type": "application/json" });
            res.end(JSON.stringify(paginate({ page, limit })));
            return;
        }

        const file = url.pathname === "/" ? "demo.html" : url.pathname.slice(1);
        try {
            const body = await readFile(join(HERE, file));
            const type = file.endsWith(".js") ? "text/javascript" : "text/html";
            res.writeHead(200, { "Content-Type": type });
            res.end(body);
        } catch {
            res.writeHead(404);
            res.end("not found");
        }
    });
}

// Run directly: node mock_server.js
if (process.argv[1] === fileURLToPath(import.meta.url)) {
    createServer().listen(8010, () => {
        console.log("Demo at http://127.0.0.1:8010/demo.html");
    });
}
