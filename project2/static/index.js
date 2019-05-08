if (!window.localStorage.getItem('username')) {
  // Redirect user if no username
  if (window.location.pathname !== '/') window.location.pathname = '/';

  document.querySelector('#submit-button').disabled = true;

  document.querySelector('#username').onkeyup = () => {
    if (document.querySelector('#username').value.length > 0) {
      document.querySelector('#submit-button').disabled = false;
    }
  };
  // Store username in user local storage
  document.querySelector('#form').onsubmit = () => {
    const user = document.querySelector('#username').value;
    window.localStorage.setItem('username', user);
    window.localStorage.setItem('room', 'general');
  };
} else if (window.location.pathname !== '/chat') {
  window.location.pathname = '/chat';
}
document.addEventListener('DOMContentLoaded', () => {
  const socket = io.connect(
    `${window.location.protocol}//${document.domain}:${window.location.port}`,
  );

  socket.on('connect', () => {
    class LocalStorage {
      constructor() {
        this.username = window.localStorage.getItem('username');
        this.room = window.localStorage.getItem('room') || 'general';
      }

      joinLastRoom() {
        socket.emit('join', {
          room: this.room,
          username: this.username,
        });
      }

      updateRoom(room) {
        window.localStorage.room = room;
        this.room = room;
      }
    }


    const localStorage = new LocalStorage();
    localStorage.joinLastRoom();

    document.querySelector('#room-form').onsubmit = () => {
      // Send room name to server
      const text = document.querySelector('#room-name');
      socket.emit('submit room', {
        room: text.value,
      });
      text.value = '';
      text.classList.remove('is-invalid');
      return false;
    };

    document.querySelector('#chat-form').onsubmit = () => {
      // Send message to server side
      const message = document.querySelector('#message').value;
      socket.emit('message', {
        room: localStorage.room,
        message,
        username: localStorage.username,
      });
      document.querySelector('#message').value = '';
      return false;
    };

    const ulList = document.querySelector('#rooms');

    /* Delegate event listener, applies click event to all childs.
       Even new ones emmited from other users */
    ulList.addEventListener('click', (event) => {
      // Connect user to chat room
      if (event.target.nodeName === 'LI') {
        const room = event.target.innerHTML;
        if (window.localStorage.room !== room) {
          socket.emit('leave', {
            room: localStorage.room,
            username: localStorage.username,
          });
          localStorage.updateRoom(room);
          document.querySelector('#chat-space').innerHTML = '';
          socket.emit('join', {
            room,
            username: localStorage.username,
          });
        }
      }
    });
  });

  socket.on('add room', (data) => {
    // Apend room name to list of rooms
    const li = document.createElement('li');
    li.innerHTML = data;
    document.querySelector('#rooms').append(li);
  });

  const createLiElement = (username, id) => {
    const liElement = document.createElement('li');
    liElement.innerHTML = username;
    liElement.id = id;
    return liElement;
  };

  socket.on('joined', (username, userId, room) => {
    // Send message that user has joned specific room to all users in the room
    const p = document.createElement('p');
    p.innerHTML = `user ${username} joined ${room}`;
    document.querySelector('#chat-space').append(p);

    const joinedUserLi = createLiElement(username, userId);
    const emitUserToList = document.querySelector('#room-online-users');
    emitUserToList.append(joinedUserLi);
  });

  socket.on('display messages and online users', (messages, users) => {
    messages.forEach((message) => {
      const oldMessages = document.createElement('p');
      oldMessages.innerHTML = `<span class="username">${message[0]}:</span> 
                               <span class="message">${message[1]}</span> 
                               <span class="time">${message[2]}<span>`;
      document.querySelector('#chat-space').append(oldMessages);
    });

    const onlineUsers = document.querySelector('#room-online-users');
    onlineUsers.innerHTML = '';

    users.forEach((user) => {
      if (user !== window.localStorage.getItem('username')) {
        const id = user[0];
        const username = user[1];
        const userLi = createLiElement(username, id);
        onlineUsers.append(userLi);
      }
    });
  });

  socket.on('message', (message, username, time) => {
    // Send message that user has joned specific room to all users in the room
    const p = document.createElement('p');
    p.innerHTML = `<span class="username">${username}:</span> <span class="message">${message}</span> <span class="time">${time}</span>`;
    document.querySelector('#chat-space').append(p);
  });

  socket.on('user left room', (userId) => {
    const onlineUser = document.getElementById(`${userId}`);
    onlineUser.parentNode.removeChild(onlineUser);
  });

  socket.on('room already exist', () => {
    // Show user alert if he tries to add existing room
    const roomForm = document.getElementById('room-name');
    roomForm.classList.add('is-invalid');
  });
});
