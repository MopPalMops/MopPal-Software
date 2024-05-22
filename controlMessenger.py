import pygame
import serial
import time

ser = serial.Serial('COM3', 9600) # Replace 'COM3' with the correct port for your device

MAX_JOYSTICK_VALUE = 1.0
MIN_JOYSTICK_VALUE = -1.0

DEBOUNCE_DELAY = 0.2

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def log_ps4_controller_input():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No controllers found.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Listening for PS4 controller input...")
    
    last_input_time = time.time()

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 0 or event.axis == 1:
                        x_value = joystick.get_axis(0)
                        y_value = joystick.get_axis(1)
                        
                        if (abs(x_value) >= 0.5 or abs(y_value) >= 0.5) and (y_value < 0.1):
                            if time.time() - last_input_time > DEBOUNCE_DELAY:
                                if abs(x_value) < 0.1:
                                    gpio1_percentage = map_value(abs(y_value), MIN_JOYSTICK_VALUE, MAX_JOYSTICK_VALUE, 0, 100)
                                    gpio2_percentage = map_value(abs(y_value), MIN_JOYSTICK_VALUE, MAX_JOYSTICK_VALUE, 0, 100)
                                else:
                                    percentage_x = map_value(abs(x_value), MIN_JOYSTICK_VALUE, MAX_JOYSTICK_VALUE, 0, 100)
                                    percentage_y = map_value(y_value, MIN_JOYSTICK_VALUE, MAX_JOYSTICK_VALUE, 0, 100)
                                    
                                    if x_value >= 0:
                                        gpio1_percentage = percentage_x
                                        gpio2_percentage = percentage_y
                                    else:
                                        gpio1_percentage = percentage_y
                                        gpio2_percentage = percentage_x

                                data_to_send = f"GPIO1: {gpio1_percentage}%, GPIO2: {gpio2_percentage}%"
                                print(data_to_send)
                                ser.write(data_to_send.encode())
                                
                                last_input_time = time.time()

                elif event.type == pygame.JOYBUTTONDOWN:
                    pass
                elif event.type == pygame.JOYBUTTONUP:
                    pass
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        pygame.quit()
        ser.close()

if __name__ == "__main__":
    log_ps4_controller_input()
