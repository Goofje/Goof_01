def detect_dead_end_and_turn():
    # Draai in stappen om de lijn te zoeken
    initial_angle = robot.angle()
    while True:
        # Controleer of de robot 90 graden heeft gedraaid zonder de lijn te vinden
        if abs(robot.angle() - initial_angle) >= 90:
            # Stop en draai om zijn as totdat de blauwe lijn gevonden is
            robot.stop()
            turn_until_line_found()
            break
        else:
            # Blijf draaien in de zoektocht naar de lijn
            robot.drive(0, turn_rate)  # Draai op de plek

def turn_until_line_found():
    robot.drive(0, turn_rate)  # Begin met draaien
    while color_sensor.color() != line_color:
        # Wacht totdat de kleursensor blauw detecteert
        wait(10)  # Check elke 10 milliseconden om niet te veel CPU-tijd te gebruiken
    robot.stop()  # Stop met draaien zodra de lijn gevonden is

