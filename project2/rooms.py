class Rooms():
    """Initialialize room, which stores 100 msg"""

    def __init__(self, name):
        self.name = name
        self.messages = []
        self.users = []

    def append_message(self, list):
        self.messages.append(list)
        self.check_maximum_lenght()

    def check_maximum_lenght(self):
        if len(self.messages) > 100:
            self.messages.pop(0)

    def append_user(self, username):
        self.users.append(username)

    def remove_user(self, username):
        return True if self.users.remove(username) else False
