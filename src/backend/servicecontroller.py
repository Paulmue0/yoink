class ServiceController:
    def __init__(self, sender) -> None:
        self.sender = sender
    def send(self, msg):
        self.sender.send_message(msg)