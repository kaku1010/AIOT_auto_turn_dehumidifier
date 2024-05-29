import joblib
import mysql.connector
import time
import Adafruit_DHT
import RPi.GPIO as GPIO
import LED  # 导入 LED 模块

# 建立与 MySQL 数据库的连接
conn = mysql.connector.connect(
    host='172.20.10.3',
    user='ling',
    password='0000',
    database='mold_prediction'
)

# 使用 cursor 执行 SQL 查询
cursor = conn.cursor()

# 加载预训练的 SVM 模型
model_filename_updated = "SVM_model_project.pkl"
classifier_updated = joblib.load(model_filename_updated)

# 温湿度传感器引脚设置
sensor = Adafruit_DHT.DHT11
GPIO_PIN = 14


def read_water_level(GPIOnum):
    return GPIO.input(GPIOnum)

try:
    LED.Setup(2, "OUT")
    LED.Setup(3, "IN")

    while True:
        currentTime = time.strftime("%Y-%m-%d %H:%M:%S")  # 使用完整的时间戳格式
        
        humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO_PIN)
        
        if humidity is not None and temperature is not None:
            temperature = float(temperature)
            humidity = float(humidity)
            print(currentTime, '-> Temp={0:.2f}*C Humidity={1:.2f}%'.format(temperature, humidity))

            # 获取温度和湿度数据进行预测
            X_latest = [[temperature, humidity]]
            prediction = classifier_updated.predict(X_latest)
            print(f"Prediction: {prediction}")
            
            insert_query = (
                "INSERT INTO mold_prediction_data_with_timestamps (Timestamp, Temperature, Humidity, MoldPresence) "
                "VALUES (%s, %s, %s, %s)"
            )
            data = (currentTime, temperature, humidity, int(prediction[0]))
            cursor.execute(insert_query, data)
            conn.commit()
            
           
           # 根据预测结果控制LED
            if prediction[0] == 1:
                LED.TurnOffLED(2)  # 打开LED，表示启动抽水

                # 检查水位传感器，等待水位降低
                while True:
                    water_level = read_water_level(3)
                    if water_level == GPIO.LOW:  # 假设LOW表示无水
                        print("No water detected")
                        LED.TurnOnLED(2)  # 关闭LED，表示停止抽水
                        break
                    else:
                        print("Water detected")
                    time.sleep(1)  # 每秒检查一次
            else:
                print("沒有發霉別擔心")
        else:
            print('Failed to get reading. Try again!')

        time.sleep(5)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # 关闭 cursor 和连接
    if conn.is_connected():
        cursor.close()
        conn.close()
    GPIO.cleanup()
