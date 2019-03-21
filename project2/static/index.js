if (!localStorage.getItem("username")) {
  // Redirect user if no username
  if (window.location.pathname !== "/") window.location.pathname = "/";

  document.querySelector("#submit-button").disabled = true;

  document.querySelector("#username").onkeyup = () => {
    if (document.querySelector("#username").value.length > 0) {
      document.querySelector("#submit-button").disabled = false;
    }
  };

  document.querySelector("#form").onsubmit = () => {
    const user = document.querySelector("#username").value;
    localStorage.setItem("username", user);
  };
} else {
  if (window.location.pathname !== "/chat") {
    window.location.pathname = "/chat";
  }
}
document.addEventListener("DOMContentLoaded", () => {
  var socket = io.connect(
    location.protocol + "//" + document.domain + ":" + location.port
  );

  socket.on("connect", () => {
    document.querySelector("#roomForm").onsubmit = () => {
      const text = document.querySelector("#room-name").value;
      socket.emit("submit room", { roomName: text });
      document.querySelector("#room-name").value = "";
      return false;
    };
  });

  socket.on("add room", data => {
    const li = document.createElement("li");
    li.innerHTML = data;
    document.querySelector("#rooms").append(li);
  });
});
