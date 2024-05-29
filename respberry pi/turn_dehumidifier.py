import socket
import threading
import RPi.GPIO as GPIO
import Adafruit_DHT
from datetime import datetime

# 設置GPIO引腳
RED_LED = 2  # 除濕機控制引腳
WATER_SENSOR = 3  # 水位偵測器引腳
DHT_SENSOR = Adafruit_DHT.DHT11  # 選擇你的DHT傳感器類型(DHT11或DHT22)
DHT_PIN = 14  # 溫溼度感應器引腳

GPIO.setwarnings(False)  # 禁用 GPIO 通道警告
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(WATER_SENSOR, GPIO.IN)

# 全局變量來控制水位檢查線程
stop_water_check = threading.Event()

def turn_on_led(led_pin):
    GPIO.output(led_pin, GPIO.HIGH)

def turn_off_led(led_pin):
    GPIO.output(led_pin, GPIO.LOW)

def read_water_sensor(sensor_pin):
    return GPIO.input(sensor_pin)  # 讀取水位偵測器的值

def read_dht_sensor(sensor, pin):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return humidity, temperature

def check_water_level():
    while not stop_water_check.is_set():
        water_level = read_water_sensor(WATER_SENSOR)
        if water_level == GPIO.LOW:  # 如果無水，關閉除濕機
            print("無水，關閉除濕機")
            turn_on_led(RED_LED)
            stop_water_check.set()
        stop_water_check.wait(1)  # 每秒檢查一次水位

server_ip = '172.20.10.4'
server_port = 8888

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((server_ip, server_port))
server.listen(5)
print(f"伺服器已啟動，監聽在 {server_ip}:{server_port}")

try:
    while True:
        client_socket, client_address = server.accept()
        print(f"與客戶端 {client_address} 建立連線")

        while True:
            data = client_socket.recv(1024)
            if data:
                command = data.decode().strip()
                print(f"收到來自客戶端的資料：{command}")

                if command == 'ron':
                    print("開啟除濕機")
                    turn_off_led(RED_LED)
                    # 開始水位檢查線程
                    stop_water_check.clear()
                    water_check_thread = threading.Thread(target=check_water_level)
                    water_check_thread.start()
                elif command == 'rof':
                    print("關閉除濕機")
                    turn_on_led(RED_LED)
                    # 停止水位檢查線程
                    stop_water_check.set()
                elif command == 'get_water_level':
                    water_level = read_water_sensor(WATER_SENSOR)
                    water_status = "有水" if water_level == GPIO.HIGH else "無水"
                    client_socket.sendall(water_status.encode())
                    print(f"已回傳水位狀態給客戶端：{water_status}")
                elif command == 'get_th':
                    humidity, temperature = read_dht_sensor(DHT_SENSOR, DHT_PIN)
                    th_data = f"Temperature: {temperature:.2f} C, Humidity: {humidity:.2f}%"
                    client_socket.sendall(th_data.encode())
                    print(f"已回傳溫溼度給客戶端：{th_data}")
                break  # 收到資料後中斷當前連線並等待新的連線

        client_socket.close()
except Exception as e:
    print(f"錯誤發生: {e}")
finally:
    server.close()
    GPIO.cleanup()

