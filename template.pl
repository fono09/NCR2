our $mysess = MySession->new(
	name => 'RESERVE_SYSTEM',
	dir => './tmp',
	expire => '+1h',
);

sub header{
	my ($msg) = @_;
	return <<"EOF";
<html>
<head>
<title>予約システム | $msg</title>
</head>
<body>
EOF
}

sub footer{
	print <<'EOF'
</body>
</html>
EOF
}

sub error{
	my ($msg) = @_;
	&header('エラー');
	print "<p>$msg</p>";
	&footer;
	$mysess->close;
	$mysess->delete;
	die "$msg";
}


1;
