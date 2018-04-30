#!/usr/bin/perl

for($i=1;$i<=9;$i++){
	$infile=$ARGV[0].".".$i.".out";
	$outfile=$ARGV[0].".".$i.".dvdl.out";
	open(OUT,">$outfile");
	open(IN,"$infile");

	$tag=0;
	while(<IN>){
		if($tag==1 && !/End\sof\sdvdl\ssummary/){
			print OUT $_;
		}	
		if(/End\sof\sdvdl\ssummary/){
			$tag=0;
		}
		if(/Summary\sof\sdvdl\svalues\sover/){
			$tag=1;
		}
	}
	print "$infile done\n"; 
	close OUT;
	close IN;
}

