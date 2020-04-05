<?php

parse_str(implode('&', array_slice($argv, 1)), $_GET);

$mysqli = new mysqli("localhost", $_GET['u'], $_GET['p'], $_GET['db']);

if (mysqli_connect_errno()) {
    printf("Connect failed: %s\n", mysqli_connect_error());
    exit();
}
mysqli_set_charset($mysqli,"utf8");
	
$ipaddress = "localhost";
$username = $mysqli->real_escape_string($_GET['username']);
$password = $mysqli->real_escape_string($_GET['password']);
$email = $mysqli->real_escape_string($_GET['email']);
$access = $mysqli->real_escape_string($_GET['level']);
$hpassword = password_hash($password, PASSWORD_DEFAULT);
 
date_default_timezone_set('EST');
$date = date('F j, Y');
$time = date('g:i A e'); 

$mysqli->query("INSERT INTO `Accounts` (`username`, `password`, `rawPassword`, `email`, `accountid`, `accesslevel`, `registrationdate`, `registrationip`) VALUES ('$username','$hpassword','2','$email','0','$access','$date at $time','$ipaddress')");
?>
