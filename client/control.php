<?php
header('Content-Type: text/html; charset=UTF-8');

// 設定伺服器 IP 位址和埠號
$server_ip = '172.20.10.4';  // 將此處替換為伺服器的 IP 位址
$server_port = 8888;  // 將此處替換為伺服器的埠號

if (isset($_POST['action'])) {
    $action = $_POST['action'];

    // 建立 socket 連線
    $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    if ($socket === false) {
        echo "無法建立 socket 連線: " . socket_strerror(socket_last_error()) . PHP_EOL;
        exit;
    }

    // 嘗試連線到伺服器
    $result = socket_connect($socket, $server_ip, $server_port);
    if ($result === false) {
        echo "無法連線到伺服器: " . socket_strerror(socket_last_error($socket)) . PHP_EOL;
        exit;
    }

    // 要傳送的資料
    $data_to_send = $action;

    // 將資料傳送到伺服器
    socket_write($socket, $data_to_send, strlen($data_to_send));

    echo "已傳送資料到伺服器: $data_to_send" . PHP_EOL;

    // 接收來自伺服器的回應
    if ($action == 'getth') {
        $response = socket_read($socket, 1024);
        echo "從伺服器接收到的資料: $response" . PHP_EOL;
    }

    // 關閉 socket 連線
    socket_close($socket);
}
?>
