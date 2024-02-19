#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor, InfraredSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import random

# Hardware
ev3 = EV3Brick()
medium_motor = Motor(Port.A)
left_motor = Motor(Port.B, positive_direction=Direction.CLOCKWISE)
right_motor = Motor(Port.C, positive_direction=Direction.CLOCKWISE)
touch_sensor = TouchSensor(Port.S1)
color_sensor = ColorSensor(Port.S2)
infrared_sensor = InfraredSensor(Port.S4)
drive_base = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=114)

# Constanten
Kp = 125  # Proportionele versterking
TARGET_REFLECTION = 4  # Doelreflectiewaarde voor blauw
LINE_SPEED = 150  # Snelheid voor lijnvolgen
SEARCH_TURN_SPEED = 75  # Draaisnelheid tijdens het zoeken naar de lijn
MAX_SEARCH_TIME = 3000  # Maximale zoektijd in milliseconden voor het omkeren van de richting
BACKUP_DISTANCE = -50  # Afstand om terug te rijden in millimeters
BACKUP_SPEED = -75  # Snelheid om terug te rijden
ACCELERATION_TIME = 2000  # Tijd in milliseconden om te accelereren naar volle snelheid
TURN_ANGLES = [90, -150]  # Mogelijke draaihoeken voor het zoeken

# Functie om een klein stukje terug te rijden
def backup():
    drive_base.straight(BACKUP_DISTANCE)

# Functie om naar de lijn te zoeken met een afwisselende zoekrichting
def search_for_line():
    global preferred_direction
    # Eerst een stukje terugrijden
    backup()
    if color_sensor.reflection() <= TARGET_REFLECTION + 5:
        return  # Lijn gevonden na het terugrijden
    
    for angle in TURN_ANGLES:
        drive_base.turn(angle * preferred_direction)
        if color_sensor.reflection() <= TARGET_REFLECTION + 5:
            return  # Lijn gevonden
        preferred_direction *= -1  # Wissel de voorkeursrichting voor de volgende zoekactie

# Helper functie voor geleidelijke acceleratie
def accelerate_to_line_speed(initial_speed, target_speed, acceleration_time):
    stopwatch = StopWatch()
    while stopwatch.time() < acceleration_time:
        current_speed = initial_speed + (target_speed - initial_speed) * (stopwatch.time() / acceleration_time)
        yield current_speed

accelerator = None  # Initialiseren van de accelerator generator

# Hoofdlus voor het volgen van de lijn
preferred_direction = 1  # Begin met een voorkeursrichting, 1 voor rechts, -1 voor links
while True:
    reflection = color_sensor.reflection()
    if reflection <= TARGET_REFLECTION + 5:
        deviation = reflection - TARGET_REFLECTION
        if accelerator is None:  # Als de accelerator generator nog niet bestaat, maak deze dan aan
            accelerator = accelerate_to_line_speed(LINE_SPEED / 2, LINE_SPEED, ACCELERATION_TIME)
        try:
            current_line_speed = next(accelerator)  # Haal de volgende snelheid uit de accelerator
        except StopIteration:
            current_line_speed = LINE_SPEED  # Als de accelerator klaar is, gebruik de maximale lijnsnelheid
        turn_rate = Kp * deviation
        drive_base.drive(current_line_speed, turn_rate)
    else:
        search_for_line()
        accelerator = None  # Reset de accelerator voor een nieuwe acceleratie na het zoeken

    wait(10)
