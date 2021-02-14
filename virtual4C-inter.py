#!/usr/bin/env python3

# Author: Colin Shew (cshew@ucdavis.edu)
# Updated: 13 Feb 2021

import argparse
import sys
import csv

def round_down(num, divisor):
	return num-(num%divisor)

def round_up(num, divisor):
	return (num+(divisor-1))//divisor*divisor

# parse arguments
parser = argparse.ArgumentParser(description='Given an interchromosomal matrix, output a vector of Hi-C read counts per bin from a given viewpoint on a different chromosome.')
parser.add_argument('res', metavar='resolution', type=int, help='Resolution (bin size in base pairs)')
parser.add_argument('start', metavar='start', type=int, help='Start coordinate of viewpoint bin')
parser.add_argument('end', metavar='end', type=int, help='End coordinate of viewpoint bin')
parser.add_argument('hic', metavar='matrix', type=str, help='Rectangular Hi-C matrix (output of "juicer dump" between chromosomes)')
parser.add_argument('col', metavar='column', type=str, help='Column containing chromosome on which viewpoint is located (1 or 2). For example,  dumping the chr 6x16 matrix gives chr16 in col1 and chr6 in col2.')
args = parser.parse_args()

start = round_down(args.start, args.res) # start at beginning of bin containing start coord
end = round_up(args.end, args.res) # stop at end of bin containing end coord

# read input
print("reading matrix...")
hic = open(args.hic).readlines()

# initialize zero vector to store output
if args.col == "1": # if anchoring on chr in col1, need output in length of chr in col2
	lastbin = max(int(xcoord.split('\t')[1]) for xcoord in hic)
elif args.col == "2": # if anchoring on chr in col2, need output in length of chr in col1
	lastbin = max(int(ycoord.split('\t')[0]) for ycoord in hic)
else:
	sys.exit("ERROR: enter column 1 or 2 for viewpoint chromosome")
nbins = int(lastbin / args.res) # x coordinate of last bin / resolution (should end up in increments of 1)
signal = [0]*nbins

# 4C profile
print("extracting signal from viewpoint bins...")
for bin in hic:
	bin = bin.strip('\n').strip('\r')
	bin = bin.split('\t')
	if sys.argv[5] == "1":
                if start <= int(bin[0]) <= end: # only for bins within the anchor (x)
                        y = int(float(bin[1]) / args.res) # y-coordinate
                        if bin[2] != 'NaN':
                                signal[y-1] = signal[y-1] + float(bin[2]) # add signal value to x-coordinate
	elif sys.argv[5] == "2": # anchor in col2
		if start <= int(bin[1]) <= end: # only for bins within the anchor (y)
			x = int(float(bin[0]) / args.res) # x-coordinate
			if bin[2] != 'NaN':
				signal[x-1] = signal[x-1] + float(bin[2]) # add signal value to x-coordinate

# write output
print("saving output...")
with open('%s.%s_%s-%s.v4c.txt' % (args.hic.split('.')[0], args.hic.split('.')[1], args.start, args.end), 'w') as csvfile:
	writer = csv.writer(csvfile, dialect='excel-tab')
	bin = 0
	for value in signal:
		bin += args.res
		writer.writerow((bin, value))
