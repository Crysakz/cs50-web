# Project 2

Web Programming with Python and JavaScript

## Description:

This is Web chat usings sockets. As problem set mentions, this app should need database, so name and rooms is stored at users local storage. Users can send message to specific room and easiy change rooms. As personal touch I chosed dynamic list users, which showcases all online users in room where user is and deletes username when particual user goes offline.

In the application.py is the backed logic of the app, manages all emits sended from user and creation of the chat room. The Rooms.py is class file, which stores users messages, enforces limit of maximum capacity per room. And enables to delete or add user to channel, this is imporant for the dynamic list of online users. In static is main.js that handles all user interaction, handles showing old messages, apend messages to chat, showing list of rooms and online users. 

Please note that styling is not done! SASS/CSS file will be added later in separate branch! Right now the chat is fully working per problem spec file, but is not yet styled! 

## How to run:

First install all needed packages:
```
pip install requirements.txt
```
Then  run:

```
python application.py
```
## Requirements:

- [x] Display Name: When a user visits your web application for the first time, they should be prompted to type in a display name that will eventually be associated with every message the user sends. If a user closes the page and returns to your app later, the display name should still be remembered.
- [x] Channel Creation: Any user should be able to create a new channel, so long as its name doesn’t conflict with the name of an existing channel.
- [x] Channel List: Users should be able to see a list of all current channels, and selecting one should allow the user to view the channel. We leave it to you to decide how to display such a list.
- [x] Messages View: Once a channel is selected, the user should see any messages that have already been sent in that channel, up to a maximum of 100 messages. Your app should only store the 100 most recent messages per channel in server-side memory.
- [x] Sending Messages: Once in a channel, users should be able to send text messages to others the channel. When a user sends a message, their display name and the timestamp of the message should be associated with the message. All users in the channel should then see the new message (with display name and timestamp) appear on their channel page. Sending and receiving messages should NOT require reloading the page.
- [x] Remembering the Channel: If a user is on a channel page, closes the web browser window, and goes back to your web application, your application should remember what channel the user was on previously and take the user back to that channel.
- [x] Personal Touch: Add at least one additional feature to your chat application of your choosing! Feel free to be creative, but if you’re looking for ideas, possibilities include: supporting deleting one’s own messages, supporting use attachments (file uploads) as messages, or supporting private messaging between two users.
- [x] In README.md, include a short writeup describing your project, what’s contained in each file, and (optionally) any other additional information the staff should know about your project. Also, include a description of your personal touch and what you chose to add to the project.
- [x] If you’ve added any Python packages that need to be installed in order to run your web application, be sure to add them to requirements.txt!

## Personoal note:

For real demployment use database, as is not really suitable to use for username local storage, which can user manipulate. It's done this way because of description of the probolem set in course. 