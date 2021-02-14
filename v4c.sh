#!/bin/bash

# Written by Colin Shew (cshew@ucdavis.edu)
# Updated 13 February 2021

# print help
args=( "$@" )
nArgs=${#args[@]}
if [[ $nArgs -ne 6 ]]; then
	echo -e "Description:"
	echo "v4c.sh takes BED input and plots 4C profiles (normalized read counts) from a .hic file ."
	echo "Usage:"
	echo "./v4c.sh {juicer} {scripts path} {in.hic} {prefix} {in.bed} {resolution}"
	echo "Positional arguments:"
	echo "	juicer          Path to juicer.jar"
	echo "	scripts path    Path to direcotry containing auxiliary scripts"
	echo "	in.hic          Path or URL of input .hic file"
	echo "	prefix          Prefix for output Hi-C text matrices"
	echo "	in.bed          Intervals for generation of 4C plots (must be named or plots will be overwritten)"
	echo "	resolution      Resolution for analysis (bp)"
	exit
fi

# set variables
juicer=$1
scripts=$2
hic=$3
hicBase=$4
bed=$5
res=$6
resKb=`expr $res / 1000`

# virtual 4C for each BED interval
while read line; do
	# parse coordinates
        read chr start end name score str <<< $(echo "$line")
        echo "processing BED entry" $chr":"$start"-"$end "("$name")"
        chrN=$(echo "$chr" | sed 's/chr//g')

        # extract chromosomal matrix
        echo "dumping intrachromosomal matrix..."
	if [ ! -f $hicBase"_"$chr"_"$resKb"kb.txt" ]; then
        	java -jar $juicer dump observed KR $hic $chrN $chrN BP $res $hicBase"_"$chr"_"$resKb"kb.txt"
	fi

        # generate 4C profiles
        echo "extracting virtual 4C profile..."
        python $scripts/virtual4C.py $hicBase"_"$chr"_"$resKb"kb.txt" $res $start $end > $hicBase"_"$chr"_"$start"-"$end"_"$resKb"kb.v4c.txt"

        # plot
        echo "generating plot..."
        Rscript $scripts/virtual4C_plot.R $hicBase"_"$chr"_"$start"-"$end"_"$resKb"kb.v4c.txt" $hicBase $chr $start $end $resKb $name

        echo "done"
        echo -e "\n"
done < $bed
