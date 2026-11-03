class EmailService {
  send(to, subject) { console.log(`Sending '${subject}' to ${to}`); }
  unsend(to) { console.log(`Recalling message to ${to}`); }
}

class SendEmailCommand {
  constructor(service, to, subject) {
    this.service = service;
    this.to = to;
    this.subject = subject;
  }
  execute() { this.service.send(this.to, this.subject); }
  undo() { this.service.unsend(this.to); }
}

class JobQueue {
  constructor() { this.pending = []; this.history = []; }
  submit(cmd) { this.pending.push(cmd); }
  runNext() { const cmd = this.pending.shift(); cmd.execute(); this.history.push(cmd); }
  cancelLast() { const cmd = this.history.pop(); if (cmd) cmd.undo(); }
}

const service = new EmailService();
const queue = new JobQueue();
queue.submit(new SendEmailCommand(service, "ana@example.com", "Weekly report"));
queue.runNext();    // Sending 'Weekly report' to ana@example.com
queue.cancelLast(); // Recalling message to ana@example.com
