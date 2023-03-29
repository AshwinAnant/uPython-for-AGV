from machine import Pin, DAC

# Define pins for motor driver
motor_left_forward = Pin(14, Pin.OUT)
motor_left_reverse = Pin(27, Pin.OUT)
motor_right_forward = Pin(12, Pin.OUT)
motor_right_reverse = Pin(13, Pin.OUT)

# Define pins for line sensors
left_sensor = Pin(34, Pin.IN)
right_sensor = Pin(32, Pin.IN)
center_sensor = Pin(36, Pin.IN)
left_most_sensor =Pin(35, Pin.IN)
right_most_sensor =Pin(33, Pin.IN)

