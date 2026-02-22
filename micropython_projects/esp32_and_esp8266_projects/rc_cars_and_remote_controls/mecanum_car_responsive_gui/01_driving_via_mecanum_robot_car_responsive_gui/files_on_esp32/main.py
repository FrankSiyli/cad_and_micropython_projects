from microdot_asyncio import Microdot, Response, send_file
from microdot_asyncio_websocket import with_websocket
from microdot_utemplate import render_template
from robot_car import RobotCar

app = Microdot()
Response.default_content_type = "text/html"

# Wifi Robot Car Configuration
MAX_POWER_LEVEL = 65535		# 100%
MEDIUM_POWER_LEVEL = 49151  # 75%
MIN_POWER_LEVEL = 32767		# 50%

front_enable_pins = [23, 22]
front_motor_pins = [19, 21, 25, 33]

rear_enable_pins = [26, 27]
rear_motor_pins = [16, 17, 12, 14]

robot_car = RobotCar(front_enable_pins, rear_enable_pins, front_motor_pins, rear_motor_pins, MEDIUM_POWER_LEVEL)


car_commands = {
    "forward": robot_car.forward,
    "reverse": robot_car.reverse,
    "left": robot_car.left,
    "right": robot_car.right,
    "spinLeft": robot_car.spinLeft,
    "spinRight": robot_car.spinRight,
    "stop": robot_car.stop
}

speed_commands = {
    "slow-speed": MIN_POWER_LEVEL,
    "normal-speed": MEDIUM_POWER_LEVEL,
    "fast-speed": MAX_POWER_LEVEL
}


# App Route
@app.route("/")
async def index(request):
    return render_template("index.html")


@app.route("/ws")
@with_websocket
async def executeCarCommands(request, ws):
    while True:
        websocket_message = await ws.receive()
        print(f"receive websocket message : {websocket_message}")
        
        if "speed" in websocket_message:
            new_speed = speed_commands.get(websocket_message)
            robot_car.set_speed(new_speed)
        else:
            command = car_commands.get(websocket_message)
            command()
        await ws.send("OK")


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
