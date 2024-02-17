#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor)
from pybricks.parameters import Port, Direction, Button
from pybricks.tools import wait
from pybricks.robotics import DriveBase
import random

# Hardware
ev3 = EV3Brick()
medium_motor = Motor(Port.A)
left_motor = Motor(Port.B, Direction.CLOCKWISE)
right_motor = Motor(Port.C, Direction.CLOCKWISE)
touch_sensor = TouchSensor(Port.S1)
color_sensor = ColorSensor(Port.S2)
infrared_sensor = InfraredSensor(Port.S4)
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Instellingen
drive_speed = 1000 
turn_speed = 500
medium_speed = 300

def random_turn():
    angle = random.choice([-130, 90, -180, 314, -220, 150])  # Draai willekeurig een aantal graden
    robot.turn(angle)

def avoid_obstacle():
    robot.stop()  # Stop de robot als de aanraaksensor wordt ingedrukt
    robot.straight(-100)  # Rij 10 cm achteruit
    random_turn()  # Maak een willekeurige draai
    wait(100)  # Wacht 100 ms

def auto_pilot():
    while Button.BEACON in infrared_sensor.buttons(channel=1):
        if touch_sensor.pressed():
            avoid_obstacle()
        else:
            robot.drive(drive_speed, 0)  # Rij rechtuit met de opgegeven snelheid
        wait(50)  # Kleine vertraging om knopstatus te verversen en CPU-overbelasting te voorkomen

def control_robot():
    while True:
        buttons_pressed = infrared_sensor.buttons(channel=1)
        
        # Controleer eerst op obstakels
        if touch_sensor.pressed():
            avoid_obstacle()
            continue  # Sla de rest van deze iteratie van de lus over

        # Autopiloot modus
        if Button.BEACON in buttons_pressed:
            auto_pilot()
            continue  # Ga terug naar het begin van de lus om de voorwaarden opnieuw te controleren

        # Handmatige besturingslogica
        if Button.LEFT_UP in buttons_pressed and Button.RIGHT_UP in buttons_pressed:
            robot.drive(drive_speed, 0)
        elif Button.LEFT_DOWN in buttons_pressed and Button.RIGHT_DOWN in buttons_pressed:
            robot.drive(-drive_speed, 0)
        elif Button.LEFT_UP in buttons_pressed:
            left_motor.run(-turn_speed)
            right_motor.run(turn_speed)
        elif Button.RIGHT_UP in buttons_pressed:
            left_motor.run(turn_speed)
            right_motor.run(-turn_speed)
        elif Button.LEFT_DOWN in buttons_pressed:
            medium_motor.run(medium_speed)
        elif Button.RIGHT_DOWN in buttons_pressed:
            medium_motor.run(-medium_speed)
        else:
            robot.stop()  # Dit stopt de rijaandrijfmotoren
            medium_motor.stop()  # Zorg dat de middelgrote motor ook stopt

        wait(50)  # Kleine vertraging om de CPU niet te overbelasten

try:
    control_robot()
except KeyboardInterrupt:
    # Zorg dat alle motoren stoppen wanneer het programma eindigt.
    left_motor.stop()
    right_motor.stop()
    medium_motor.stop()
