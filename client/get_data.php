<?php
// 資料庫連線設定
$servername = "localhost"; // 請根據你的設定修改
$username = "ling"; // 請填入你的資料庫用戶名
$password = "0000"; // 請填入你的資料庫密碼
$dbname = "mold_prediction"; // 請填入你的資料庫名稱

// 建立資料庫連線
$conn = new mysqli($servername, $username, $password, $dbname);

// 檢查連線是否成功
if ($conn->connect_error) {
    die("連線失敗: " . $conn->connect_error);
}

// 準備 SQL 語句，獲取最近100筆溫度和濕度數據
$sql = "SELECT Timestamp,Temperature,Humidity FROM mold_prediction_data_with_timestamps ORDER BY Timestamp DESC LIMIT 200";
$result = $conn->query($sql);

// 將結果轉換為JSON格式並返回給網頁
$data = array();
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $data['labels'][] = $row['Timestamp'];
        $data['temperature'][] = $row['Temperature'];
        $data['humidity'][] = $row['Humidity'];
    }
}
// 反轉數據以按照時間順序顯示
$data['labels'] = array_reverse($data['labels']);
$data['temperature'] = array_reverse($data['temperature']);
$data['humidity'] = array_reverse($data['humidity']);

echo json_encode($data);

// 關閉資料庫連線
$conn->close();
?>
