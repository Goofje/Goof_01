from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Direction, Color, SoundFile
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# Hardware initialisatie
ev3 = EV3Brick()
left_motor = Motor(Port.B, positive_direction=Direction.CLOCKWISE)
right_motor = Motor(Port.C, positive_direction=Direction.CLOCKWISE)
color_sensor = ColorSensor(Port.S3)
drive_base = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=114)
stopwatch = StopWatch()

# Constanten
Kp = 2  # Proportionele versterking voor lijnvolglogica
TARGET_REFLECTION = 20  # Doelreflectiewaarde voor lijnvolgen
LINE_SPEED = 150  # Snelheid voor lijnvolgen
search_angle = 20  # Begin hoek voor het zoeken naar de lijn
search_direction = 1  # Beginrichting voor het zoeken naar de lijn
best_time = None  # Beste tijd record, initieel None

# Patroonherkenning
pattern_correct = [Color.BLUE, Color.RED, Color.BLACK, Color.BLUE]
pattern_incorrect = [Color.BLUE, Color.BLACK, Color.RED, Color.BLUE]
current_pattern = []

def backup():
    drive_base.straight(-50)  # Rijdt 50 mm achteruit

def search_for_line():
    global search_angle, search_direction
    backup()
    drive_base.turn(search_angle * search_direction)
    search_direction *= -1
    search_angle += 20

def adjust_parameters():
    global Kp, LINE_SPEED, best_time
    current_time = stopwatch.time()
    if best_time is None or current_time < best_time:
        best_time = current_time
        ev3.speaker.say("New record, time: {} milliseconds".format(best_time))
        Kp += 0.1
        LINE_SPEED += 10
    else:
        Kp -= 0.05
        LINE_SPEED -= 5
    stopwatch.reset()
    stopwatch.start()

def adjust_route_based_on_pattern():
    global current_pattern
    if current_pattern == pattern_correct:
        ev3.speaker.play_file(SoundFile.FANFARE)
        adjust_parameters()  # Pas parameters aan na succesvolle ronde
        current_pattern = []  # Reset het patroon
    elif current_pattern == pattern_incorrect:
        ev3.speaker.play_file(SoundFile.BOING)
        drive_base.turn(180)
        current_pattern = []  # Reset het patroon

stopwatch.start()  # Start de stopwatch aan het begin van het script

# Hoofdlus
while True:
    reflection = color_sensor.reflection()
    detected_color = color_sensor.color()
    error = TARGET_REFLECTION - reflection
    turn_rate = Kp * error

    if detected_color != Color.NONE and (not current_pattern or detected_color != current_pattern[-1]):
        current_pattern.append(detected_color)
        current_pattern = current_pattern[-4:]

    adjust_route_based_on_pattern()

    if reflection < TARGET_REFLECTION - 5 or reflection > TARGET_REFLECTION + 5:
        search_for_line()
    else:
        drive_base.drive(LINE_SPEED, turn_rate)

    wait(10)
