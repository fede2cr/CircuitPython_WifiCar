# RobotControl
# Cualquier posible sensor va a estar apagado por omisión
# Los comandos de movimiento deberían ser similares a los de LogoWriter

# Uso ejemplo:
#   import Robot
#   robot = Robot.Control(motors)
#   robot.adelante(10)
# Autor: Alvaro Figueroa (alvaro@greencore.co.cr)
import time

class Control:
    def __init__(self, motors):
        self._motors = motors
        self._motors.brake(0)
        self._motors.brake(3)

    def adelante(self, secs):
        self._motors.speed(0,2000)
        self._motors.speed(3,2000)
        time.sleep(secs)
        self._motors.brake(0)
        self._motors.brake(3)

    def atras(self, secs):
        self._motors.speed(0,-2000)
        self._motors.speed(3,-2000)
        time.sleep(secs)
        self._motors.brake(0)
        self._motors.brake(3)

    def derecha(self, secs):
        self._motors.speed(0,2000)
        self._motors.speed(3,-2000)
        time.sleep(secs)
        self._motors.brake(0)
        self._motors.brake(3)

    def izquierda(self, secs):
        self._motors.speed(0,-2000)
        self._motors.speed(3,2000)
        time.sleep(secs)
        self._motors.brake(0)
        self._motors.brake(3)

    def hola(self):
        self.adelante(1)
        self.atras(1)
        self.derecha(1)
        self.izquierda(1)

    def geometria(self, lados, largo_secs, angulo_secs):
        for i in range(lados):
            self.adelante(largo_secs)
            self.izquierda(angulo_secs)

    def sillywalk_serpiente(self,secs):
        for i in range(4):
            self._motors.speed(0,4000)
            self._motors.speed(3,2000)
            time.sleep(secs/8)
            self._motors.speed(0,2000)
            self._motors.speed(3,4000)
            time.sleep(secs/8)
        self._motors.brake(0)
        self._motors.brake(3)

    def sillywalk_turn(self,secs):
        for i in range(4):
            self._motors.speed(0,4000)
            self._motors.speed(3,-4000)
            time.sleep(secs/8)
            self._motors.speed(0,-4000)
            self._motors.speed(3,4000)
            time.sleep(secs/8)
        self._motors.brake(0)
        self._motors.brake(3)


    def ayuda(self):
        print("""Modulo de control de robot.
Comandos:
carro.hola()                    Realiza una demostracion de movimientos
carro.adelante(segundos)        Avanza la cantidad de segundos que se indique
carro.atras(segundos)           Retocede la cantidad de segundos que se indique
carro.derecha(segundos)         Gira sobre su eje a la derecha, la cantidad de
                                segundos que se indique
carro.izquierda(segundos)       Gira sobre su eje a la izquierda, la cantidad de
                                segundos que se indique
carro.geometria(lados,
   largo_secs, angulo_secs)     Le indicamos la cantidad de lados, que tan
                                largos en segundos, cuanto tiempo durar girando,
                                y nos crea una figura geometrica

Ejemplos:
carro.hola()
carro.adelante(2)
carro.izquierda(1)
carro.atras(3)
carro.geometria(4, 2, 0.7)
Puede encontrar informacion adicional en
https://github.com/fede2cr/CircuitPython_WifiCar/""")
