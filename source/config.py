try:
    import RPi.GPIO as GPIO
except:
    print("""Error importing RPi.GPIO!""")

# freq of PWM
frequency = 100
# GPIO ports
wheels = [2, 3, 5, 6]
# IN1: 2, left+front
# IN2: 3, left+hind
# IN3: 4, right+front
# IN4: 17, right+hind
PWMs = []
IR = {'LU': 27, 'LL': 22, 'RU': 23, 'RL': 24}
# IR: infrared
# LU: left+upper, LL: left+lower, RU: right+upper, RL: right+lower
US = {'echo': 10, 'trig': 9}
# US: ultrasonic


def setup():
    print("Setup!")
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    # BroadCom Mode / GPIO numbering
    GPIO.setup(wheels, GPIO.OUT)
    for i in wheels:
        p = GPIO.PWM(i, frequency)
        PWMs.append(p)
        p.start(0)
    for i in IR.values():
        GPIO.setup(i, GPIO.IN)
    GPIO.setup(US['echo'], GPIO.IN)
    GPIO.setup(US['trig'], GPIO.OUT)



def cleanup():
    print("Clean up!")
    GPIO.output(US["trig"], GPIO.LOW)
    for w in PWMs:
        w.stop()
    GPIO.cleanup()



