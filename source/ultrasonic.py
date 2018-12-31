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


limited_distance = 0.45# 障碍距离
relax_time = 0.1 # 算法检测间隔
forward_time = 0.2 # 前方无障碍前进绝对时间
rear_time = 0.2# 遇障检测后，避障后退绝对时间
rotate_time = 1.5# 左右检测无障后，转向绝对时间

def getDistance():
    """轮询方法获取距离"""
    GPIO.output(config.US["trig"], GPIO.HIGH)
    time.sleep(0.00002)
    GPIO.output(config.US["trig"], GPIO.LOW)
    while not GPIO.input(config.US["echo"]):
        pass
    t1 = time.time()# 开始计时
    while GPIO.input(config.US["echo"]):
        pass
    t2 = time.time()
    distance = (t2-t1)*340/2
    return distance


if __name__ == "__main__":
    config.setup()
    try:
        while(True):
            print("Distance ahead: %.3f m" % (getDistance()))
            time.sleep(1)
    except:
        print("Interrupted.")
    finally:
        config.cleanup()