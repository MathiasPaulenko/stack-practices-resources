interface Command {
    void execute();
    void undo();
}

class EmailService {
    void send(String to, String subject) {
        System.out.println("Sending '" + subject + "' to " + to);
    }
    void unsend(String to) {
        System.out.println("Recalling message to " + to);
    }
}

class SendEmailCommand implements Command {
    private final EmailService service;
    private final String to, subject;
    SendEmailCommand(EmailService service, String to, String subject) {
        this.service = service; this.to = to; this.subject = subject;
    }
    public void execute() { service.send(to, subject); }
    public void undo() { service.unsend(to); }
}

class JobQueue {
    private final Deque<Command> pending = new ArrayDeque<>();
    private final List<Command> history = new ArrayList<>();
    void submit(Command cmd) { pending.addLast(cmd); }
    void runNext() { Command c = pending.pollFirst(); c.execute(); history.add(c); }
    void cancelLast() {
        if (!history.isEmpty()) history.remove(history.size() - 1).undo();
    }
}
