#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor)
from pybricks.parameters import Port, Direction, Button
from pybricks.tools import wait
from pybricks.robotics import DriveBase
import random

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Hardware setup
medium_motor = Motor(Port.A)
left_motor = Motor(Port.B, Direction.CLOCKWISE)
right_motor = Motor(Port.C, Direction.CLOCKWISE)
touch_sensor = TouchSensor(Port.S1)
# Color sensor setup for potential future use
color_sensor = ColorSensor(Port.S2)
infrared_sensor = InfraredSensor(Port.S4)
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

# Drive speed for manual control.
drive_speed = 1000  # Adjust this value as needed
turn_speed = 500
medium_speed = 300

def random_turn():
    angle = random.choice([-130, 90, -180, 314, -220, 150])  # Randomly turn degrees
    robot.turn(angle)

def avoid_obstacle():
    robot.stop()  # Stop the robot if the touch sensor is pressed
    robot.straight(-100)  # Reverse 10 cm
    random_turn()  # Make a random turn
    wait(100)  # Wait for 100 ms

def auto_pilot():
    while Button.BEACON in infrared_sensor.buttons(channel=1):
        if touch_sensor.pressed():
            avoid_obstacle()
        else:
            robot.drive(drive_speed, 0)  # Drive straight at the specified speed
        wait(50)  # Small delay to allow for button state refresh and prevent CPU overload

def control_robot():
    while True:
        buttons_pressed = infrared_sensor.buttons(channel=1)
        
        # Check for obstacles first
        if touch_sensor.pressed():
            avoid_obstacle()
            continue  # Skip the rest of this loop iteration

        # Auto-pilot mode
        if Button.BEACON in buttons_pressed:
            auto_pilot()
            continue  # Return to the start of the loop to check conditions again

        # Manual control logic
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
            robot.stop()  # This stops the driving motors
            medium_motor.stop()  # Ensure the medium motor also stops

        wait(50)  # Small delay to prevent overloading the CPU

try:
    control_robot()
except KeyboardInterrupt:
    # Ensure all motors are stopped when the program ends.
    left_motor.stop()
    right_motor.stop()
    medium_motor.stop()