# Guía de construcción y uso del WifiCar con CircuitPython

## Instrucciones
1. Realizar conexión física

Se recomienda que el soldado de los stacking headers y terminales sea realizado previo al taller. De esta forma la única herramienta necesaria sería un desatornillador de punta phillips para ensamblaje del chasis.

- Soldar stacking headers en el ESP8266 y el Featherwing para motor
- Soldar terminales de tornillo en Featherwing para motor
- Poner baterías en holder
- Conectar holder de baterías a puerto de batería para motor, del Featherwing para motores

La tarjeta debería verse de esta forma:

![Diagrama de Fritzing](https://github.com/fede2cr/CircuitPython_WifiCar/blob/master/doc/Diagrama%20conexiones%20-%20Wifi%20Car.png)

2. Instalar CircuitPython en ESP8266: Se carga firmware según [instrucciones de Adafruit](https://learn.adafruit.com/micropython-basics-how-to-load-micropython-on-a-board/?view=all#esp8266), pero usando release de CircuitPython

```
esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 adafruit-circuitpython-feather_huzzah-0.8.4.bin
```
Reiniciar el ESP8266, y comprobar que se puede acceder al REPL de CircuitPython, conectándose al puerto serial
```
screen /dev/ttyUSB0 115200
```
Puede salir de screen digitando ``CTRL+A`` y luego ``:quit``.

3. Luego debe descargar los módulos de CircuitPython de [Featherwing de motor](https://github.com/adafruit/Adafruit_CircuitPython_PCA9685/releases), de [Register](https://github.com/adafruit/Adafruit_CircuitPython_Register/releases) y [Bus Device](https://github.com/adafruit/Adafruit_CircuitPython_BusDevice/releases):

```
export AMPY_PORT=/dev/ttyUSB0
unzip adafruit_pca9685.zip
ampy put adafruit_pca9685
unzip adafruit_register.zip
ampy put adafruit_register
unzip adafruit_bus_device.zip
ampy put adafruit_bus_device
ampy ls
```
Ahora puedes probar un pequeño "hola mundo" para comprobar que has subido los módulos de forma correcta, y que has conectado correctamente las baterías y motores. Para esto debes ejecutar de nuevo el comando de ``screen`` para entrar en el REPL de CircuitPython.
**Nota: Si todo funciona correctamente, el carro se va a mover hacia adelante. Acomódelo de forma que no se caiga de la mesa de trabajo**
```
from board import *
import bitbangio as io
i2c = io.I2C(SCL, SDA)
from adafruit_pca9685 import motor
motors = motor.DCMotors(i2c)
motors.speed(0, 2000)
motors.speed(3, 2000)
```
*Nota: Es posible que el número del motor haya cambiado, por lo que puedes probar cambiando el motor a mover*
Habiendo comenzado a moverse, el robot solo se va a detener hasta que se agoten las baterías. Para ello digitamos el siguiente comando por cada motor, para iniciar el frenado:
```
motors.brake(0)
motors.brake(3)
```

## Acceso por Wifi
Esta es una parte que también puede ser preconfigurada en la tarjeta antes de entregar al estudiante, dependiendo de la naturaleza del laboratorio a realizar.
Para tener control del IP que recibe la tarjeta, puede definirle un hostname y utilizar el módulo de MulticastDNS (mDNS) para publicar un nombre único por tarjeta.


