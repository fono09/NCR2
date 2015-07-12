#!/usr/bin/perl
use strict;
use warnings;

use Time::Piece;
use MySession;
use Data::Dumper;

require './template.pl';
my $sess = $main::mysess;

print $sess->header;
&header('確認画面');

use constant ROOM => ('シングル(7,000円)',' ツイン(12,000円)','ダブル(15,000円)','デラックスツイン(21,000円)','スイート(35,000円)');

#Validate params
my $t=localtime;
my $i;
eval{$i=Time::Piece->strptime($sess->params->{'date'},"%Y/%m/%d")};
&error("チェックイン日を正しく入力してください") if @_;

$sess->params->{'name'} =~ s/\s//g;
$sess->params->{'phone'} =~ s/[^\d\s-]//g;
$sess->params->{'day'} = int $sess->params->{'day'};

if($sess->params->{'name'} eq ""){
	&error("名前を正しく入力してください");
}elsif($sess->params->{'phone'} !~ /(\d+|-+)/){
	&error("電話番号を正しく入力してください");
}elsif($sess->params->{'mail'} !~ /\w+\@\w+[\.\w]+/){
	&error("メールアドレスを正しく入力してください");
}elsif($sess->params->{'day'} < 1 || $sess->params->{'day'} =~ /\d{2}/ || $sess->params->{'day'} > 9){
	&error("宿泊数を正しく入力してください<br>尚、宿泊数は10日以下となっておりますので予めご了承くださいませ");
}elsif($sess->params->{'date'} !~ /(\d{4})\/(\d{2})\/(\d{2})/){
	&error("チェックイン日を正しく入力してください");
}elsif($t > $i){
	&error("過去の予約は受け付けておりません");
}

print <<EOF;
<h1>以下の内容で予約してもよろしいでしょうか</h1>
<p>
お客様のお名前とご連絡先<br>
お名前:@{[$sess->params->{'name'}]}<br>
電話番号:@{[$sess->params->{'phone'}]}<br>
メールアドレス:@{[$sess->params->{'mail'}]}
</p>

<p>
チェックインされる日・宿泊数</br>
チェックイン日:@{[$sess->params->{'date'}]}<br>
宿泊数:@{[$sess->params->{'day'}]}
</p>

<p>
部屋の種類と料金<br>
@{[(ROOM)[$sess->params->{'room'}]]}
</p>

<p>禁煙ルームのご希望<br>
@{[$sess->params->{'smoke'}==0?"どちらでも良い":"禁煙ルーム"]}
</p>
<form method="POST" action="reservation.cgi">
<input type="submit" value="送信">
EOF
$sess->flush;

&footer;
