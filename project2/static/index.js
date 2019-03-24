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
  };
} else if (window.location.pathname !== '/chat') {
  window.location.pathname = '/chat';
}
document.addEventListener('DOMContentLoaded', () => {
  const socket = io.connect(
    `${window.location.protocol}//${document.domain}:${window.location.port}`,
  );

  socket.on('connect', () => {
    document.querySelector('#roomForm').onsubmit = () => {
      // Send room name to server
      const text = document.querySelector('#room-name').value;
      socket.emit('submit room', { roomName: text });
      text.value = '';
      return false;
    };

    document.querySelector('#chatForm').onsubmit = () => {
      // Send room name to server
      const message = document.querySelector('#message').value;
      message.value = '';
      return false;
    };

    const list = document.querySelector('#rooms');

    /* Delegate event listener, applies click event to all childs.
       Even new ones emmited from other users */
    list.addEventListener('click', (event) => {
      // Connect user to chat room and leave old on
      const room = event.target.innerHTML;
      const username = window.localStorage.getItem('username');
      socket.emit('join', { room, username });
    });
  });

  socket.on('add room', (data) => {
    // Apend room name to list of rooms
    const li = document.createElement('li');
    li.innerHTML = data;
    document.querySelector('#rooms').append(li);
  });

  socket.on('joined', (username, room) => {
    // Send message that user has joned specific room, to all users in the room
    const p = document.createElement('p');
    p.innerHTML = `user ${username} joined ${room}`;
    document.querySelector('#chatForm').append(p);
  });

  socket.on('room already exist', (data) => {
    // Show user alert if he tries to add existing room
    const errorAlert = document.createElement('div');
    errorAlert.innerHTML = `${data} Room already exists!$`;
    errorAlert.classList.add('alert', 'alert-danger');
    document.querySelector('body').prepend(errorAlert);
  });
});
