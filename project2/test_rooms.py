import unittest

from rooms import Rooms


class TestRoom(unittest.TestCase):

    def setUp(self):
        self.new_room = Rooms("general")
        self.new_room.message_limit = 5

    def test_name_of_the_room(self):
        self.assertEqual(self.new_room.name, "general")

    def test_adding_user(self):
        self.new_room.append_user("John")
        self.assertIn("John", self.new_room.users)

    def test_removing_user(self):
        self.new_room.append_user("John")
        self.new_room.remove_user("John")
        self.assertNotIn("John", self.new_room.users)

    def test_adding_message(self):
        self.new_room.append_message("Hello!")
        self.assertIn("Hello!", self.new_room.messages)

    def test_enforcing_limit(self):
        self.new_room.messages = ["Hello", "Hi"]
        self.new_room.enforce_max_messages()
        self.assertEqual(len(self.new_room.messages), 2)

    def test_enforcing_limit2(self):
        self.new_room.messages = [
            "Hello", "Hi", "Tony", "How are you?", "good", "bad"]
        self.new_room.enforce_max_messages()
        self.assertEqual(len(self.new_room.messages), 5)


if __name__ == '__main__':
    unittest.main()
