import RPi.GPIO as GPIO
import time

def Setup(GPIOnum, OUT_IN):
    GPIO.setmode(GPIO.BCM)
    if OUT_IN == "OUT":
        GPIO.setup(GPIOnum, GPIO.OUT)
    else:
        GPIO.setup(GPIOnum, GPIO.IN)

def read_water_level(GPIOnum):
    return GPIO.input(GPIOnum)

def main():
    water_sensor_pin = 3
    Setup(water_sensor_pin, "IN")
    
    try:
        while True:
            water_level = read_water_level(water_sensor_pin)
            if water_level == GPIO.HIGH:
                print(water_level,"Water detected")
            else:
                print(0)
            time.sleep(1)  # 每秒檢查一次
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
