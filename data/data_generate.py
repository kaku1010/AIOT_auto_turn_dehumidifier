import csv
import random
from datetime import datetime, timedelta

# 設定隨機種子以保證結果可重現
random.seed(42)

# 生成2000筆數據
num_samples = 2000

# 生成溫度範圍為 10 到 40 攝氏度的隨機數據，並保留兩位小數
temperatures = [round(random.uniform(10, 40), 2) for _ in range(num_samples)]

# 生成濕度範圍為 20% 到 100% 的隨機數據，並保留兩位小數
humidities = [round(random.uniform(20, 100), 2) for _ in range(num_samples)]

# 根據條件判斷是否會發霉
mold_presence = [
    1 if (10 <= temp <= 35) and (humidity > 50) and (20 <= temp <= 30) else 0
    for temp, humidity in zip(temperatures, humidities)
]

# 生成從2024年5月1日開始的時間戳，間隔為每分鐘
start_date = datetime(2024, 5, 1)
timestamps = [start_date + timedelta(minutes=i) for i in range(num_samples)]

# 定義CSV文件路徑
file_path = 'mold_prediction_data_with_timestamps.csv'

# 將數據寫入CSV文件
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Temperature', 'Humidity', 'MoldPresence'])
    for timestamp, temp, humidity, mold in zip(timestamps, temperatures, humidities, mold_presence):
        writer.writerow([timestamp.strftime('%Y-%m-%d %H:%M:%S'), temp, humidity, mold])

print(f'CSV文件已生成：{file_path}')
