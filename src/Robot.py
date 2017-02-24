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
