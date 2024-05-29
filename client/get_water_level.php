<?php
// 设置服务器IP和端口
$server_ip = '172.20.10.4';
$server_port = 8888;

// 创建socket连接
$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
if ($socket === false) {
    die("無法建立socket連線: " . socket_strerror(socket_last_error()));
}

// 连接到服务器
$result = socket_connect($socket, $server_ip, $server_port);
if ($result === false) {
    die("無法連線到伺服器: " . socket_strerror(socket_last_error($socket)));
}

// 发送获取水位状态命令
$command = 'get_water_level';
socket_write($socket, $command, strlen($command));

// 接收服务器响应
$response = socket_read($socket, 1024);

// 关闭socket连接
socket_close($socket);

// 输出响应
echo $response;
?>
