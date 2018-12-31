import time
import platform
if platform.system() == "Windows":
    from RaspPi import config
    from RaspPi import wheels, infrared, ultrasonic, GUI
elif platform.system() == "Linux":
    import config
    import wheels, infrared, ultrasonic, GUI
else:
    print("Invalid operating system.")
    exit(-1)

try:
    import RPi.GPIO as GPIO
except:
    print("""Error importing RPi.GPIO!""")
    exit(-1)


def algorithm(speed):
    """
    1. Detect the distance from obstacle ahead.
    2. If distance > limited_distance
           2.1 if left is not blocked and right is blocked
                turn left for rotate_time secs
           2.2 if right is not blocked and left is blocked
                turn left for rotate_time secs
           2.3 if left is not blocked and right is not blocked
               go forward for forward_time secs
           2.4 if left is blocked and right is blocked
                U-turn
    3. Else, go Backward for rear_time
       and detect distance from obstacles aside.
           3.1 If left is not blocked,
               try turn leftback for rotate_time secs,
           3.2 else if right is doable
               try turn rightback for rotate_time secs,
           3.3 else,
               go Backward for rear_time
    :param speed: current speed of the car
           PWM = speed * 5
    :return: None
    """
    dis = ultrasonic.getDistance()
    left_doable, right_doable = lrDoable()
    # print("Algorithm begins, distance ahead:", dis)
    if dis > ultrasonic.limited_distance:
        if left_doable and (not right_doable):
            wheels.LeftBack(speed)
            time.sleep(ultrasonic.rotate_time)
            wheels.LeftRelease()
        elif (not left_doable) and right_doable:
            wheels.RightBack(speed)
            time.sleep(ultrasonic.rotate_time)
            wheels.RightRelease()
        elif left_doable and right_doable:
            wheels.Forward(speed)
            time.sleep(ultrasonic.forward_time)
            wheels.ForwardRelease()
        else:
            wheels.RightBack(speed)
            time.sleep(2*ultrasonic.rotate_time)
            wheels.RightRelease()
    else:
        # print("Obstacle ahead detected.")
        wheels.Backward(speed)
        time.sleep(ultrasonic.rear_time)
        wheels.BackwardRelease()
        detectLR(speed)



def detectLR(speed):
    """
    :param speed: current speed
    :param once: if is in Step 2
    :return:
    """
    # print("Detect obstacles on the left and right.")
    left_doable, right_doable = lrDoable()
    if left_doable:
        # print("Blocked ahead, turn left.")
        wheels.LeftBack(speed)
        time.sleep(ultrasonic.rotate_time)
        wheels.LeftRelease()
    elif right_doable:
        # print("Blocked ahead/left, turn right.")
        wheels.RightBack(speed)
        time.sleep(ultrasonic.rotate_time)
        wheels.RightRelease()
    else:
        # print("Blocked ahead/left/right, go Backward.")
        wheels.Backward(speed)
        time.sleep(ultrasonic.rear_time)
        wheels.BackwardRelease()
    time.sleep(ultrasonic.relax_time)


def lrDoable():
    left_distance = infrared.isBlocked("LU")
    right_distance = infrared.isBlocked("RU")
    return left_distance, right_distance


def start(speed, duration=20):
    start_time = time.time()
    while (True):
        algorithm(5)
        time.sleep(0.1)
        if time.time() - start_time > duration:
            # default : duration of Obstacle Mode = 20 seconds
            break

def stop():
    GPIO.output(config.US["trig"], GPIO.LOW)
    for w in config.PWMs:
        w.ChangeDutyCycle(0)

if __name__ == "__main__":
    config.setup()
    try:
        while(True):
            algorithm(4)
            time.sleep(0.2)
    except:
        print("Interrupted.")
    finally:
        stop()
        config.cleanup()