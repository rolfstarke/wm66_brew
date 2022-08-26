<html>
<head>
<meta name="viewport" content="width=device-width" />
<title>Schalter</title>
</head>
GPIO 18 schalten:
<form method="get" action="index.php">
<input type=
<input type="submit" value="Licht ein" name="Lichtein">
<input type="submit" value="Licht aus" name="Lichtaus">
</form>
<?php
$modeon18 = trim(@shell_exec("/usr/local/bin/gpio -g mode 18 out"));
if(isset($_GET["Lichtein"])){
	$val = trim(@shell_exec("/usr/local/bin/gpio -g write 18 1"));
	echo "Licht an";
}
else if(isset($_GET["Lichtaus"])){
	$val = trim(@shell_exec("/usr/local/bin/gpio -g write 18 0"));
	echo "Licht aus";
}
?>
</body>
</html>