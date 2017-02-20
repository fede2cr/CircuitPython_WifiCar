# Guía de construcción y uso del WifiCar con CircuitPython

## Instrucciones
### Realizar conexión física

Se recomienda que el soldado de los stacking headers y terminales sea realizado previo al taller. De esta forma la única herramienta necesaria sería un desatornillador de punta phillips para ensamblaje del chasis.

- Soldar stacking headers en el ESP8266 y el Featherwing para motor
- Soldar terminales de tornillo en Featherwing para motor
- Poner baterías en holder
- Conectar holder de baterías a puerto de batería para motor, del Featherwing para motores

La tarjeta debería verse de esta forma:

![Diagrama de Fritzing](https://github.com/fede2cr/CircuitPython_WifiCar/blob/master/doc/Diagrama%20conexiones%20-%20Wifi%20Car.png)

### Instalar CircuitPython en ESP8266

Se carga firmware según [instrucciones de Adafruit](https://learn.adafruit.com/micropython-basics-how-to-load-micropython-on-a-board/?view=all#esp8266), pero usando release de CircuitPython

```bash
esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 adafruit-circuitpython-feather_huzzah-0.8.4.bin
```
Reiniciar el ESP8266, y comprobar que se puede acceder al REPL de CircuitPython, conectándose al puerto serial
```
screen /dev/ttyUSB0 115200
```
Puede salir de screen digitando ``CTRL+A`` y luego ``:quit``.

### Módulos de CircuitPython

Luego debe descargar los módulos de CircuitPython de [Featherwing de motor](https://github.com/adafruit/Adafruit_CircuitPython_PCA9685/releases), de [Register](https://github.com/adafruit/Adafruit_CircuitPython_Register/releases) y [Bus Device](https://github.com/adafruit/Adafruit_CircuitPython_BusDevice/releases). Luego utilice la herramienta de ``ampy`` para subir las **carpetas** de los módulos al flash de la ESP8266:

```bash
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
```python
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
```python
motors.brake(0)
motors.brake(3)
```

### Acceso por Wifi
Esta es una parte que también puede ser preconfigurada en la tarjeta antes de entregar al estudiante, dependiendo de la naturaleza del laboratorio a realizar.
A como viene el firmware de CircuitPython de Adafruit, el ESP8266 se va a comportar como un Access Point wireless, por lo que queremos conectarlo a la red a utilizar durante el curso o taller. También es importante que se configure antes de pasar al sección de WebREPL.

Es importante que la configuración de Wifi no debe ser guardada en ``boot.py`` dado que es almacenada de forma interna por CircuitPython. Para ello ejemutamos desde el REPL.

```python
import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('nombre-AP-curso','clave-segura')
```
Luego de unos segundos estará conectado a la red, lo que puede comprobar ejecutando:
```python
wlan.ifconfig()
```

### WebREPL
El WebREPL ya casi se encuentra listo para ser usado. Primero debes importar el módulo de `webrepl_setup` el cual se encarga de habilitar WebREPL de forma permanente, así como definir una contraseña de acceso. *Nota: CircuitPython no tiene límite de conexiones por lo que es fácilmente atacable por fuerza bruta con listas de diccionario. Por ello, fuera de un ambiente académico se recomienda o utilizar una contraseña segura o deshabilitar WebREPL*.


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

Luego de este paso, la tarjeta debería reiniciar automáticamente y dejarnos con el WebREPL activado. Por [mientras](https://github.com/adafruit/circuitpython/issues/98) debes reiniciar la tarjeta manualmente presionando el botón de RESET ya sea en la ESP8266 o en el Featherwing de motores.

Para accesar el WebREPL debes bajar el [cliente desde esta dirección](https://github.com/micropython/webrepl/archive/master.zip), descomprimir, y abrir con Firefox o Chromium. Defines el IP que tiene actualmente el ESP8266, presionas *Conectar* y digitas la contraseña definida. Ya puedes digitar comandos en la microcontroladora desde el WebREPL, incluidos comandos para los motores y otros.

### Autoconfiguración

Para evitar que tengamos que digitar las operaciones que definen el motor, vamos a agregar estos comandos iniciales al archivo `boot.py` de forma que cuando inicie la micro, automáticamente va a configurar la tarjeta de motor shield, para que sea más sencillo y podamos digitar comandos de motores de forma directa.

Para ello es buena idea revisar si nuestro archivo `boot.py` posee algún código importante, sin embargo en nuestro caso como hemos comenzado desde cero, es posible omitir este paso. Para revisarlo puede ejecutar:
```bash
ampy get boot.py
```
En nuestro caso, vamos a usar el archivo como base, descomentando las líneas que deshabilitan *debugging*, el cual se encuentra habilitado porque CircuitPython se encuentra en un estado muy activo de desarrollo.
Agregamos las líneas de iniciado de motor y librerías que vimos arriba, y subimos el archivo a nuestra ESP8266.
```bash
ampy push boot.py
```

Después de reiniciar nuestro ESP8266 ya podemos ejecutar comandos de motores:
```python
motors.speed(0, 2000)
motors.speed(3, 2000)
```
Recuerde que el comando actual no ejecuta ningún frenado por lo que luego debe ejecutar:

```python
motors.brake(0)
motors.brake(3)

```

### Clase de Python para manejo de carro

Hasta el momento tenemos un carro que podemos controlar vía Web sobre Wifi. Sin embargo los controles de dicho carro son un poco diferentes a las formas como conducimos algún tipo de carro eléctrico, ya sea de control remoto, un GoCart o un Tesla.

Para ello se propone crear una pequeña clase de Python donde se pueda controlar se las siguientes formas. Se asume que el robot no tiene sensores como giroscopios o rotary encoder, por lo cual algunos movimientos deben ser calibrados y aproximados.

```python
carro.adelante(segundos)
carro.izquierda(segundos)
carro.adelante(segundos,funnywalks)
```

Así mismo, se deben crear demostraciones de comportamiento, las cuales pueden ser cargadas como una clase de ejemplos:
```python
carro.demo(funnywalks)
carro.demo(wifitaxa)
```