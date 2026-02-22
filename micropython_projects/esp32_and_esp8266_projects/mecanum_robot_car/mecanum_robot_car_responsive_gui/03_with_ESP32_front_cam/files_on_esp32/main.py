from microdot_asyncio import Microdot, Response, send_file
from microdot_asyncio_websocket import with_websocket
from microdot_utemplate import render_template
from robot_car import RobotCar
from machine import Pin
from machine import time_pulse_us
from ultrasonic_sensors import get_distance_front, get_distance_rear
import uasyncio
import time
import ujson

app = Microdot()
Response.default_content_type = "text/html"

# Wifi Robot Car Configuration
MAX_POWER_LEVEL = 65535  # 100%
MEDIUM_POWER_LEVEL = 49151  # 75%
MIN_POWER_LEVEL = 32767  # 50%

front_enable_pins = [23, 22]
front_motor_pins = [19, 21, 25, 33]

rear_enable_pins = [26, 27]
rear_motor_pins = [16, 17, 12, 14]

robot_car = RobotCar(
    front_enable_pins,
    rear_enable_pins,
    front_motor_pins,
    rear_motor_pins,
    MEDIUM_POWER_LEVEL,
)


async def request_distance_command(ws):
    distance_front = get_distance_front()
#    print(f"FrontDistance: {distance_front} cm, Type: {type(distance_front)}")
    distance_rear = get_distance_rear()
#    print(f"RearDistance: {distance_rear} cm, Type: {type(distance_rear)}")
    ws_message = ujson.dumps({"distance_front": distance_front, "distance_rear": distance_rear})
    await ws.send(ws_message)

car_commands = {
    "car-forward": robot_car.forward,
    "car-reverse": robot_car.reverse,
    "car-left": robot_car.left,
    "car-right": robot_car.right,
    "car-spinLeft": robot_car.spinLeft,
    "car-spinRight": robot_car.spinRight,
    "car-stop": robot_car.stop,
}

sensor_commands = {"request_distance": request_distance_command}

speed_commands = {
    "slow-speed": MIN_POWER_LEVEL,
    "normal-speed": MEDIUM_POWER_LEVEL,
    "fast-speed": MAX_POWER_LEVEL,
}


# App Route
@app.route("/")
async def index(request):
    return render_template("index.html")


@app.route("/ws")
@with_websocket
async def handle_websocket(request, ws):
    while True:
        websocket_message = await ws.receive()
        print(f"Received WebSocket message: {websocket_message}")
        if "distance" in websocket_message and websocket_message in sensor_commands:
            uasyncio.create_task(handle_sensor_command(websocket_message, ws))
            await ws.send("OK")
        elif "car" in websocket_message and websocket_message in car_commands:
            command = car_commands.get(websocket_message)
            command()
            await ws.send("OK")
        elif "speed" in websocket_message and websocket_message in speed_commands:
            robot_car.set_speed(speed_commands[websocket_message])
            await ws.send("OK")
        else:
            print(f"Command '{websocket_message}' not found.")



async def handle_car_command(command):
    await car_commands[command]()


async def handle_sensor_command(command, ws):
    await sensor_commands[command](ws)


@app.route("/shutdown")
async def shutdown(request):
    request.app.shutdown()
    return "The server is shutting down..."


@app.route("/static/<path:path>")
def static(request, path):
    if ".." in path:
        # directory traversal is not allowed
        return "Not found", 404
    return send_file("static/" + path)


if __name__ == "__main__":
    try:
        app.run()
    except KeyboardInterrupt:
        robot_car.cleanUp()