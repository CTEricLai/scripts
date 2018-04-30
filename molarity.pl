#!/usr/bin/perl

$molar = $ARGV[0];
$box_x = $ARGV[1];
$box_y = $ARGV[2];
$box_z = $ARGV[3];

$volume = $box_x * $box_y * $box_z;


$molecules = 6.022 * $volume * $molar / 10000;

printf(" MOLARITY = %8.3f\n", $molar);
printf(" Box size = %8.3f %8.3f %8.3f\n", $box_x, $box_y, $box_z);
printf(" Volume = %8.3f\n", $volume);
printf("\n %8.3f molecules are necessary to make a molarity of %6.2f M\n\n", $molecules, $molar); 
