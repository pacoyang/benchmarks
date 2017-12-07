<?php
$port = 8080;
$http = new swoole_http_server('127.0.0.1', $port);
$responses = [];

$http->on('start', function ($server) {
    global $port;
    echo "Swoole http server is started at http://127.0.0.1:$port\n";
});

$http->on('request', function ($request, $response) {
    global $responses;
    $msize = 1024;
    if (!array_key_exists($msize, $responses)) {
      $responses[$msize] = str_repeat('X', $msize);
    }
    $response->end($responses[$msize]);
});

$http->start();
