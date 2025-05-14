import pigpio
from time import sleep

#----CONFIGURATION-----
servo_pin = 18  # GPIO18 
min_us = 1500   # PWM left
max_us = 2000   # PWM right
step_us = 50    # Step size in microseconds
delay = 0.5     # Delay between moves

# Initialize pigpio and servo pin
pi = pigpio.pi()
if not pi.connected:
    raise Exception("Check if pigpiod is running.")

try:
    # Generate positions from min to max
    positions = list(range(min_us, max_us + 1, step_us))

    while True:
        # Sweep left to right
        for pos in positions:
            pi.set_servo_pulsewidth(servo_pin, pos)
            sleep(delay)

        sleep(1)

        # Sweep right to left
        for pos in reversed(positions):
            pi.set_servo_pulsewidth(servo_pin, pos)
            sleep(delay)

        sleep(1)

except KeyboardInterrupt:
    print("Servo stopped.")
finally:
    pi.set_servo_pulsewidth(servo_pin, 0)  # Stop sending PWM
    pi.stop()
