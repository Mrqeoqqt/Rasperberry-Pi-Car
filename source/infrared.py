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


def isBlocked(name):
    """
    if GPIO.input(config.IR['LU']) == GPIO.HIGH:
        left side is not blocked
    elif GPIO.input(config.IR['RU']) == GPIO.HIGH:
        right side is not blocked
    :param name: name = 'LU' / 'LL' / 'RU' / 'RL'
    :return:
    """
    return (GPIO.input(config.IR[name]) == GPIO.HIGH)


if __name__ == "__main__":
    config.setup()
    try:
        while(True):
            if isBlocked("LU"):
                print("Left side is not blocked.")
            else:
                print("Left side is blocked.")
            time.sleep(1)
    except:
        print("Interrupted.")
    finally:
        config.cleanup()
