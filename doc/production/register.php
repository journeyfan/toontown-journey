<?php
$mysqli = new mysqli("localhost", "toontown", "xxxx", "toontown");
if (mysqli_connect_errno()) {
    printf("Connect failed: %s\n", mysqli_connect_error());
    exit();
}
mysqli_set_charset($mysqli,"utf8");
	
if (getenv('HTTP_CLIENT_IP')) {
	$ipaddress = getenv('HTTP_CLIENT_IP');
} elseif (getenv('HTTP_X_FORWARDED_FOR')) {
	$ipaddress = getenv('HTTP_X_FORWARDED_FOR');
} elseif (getenv('HTTP_X_FORWARDED')) {
	$ipaddress = getenv('HTTP_X_FORWARDED');
} elseif (getenv('HTTP_FORWARDED_FOR')) {
	$ipaddress = getenv('HTTP_FORWARDED_FOR');
} elseif (getenv('HTTP_FORWARDED')) {
	$ipaddress = getenv('HTTP_FORWARDED');
} elseif (getenv('REMOTE_ADDR')) {
	$ipaddress = getenv('REMOTE_ADDR');
} else {
	$ipaddress = 'UNKNOWN';
}


$username = $mysqli->real_escape_string($_POST['username']);
$password = $mysqli->real_escape_string($_POST['password']);
$email = $mysqli->real_escape_string($_POST['email']);
$hpassword = password_hash($password, PASSWORD_DEFAULT);
 
date_default_timezone_set('EST');
$date = date('F j, Y');
$time = date('g:i A e'); 

$mysqli->query("INSERT INTO `Accounts` (`username`, `password`, `rawPassword`, `email`, `accountid`, `accesslevel`, `registrationdate`, `registrationip`) VALUES ('$username','$hpassword','2','$email','0','100','$date at $time','$ipaddress')");
?>
