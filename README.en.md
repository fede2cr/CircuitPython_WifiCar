# How to build and use of the WifiCard with CircuitPython

## Instructions
### Physical assembly

It is recommented that you install stacking headers and terminals on the Feather and Featherwing previous to the class. If you prepare in advance you will only need a phillips screw driver to complete the assembly of the chassis.

- Solder stacking headers on the ESP8266 Feather Huzzah and the DC motor Featherwing.
- Solder screw terminals for the DC motor Featherwing.
- Add AA batteries to the battery holder.
- Connect the battery holder cables to the screw terminal on the DC motor Featherwing

The build should look like this at this step:

![Fritzing Diagram](https://github.com/fede2cr/CircuitPython_WifiCar/blob/master/doc/Diagrama%20conexiones%20-%20Wifi%20Car.png)
(TODO: I'm missing the Lipo for the ESP in this diagram)

### Install CircuitPython on the ESP8266

Load up the firmware following the streps on this [guide by Adafruit](https://learn.adafruit.com/micropython-basics-how-to-load-micropython-on-a-board/?view=all#esp8266), pero using a CircuitPython release.

```bash
esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 adafruit-circuitpython-feather_huzzah-2.2.0.bin
```
Reboot the ESP8266, and doble check you can access the CircuitPython REPL, by connecting to the serial port:
```
screen /dev/ttyUSB0 115200
```
You can exit `screen` by writing ``CTRL+A`` and then ``:quit``.

### CircuitPython modules

Instead downloading the CircuitPython modules for the Featherwing de motor module, the Register module and the Bus Device module, we will download the [CircuitPython Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases) use the tool ``ampy`` to upload the ``lib`` **folder** that contains the modules, to the flash of the ESP8266:

```bash
export AMPY_PORT=/dev/ttyUSB0
unzip adafruit-circuitpython-bundle-2.*.zip
ampy put lib 
ampy ls
```
Now you can test a small proof of concept to test that you have uploaded the modules properly, and that you have correctly plugged in the batteries and motors to the correct terminals. To do this you need to run the `screen` command again to get into the CircuitPython REPL.

**Note: If everything works fine, the car should move forward. Please place it in a safe position to avoid it being dropped from a work table**

```python
from board import *
import bitbangio as io
i2c = io.I2C(SCL, SDA)
from adafruit_pca9685 import motor
motors = motor.DCMotors(i2c)
motors.speed(0, 2000)
motors.speed(3, 2000)
```
*Note: The motor number can change depending how where you connect the motors and how many do you have, so if a motor doesn't move try changing this values*

Once the robot speed is set and starts moving, it will only stop moving when the batteries run out. To make it stop when you want use the following command, once for each motor:
```python
motors.brake(0)
motors.brake(3)
```

### Wifi
This part can also be pre-configured before giving out the boards to the students, depending on the nature of the class you are preparing.

With the CircuitPython firmware with the default settings from Adafruit, the ESP8266 will start running as an wireless access point, and we would like to connect it to our local wireless network during our class or workshop. It is also important to configure this before moving to the WebREPL section.

It is important that the Wifi config does not have to be stored in the `boot.py` file, since it is stored internally by CircuitPython. For this we run this commands inside the REPL.

```python
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('nombre-AP-curso','clave-segura')
```
After a few seconds you will be connected to the network, which you can verify by running:
```python
wlan.ifconfig()
```

### WebREPL
The Web version of the REPL is almost ready to be used. First you must import the  `webrepl_setup` module, which handles enabling the WebREPL permanently, as well as defining an access  password.

*Note: CircuitPython does not have a limit for the ammount of conextions which is why it should be easy to do a brute force dictionary attack to guest the password. For this reason, outside an educational environment it is recommended to either to use a secure password, o disable WebREPL altogether.*


```python
>>> import webrepl_setup
WebREPL daemon auto-start status: disabled

Would you like to (E)nable or (D)isable it running on boot?
(Empty line to quit)
> e
To enable WebREPL, you must set password for it
New password: greencore
Confirm password: greencore
Changes will be activated after reboot
Would you like to reboot now? (y/n) y

```

After this step the board should reboot automatically and leave as enabled WebREPL. For  [now](https://github.com/adafruit/circuitpython/issues/98) you must reboot the board manually by pressing the RESET button on either the ESP8266 or in the Motor Featherwing.

Normally we should download [this client](https://github.com/micropython/webrepl/archive/master.zip), open up the zip, open with Firefox or Chromium. You then define the IP the ESP8266 is using, press *Connect* and write the predefined password. You can now write python commands on to the microcontroller vía WebREPL, including commands for moving the motors. However, in this project we have included web server functionality so that the WebREPL web page is self hosted by the ESP8266.

We will add some code to `boot.py` to enable the web server and self-host it's own WebREPL without the need for an extra web server or an Internet connection. The code is based on  [replserver](https://github.com/ShrimpingIt/cockle/blob/master/replserver/).

To upload the self served WebREPL, we must add this minimized and compressed web page by running:
```bash
ampy put webrepl-inlined.html.gz
```

### Robot autoconfiguration

In order to avoid writing the commands that define the motors each time we boot the board, we are adding this commands to the `boot.py` file. This way, everytime we start the board it will configure the motor Featherwing and the car will be ready for just writing the driving commands directly.

To do this you first should look if you have some other code in your existing `boot.py` file that might be worth saving. In our case however, since we are starting from scratch, you can skip this step. To check it's content we run:
```bash
ampy get boot.py
```
For our robot we will use the file as a base, un-comment the lines that disable *debugging*, which is enabled dues to the early stage of development in which CircuitPython is at the time.
We add the lines for configuring the motor Featherwing as well as the web server code for the self-hosted WebREPL and we upload them to our ESP8266 with:
```bash
ampy put boot.py
```

After rebooting our ESP8266 we can now run run motors command directly on the board:
```python
motors.speed(0, 2000)
motors.speed(3, 2000)
```
Remember that this command will never brake so you have to by running:

```python
motors.brake(0)
motors.brake(3)
```

### Python class for driving the car

Up to now we have a car that we can control via Web over Wifi. However the way we control this car is quite different from the way you would drive any other type of electric car like a GoCard or a Tesla.

So we would like to create a small Python class that will handle the driving commands in a simpler way. We will also assume that this version of the robot doesn't have any type of sensors like a gyroscope or rotary encoders, which is why we must calibrate and approximate the motion of the robot.

Loading this class is already being done automatically by the `boot.py` file.

To load the class to the robot you must run:
```bash
ampy put Robot.py
ampy ls
```
Now you can connect to the robot using either `screen` or WebREPL and inside it run:

```python
carro.adelante(seconds)
carro.izquierda(seconds)
carro.hola() # A mini demo
```

You can also create simple geomteries by defining the **amount of sides**, the **length of the lines in seconds**, and the **time to rotate to create correct angle**. It is important to calibrate the angle which will change depending of the surface, traction of the tires, type and charge of the batteries for the motors:
```python
carro.geometria(3, 1, 0.9) # A small triangle
carro.geometria(4, 2, 0.7) # Un square
```

You can also run some of the behavior demos this way:
```python
carro.demo(sillywalks) # Like MonthyPython
carro.demo(wifitaxa)   # Walks to find the access point
```

## References
- [Running code and Ampy use](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/?view=all)
- [Motor Featherwing](https://learn.adafruit.com/micropython-hardware-pca9685-dc-motor-and-stepper-driver/?view=all)
- [WebREPL](https://learn.adafruit.com/micropython-basics-esp8266-webrepl/?view=all)
- [TonyD's WebREPL Robot](https://www.youtube.com/watch?v=hOwReBsHq7g)
- [replserver](https://github.com/ShrimpingIt/cockle/blob/master/replserver/)
