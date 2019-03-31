class Rooms():
    """Initialialize room, which stores 100 msg"""
    def __init__(self, name):
        self.name = name
        self.messages = []

    def append_message(self, list):
        self.messages.append(list)
        self.check_maximum_lenght()

    def check_maximum_lenght(self):
        if len(self.messages) > 100:
            self.messages.pop(0)
