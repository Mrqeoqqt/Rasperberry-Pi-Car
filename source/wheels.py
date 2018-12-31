import time

import platform
if platform.system() == "Windows":
    from RaspPi import config
elif platform.system() == "Linux":
    import config
else:
    print("Invalid operating system.")
    exit(-1)

try:
    import RPi.GPIO as GPIO
except:
    print("""Error importing RPi.GPIO!""")
    exit(-1)

duration = 0.2


def Left(speed):
    """
    turn left
    wheels on left stop,
    wheels on right continue
    """
    # print("Turn left, speed", speed)
    config.PWMs[0].ChangeDutyCycle(0.1)
    config.PWMs[1].ChangeDutyCycle(float(speed) * 5)


def LeftBack(speed):
    """
    turn left
    wheels on right stop,
    wheels on left go backward
    """
    # print("Turn left back, speed", speed)
    config.PWMs[2].ChangeDutyCycle(0.1)
    config.PWMs[3].ChangeDutyCycle(float(speed) * 5)


def LeftRelease():
    # print("Turn left stopped.")
    config.PWMs[0].ChangeDutyCycle(0)
    config.PWMs[1].ChangeDutyCycle(0)
    config.PWMs[2].ChangeDutyCycle(0)
    config.PWMs[3].ChangeDutyCycle(0)


def Right(speed):
    """
    turn right
    wheels on right stop,
    wheels on right continue
    """
    # print("Turn right, speed", speed)
    config.PWMs[2].ChangeDutyCycle(float(speed) * 5)
    config.PWMs[3].ChangeDutyCycle(0.1)


def RightBack(speed):
    """
    turn right
    wheels on left stop,
    wheels on right go backward
    """
    # print("Turn right back, speed", speed)
    config.PWMs[0].ChangeDutyCycle(float(speed) * 5)
    config.PWMs[1].ChangeDutyCycle(0.1)


def RightRelease():
    # print("Turn right stopped.")
    config.PWMs[0].ChangeDutyCycle(0)
    config.PWMs[1].ChangeDutyCycle(0)
    config.PWMs[2].ChangeDutyCycle(0)
    config.PWMs[3].ChangeDutyCycle(0)


def Forward(speed):
    # print("Go forward, speed", speed)
    config.PWMs[0].ChangeDutyCycle(0.1)
    config.PWMs[1].ChangeDutyCycle(float(speed) * 5)
    config.PWMs[2].ChangeDutyCycle(float(speed) * 5)
    config.PWMs[3].ChangeDutyCycle(0.1)


def ForwardRelease():
    # print("Go forward stopped.")
    config.PWMs[0].ChangeDutyCycle(0)
    config.PWMs[1].ChangeDutyCycle(0)
    config.PWMs[2].ChangeDutyCycle(0)
    config.PWMs[3].ChangeDutyCycle(0)


def Backward(speed):
    # print("Go backward, speed", speed)
    config.PWMs[0].ChangeDutyCycle(float(speed) * 5)
    config.PWMs[1].ChangeDutyCycle(0.1)
    config.PWMs[2].ChangeDutyCycle(0.1)
    config.PWMs[3].ChangeDutyCycle(float(speed) * 5)


def BackwardRelease():
    # print("Go backward stopped.")
    config.PWMs[0].ChangeDutyCycle(0)
    config.PWMs[1].ChangeDutyCycle(0)
    config.PWMs[2].ChangeDutyCycle(0)
    config.PWMs[3].ChangeDutyCycle(0)


if __name__ == "__main__":
    config.setup()
    # Left(5.0)
    # time.sleep(2)
    # LeftRelease()
    # Right(5.0)
    # time.sleep(2)
    # RightRelease()
    LeftBack(5.0)
    time.sleep(2)
    LeftRelease()
    RightBack(5.0)
    time.sleep(2)
    RightRelease()
    config.cleanup()

