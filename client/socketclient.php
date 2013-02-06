<?php

define('PPY_HOST', '127.0.0.1');
define('PPY_PORT', '32123');
define('PPY_RECVBUFFER', 1024);

function exchange($entry='', $func='', $param=array()){
	if (!isset($entry{0}) || !isset($func{0})){
		die('PPY ERROR[PHP]: PARAM entry && func must be specified');
	}
	if (!is_array($param)){
		die('PPY ERROR[PHP]: PARAM param must be an array');
	}
	
	$c = socket_create(AF_INET, SOCK_STREAM, 0);
	if (socket_connect($c, PPY_HOST, PPY_PORT) === false){
		die('PPY ERROR[PHP]: socket_connect() error');
	};
	$send = json_encode(array('entry' => $entry, 'func' => $func, 'param' => $param));
	$sendsize = strlen($send);
	$sendsize .= '.';
	if (strlen($sendsize) > 11){
		die('PPY ERROR[PHP]: Too much data.');
	}
	while (strlen($sendsize) < 11){
		$sendsize .= '0';
	}
	$send = $sendsize . $send;
	
	if (socket_write($c, $send) === false){
		die('PPY ERROR[PHP]: socket_write() error');
	}
	
	if (($datasize = socket_read($c, 11)) === false){
		die('PPY ERROR[PHP]: socket_read() error');
	}
	$data = '';
	do {
		if (($recv = socket_read($c, PPY_RECVBUFFER)) === false){
			die('PPY ERROR[PHP]: socket_read() error');
		}
		$datasize -= PPY_RECVBUFFER;
		$data .= $recv;
	}
	while ($datasize > 0);
	socket_close($c);
	return $data;
}
