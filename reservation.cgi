#!/usr/bin/perl
use strict;
use warnings;
use MySession;

require './template.pl';
my $sess = $main::mysess;

print $sess->header;
&header('予約完了');

if(!defined($sess->params->{'name'})){
	&error("セッションが切れています。お手数ですが再びご入力をお願いします。<br>複数または大量のご予約をご用命の場合は、電話またはメールにてご相談頂ければ幸いでございます。");
	$sess->close;
	$sess->delete;
}
my $s = '","';
my $buff = '"'.$sess->params->{'name'}.$s;
$buff .= $sess->params->{'phone'}.$s;
$buff .= $sess->params->{'mail'}.$s;
$buff .= $sess->params->{'room'}.$s;
$buff .= $sess->params->{'date'}.$s;
$buff .= $sess->params->{'day'}.$s;
$buff .= $sess->params->{'smoke'}.'"'."\n";

open(FH,">>","reserve.cgi");
flock(FH,2);
print FH $buff;
close(FH);

$sess->delete;

print <<"EOF";
<h1>予約完了</h1>
<p>ご予約が完了いたしました。<br>
またのご利用をお待ちしています。</p>
EOF
&footer;
