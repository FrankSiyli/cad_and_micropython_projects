var targetUrl = `ws://${location.host}/ws`;
var websocket;

function initializeSocket() {
  console.log("Opening WebSocket connection to ESP32 MicroPython Server...");
  websocket = new WebSocket(targetUrl);
  websocket.onopen = onOpen;
  websocket.onclose = onClose;
  websocket.onmessage = onMessage;
}

function onLoad() {
  initializeSocket();
  setDefaultSpeed();
  setInterval(updateDistanceValue, 250);
  setInterval(updateCPUTemperature, 5000);
}

function onOpen(event) {
  console.log("Starting connection to WebSocket server..");
}

function onClose(event) {
  console.log("Closing connection to server..");
  setTimeout(initializeSocket, 2000);
}

function updateCPUTemperature() {
  websocket.send("request_cpu_temp");
}

function handleDirectionButton(distance, direction) {
  const button = document.querySelector(
    `.control[data-direction="${direction}"]`
  );
  if (distance < 20) {
    sendMessage("car-stop");
    button.classList.add("disabled");
  } else {
    button.classList.remove("disabled");
  }
}

function onMessage(event) {
  var data = JSON.parse(event.data);
  document.getElementById(
    "distance-front-value"
  ).innerText = `Front distance: ${data.distance_front} cm`;
  document.getElementById(
    "distance-rear-value"
  ).innerText = `Rear distance: ${data.distance_rear} cm`;
  document.getElementById(
    "distance-left-value"
  ).innerText = `Left distance: ${data.distance_left} cm`;
  document.getElementById(
    "distance-right-value"
  ).innerText = `Right distance: ${data.distance_right} cm`;

  handleDirectionButton(data.distance_front, "forward");
  handleDirectionButton(data.distance_rear, "reverse");
  handleDirectionButton(data.distance_left, "left");
  handleDirectionButton(data.distance_right, "right");
  if (data.cpu_temp) {
    document.getElementById(
      "cpu-temp"
    ).innerText = `CPU temp: ${data.cpu_temp} °C`;
  }
}

function updateDistanceValue() {
  websocket.send("request_distance");
}

function sendMessage(message) {
  websocket.send(message);
}

var speedSettings = document.querySelectorAll(
  'input[type=radio][name="speed-settings"]'
);
speedSettings.forEach((radio) =>
  radio.addEventListener("change", () => {
    var speedSettings = radio.value;
    console.log("Speed Settings :: " + speedSettings);
    sendMessage(speedSettings);
  })
);

function setDefaultSpeed() {
  console.log("Setting default speed to normal..");
  let normalOption = document.getElementById("option-2");
  normalOption.checked = true;
}

// O-Pad/ D-Pad Controller and Javascript Code
document.body.addEventListener("click", function (e) {
  if (e.target && e.target.nodeName == "A") {
    e.preventDefault();
  }
});

function touchStartHandler(event) {
  var direction = event.target.dataset.direction;
  console.log("Touch Start :: " + direction);
  sendMessage("car-" + direction);
}

function touchEndHandler(event) {
  const stop_command = "car-stop";
  var direction = event.target.dataset.direction;
  console.log("Touch End :: " + direction);
  sendMessage(stop_command);
}

document.querySelectorAll(".control").forEach((item) => {
  item.addEventListener("touchstart", touchStartHandler);
});

document.querySelectorAll(".control").forEach((item) => {
  item.addEventListener("touchend", touchEndHandler);
});

// Call onLoad function when the window loads
window.addEventListener("load", onLoad);
