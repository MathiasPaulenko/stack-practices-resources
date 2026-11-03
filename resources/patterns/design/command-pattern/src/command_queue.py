from abc import ABC, abstractmethod
from collections import deque

class Command(ABC):
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def undo(self): ...

class EmailService:  # Receiver
    def send(self, to: str, subject: str):
        print(f"Sending '{subject}' to {to}")
    def unsend(self, to: str):
        print(f"Recalling message to {to}")

class SendEmailCommand(Command):  # Concrete command
    def __init__(self, service: EmailService, to: str, subject: str):
        self.service = service
        self.to = to
        self.subject = subject

    def execute(self):
        self.service.send(self.to, self.subject)

    def undo(self):
        self.service.unsend(self.to)

class JobQueue:  # Invoker: runs + tracks commands, knows nothing about EmailService
    def __init__(self):
        self.pending = deque()
        self.history = []

    def submit(self, cmd: Command):
        self.pending.append(cmd)

    def run_next(self):
        cmd = self.pending.popleft()
        cmd.execute()
        self.history.append(cmd)

    def cancel_last(self):
        if self.history:
            self.history.pop().undo()

# Client: wires commands to receivers, submits them to the invoker
service = EmailService()
queue = JobQueue()
queue.submit(SendEmailCommand(service, "ana@example.com", "Weekly report"))
queue.submit(SendEmailCommand(service, "luis@example.com", "Invoice #42"))
queue.run_next()      # Sending 'Weekly report' to ana@example.com
queue.cancel_last()   # Recalling message to ana@example.com
