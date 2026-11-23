import express from "express";
import http from "http";
import { Server } from "socket.io";

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: { origin: "*" }
});

const users = new Map();

io.on("connection", (socket) => {
    socket.on("user-join", (username) => {
        users.set(socket.id, { username, joinedAt: Date.now() });
        io.emit("user-list", [...users.values()].map(u => u.username));
        socket.broadcast.emit("notification", `${username} joined the chat`);
    });

    socket.on("join-room", (room) => {
        socket.join(room);
        socket.to(room).emit("user-joined", { id: socket.id });
    });

    socket.on("leave-room", (room) => {
        socket.leave(room);
        socket.to(room).emit("user-left", { id: socket.id });
    });

    socket.on("room-message", ({ room, message }) => {
        const user = users.get(socket.id);
        socket.to(room).emit("room-message", {
            from: user?.username ?? socket.id,
            message,
            timestamp: Date.now()
        });
    });

    socket.on("chat-message", (message) => {
        const user = users.get(socket.id);
        if (!user) return;

        io.emit("chat-message", {
            username: user.username,
            message,
            timestamp: Date.now()
        });
    });

    socket.on("typing", (isTyping) => {
        const user = users.get(socket.id);
        if (!user) return;
        socket.broadcast.emit("typing", { username: user.username, isTyping });
    });

    socket.on("disconnect", () => {
        const user = users.get(socket.id);
        if (user) {
            users.delete(socket.id);
            io.emit("user-list", [...users.values()].map(u => u.username));
            socket.broadcast.emit("notification", `${user.username} left the chat`);
        }
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Chat server running on port ${PORT}`));
