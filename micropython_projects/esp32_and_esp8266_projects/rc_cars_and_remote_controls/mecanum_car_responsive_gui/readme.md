![image](./IMG_5258.jpg)
<br>

![image](./IMG_4919.jpg)

### Parts

<br>
4WD with 4x Mecanum wheels and 4x motors
<br>
1x ESP32 Wroom32 Devkit 4
<br>
2x L298N
<br>
1x ON/OFF switch
<br>
2x 18650 cells
<br>
1x 2S BMS charger
<br>
<br>

## Code Base

The fantastic code base for a 2 wheel robot is from
[donskytech](https://github.com/donskytech/micropython-wifi-robot-car/tree/main)
<br>
<br>
I adjusted it for my 4 wheel mecanum robot.
<br>
<br>
Please also install the utemplate library on your ESP

## To use the robot car, follow these steps:

1. In the boot.py change the Hotspot name and the password that belongs to your iphone Hotspot.
2. Create the Hotspot with your iPhone.
3. Press the reset button of your ESP32, the programm should log into your iphone Hotspot. You can follow the progress in the REPL.
4. In your browser, visit the IP address of your ESP and add ":5000". You can find the address in the REPL, for example: `172.20.10.2:5000`.

<br>
<br>

## Pins

### Front L298N:

IN1 --> Pin 21
<br>
IN2 --> Pin 19
<br>
IN3 --> Pin 33
<br>
IN4 --> Pin 25
<br>
ENA --> Pin 23
<br>
ENB --> Pin 22
<br>

### Rear L298N:

IN1 --> Pin 17
<br>
IN2 --> Pin 16
<br>
IN3 --> Pin 14
<br>
IN4 --> Pin 12
<br>
ENA --> Pin 26
<br>
ENB --> Pin 27
