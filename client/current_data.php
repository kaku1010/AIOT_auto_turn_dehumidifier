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

// 準備 SQL 語句，獲取最新的溫度和濕度數據
$sql = "SELECT Timestamp, Temperature, Humidity FROM mold_prediction_data_with_timestamps ORDER BY Timestamp DESC LIMIT 1";
$result = $conn->query($sql);

// 將結果轉換為JSON格式並返回給網頁
$data = array();
if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    $data['timestamp'] = $row['Timestamp'];
    $data['temperature'] = $row['Temperature'];
    $data['humidity'] = $row['Humidity'];
} else {
    $data['error'] = "No data found";
}
echo json_encode($data);

// 關閉資料庫連線
$conn->close();
?>
