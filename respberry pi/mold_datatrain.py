import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib  # 使用 joblib 庫來儲存模型

# 建立與MySQL資料庫的連線
conn = mysql.connector.connect(
    host='172.20.10.3',
    user="ling",
    password="0000",
    database="mold_prediction"
)

# 使用cursor執行SQL查詢
cursor = conn.cursor()

# 執行查詢語句，讀取資料
query = "SELECT Temperature, Humidity, MoldPresence FROM mold_prediction_data_with_timestamps LIMIT 800"
cursor.execute(query)

# 擷取資料
data = cursor.fetchall()

# 取得欄位名稱
columns = [col[0] for col in cursor.description]

# 將資料轉換為特徵(X)和目標值(y)
X_idx_temp = columns.index('Temperature')
X_idx_humi = columns.index('Humidity')
y_idx_target = columns.index('MoldPresence')

X = []
y = []
for row in data:
    X.append([row[X_idx_temp], row[X_idx_humi]])
    y.append(row[y_idx_target])

# 關閉cursor和連線
cursor.close()
conn.close()

# 切分資料為訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 定義要使用的分類器
classifiers = {
    'SVM': SVC(),
    'Random Forest': RandomForestClassifier(),
    'Decision Tree': DecisionTreeClassifier(),
    'ANN': MLPClassifier(),
    'Logistic Regression': LogisticRegression(),
    'Naive Bayes': GaussianNB(),
    'AdaBoost': AdaBoostClassifier(),
    'Gradient Boosting': GradientBoostingClassifier()
}

# 訓練並評估每個分類器的表現
for name, classifier in classifiers.items():
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{name}: Accuracy {accuracy}")
    model_filename = f"{name}_model_project.pkl"  # 檔案名稱可根據模型名稱自行調整
    joblib.dump(classifier, model_filename)
    