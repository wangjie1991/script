#!/usr/bin/env perl
use strict;
use threads;
use threads::shared;

my $CMD = "./compfeat -config fbanks.cfg -S INPUTSCP";
if(@ARGV != 2)
{
	die "perl $0 [(IN)featlist] [(IN)Thread_Num]\n";
}

my ($in,$threadNum) = @ARGV;

open(IN,"$in") || die "cannot open $in\n";
my @feat = <IN>;
my $each = int(($#feat+1)/$threadNum);
my $prev = 0;
my $i = 1;
for(;$i < $threadNum; $i++)#split featlist
{
	open(PO,">$in\.$i") || die "cannot open $in\.$i\n";
	print "[$i]$in\.$i\n";
	my $j = $prev;
	for(; $j < $prev + $each; $j++)
	{
		print PO "$feat[$j]";
	}
	close(PO);
	$prev = $j;
}
##############
# last slice #
##############
print "[$i]$in\.$i\n";
open(PO,">$in\.$i") || die "cannot open $in\.$i\n";
for(my $j = $prev; $j < @feat; $j++)
{
	print PO "$feat[$j]";
}
close(PO);

my @threadList = [];
for(my $i = 1; $i <= $threadNum; $i++)
{
	my $pd = fork();
	if($pd)
	{
		push(@threadList,$pd);
	}
	elsif($pd == 0)
	{
		my $curCMD = $CMD;
		$curCMD =~ s/INPUTSCP/$in\.$i/g;
		$curCMD .= " > fe.log.$i 2>&1";
		print "$curCMD\n";
		`$curCMD`; # execute sub thread.
		exit 0;
	}
	else
	{
		die "ERROR: Fork error!";
	}
}

for(my $i = 0; $i < $#threadList; $i++)
{
	my $num = waitpid($threadList[$i],0);
}

########################################
#              clearing                #
########################################
`rm -f $in\.\*`;
`rm -f fe.log.\*`;
print "[SUCCESS] Feature extraction Finished\n";
