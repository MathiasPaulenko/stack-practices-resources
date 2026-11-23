// Minimal Socket.io client — works in Node or bundler context.
// Run a second instance to see real-time delivery.
import { io } from "socket.io-client";

const url = process.env.SERVER_URL || "http://localhost:3000";
const username = process.env.USERNAME || `user-${Math.floor(Math.random() * 1000)}`;

const socket = io(url);

socket.on("connect", () => {
    console.log(`Connected as ${username} (${socket.id})`);
    socket.emit("user-join", username);
    socket.emit("join-room", "general");
});

socket.on("chat-message", (data) => {
    console.log(`[${data.username}] ${data.message}`);
});

socket.on("room-message", (data) => {
    console.log(`(room) [${data.from}] ${data.message}`);
});

socket.on("user-list", (list) => {
    console.log("Online:", list.join(", "));
});

socket.on("notification", (msg) => {
    console.log("—", msg);
});

socket.on("disconnect", () => {
    console.log("Disconnected from server");
});

// Send a test message every few seconds so two clients can see each other.
setInterval(() => {
    socket.emit("chat-message", `hello from ${username} @ ${new Date().toISOString()}`);
}, 5000);
