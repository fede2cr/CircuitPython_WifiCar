# CircuitPython_WifiCar
Carro controlado por medio de Wifi, basado en la micro ESP8266 con el lenguaje educativo CircuitPython, basado en Micropython

Este documento describe las labores a realizar. Una vez que el proyecto tenga avance, el documento [HOWTO.md](https://github.com/fede2cr/CircuitPython_WifiCar/blob/master/HOWTO.md) reemplazará buena parte de este README.

## Descripción
Greencore Solutions ya tiene un curso de robótica para niños basado en micros Arduino, donde los estudiantes construyen su carro de dos motores el cual es manejado con un control remoto infrarojo, al cual queremos mejorar lo siguiente:

1. El control infrarojo de un estudiante acciona los carros de otros estudiantes por lo que necesitamos cambiar la forma de control remoto.
2. El lenguaje de Arduino se basa en C/C++ por lo que no es la mejor opción para estudiantes completamente novatos. Para ello se recomienda migra a MicroPython o mejor aún a CircuitPython.
3. La micro ofrecida anteriormente tenía un acelerómetro lo que permitía que estudiantes avanzados comenzaran a hacer detección de golpe y otros comportamientos. La micro actual es un poco básica por lo que requiere hardware adicional para permitir que sea interesante para estudiantes avanzados.

## Propuesta
Cambiar a la plataforma de [Feather de Adafruit](https://www.adafruit.com/feather), con los siguientes componentes:

- Adafruit ESP8266 Feather: La plataforma ESP8266 es compatible con Arduino si fuera necesario, tiene conector JST para batería (con capacidad de cargar baterías Lipo), capacidades de red inalámbrica Wifi, así como trabaja con CircuitPython/Micropython.
- Adafruit DC Motor+Stepper Featherwing: Tiene capacidad de hasta cuatro motores lo que permite usar cualquier de los chasis disponibles en [CrCibernetica](http://crcibernetica.com/).

### Cambios menores:
- Cambiar lugar de baterías AAA por posición más accesible. Actualmente hay que desarmar parcialmente el robot para cambio de baterías. Es posible alimentar los motores de 4.5VDC a 13.5VDC por lo que se podría cambiar a baterías 9V u otras.

## Plan de trabajo
- [x] Alistar componentes de hardware: Soldar stacing headers en Feather y Featherwing, remover placa anterior, alistar conectores de batería.
- [x] Instalar última versión de CircuitPython en la ESP8266
- [x] Ensamblar robot con nueva micro y realizar control básico de motores.
- [x] Usar como base WebREPL para crear una librería que permita control del robot por medio de una página web servida por el mismo ESP8266.
- [ ] Crear documentación visual de ensamblaje de robot.
- [ ] Crear diversos laboratorios que el estudiante pueda seguir para sacarle un mejor provecho a su robot ensamblado y completo.
- [ ] Crear traducciones de la documentación
- [ ] Crear clases que permitan crear alias para comandos en otros idiomas (forward=adelante, etc)
