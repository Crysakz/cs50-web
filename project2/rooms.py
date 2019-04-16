class Rooms():
    """Initialialize room, which stores 100 msg per specification"""

    def __init__(self, name):
        self.name = name
        self.messages = []
        self.users = []
        self.mesage_limit = 100

    def append_message(self, list):
        self.messages.append(list)

    def enforce_max_messages(self):
        if len(self.messages) > self.mesage_limit:
            self.messages.pop(0)

    def append_user(self, username):
        self.users.append(username)

    def remove_user(self, username):
        self.users.remove(username)
