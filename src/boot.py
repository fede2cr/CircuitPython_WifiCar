# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import gc
import webrepl
webrepl.start()
gc.collect()

from board import *
import bitbangio as io
i2c = io.I2C(SCL, SDA)
from adafruit_pca9685 import motor
motors = motor.DCMotors(i2c)
