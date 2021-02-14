#!/usr/bin/env python3

# Author: Colin Shew (cshew@ucdavis.edu)
# Updated 13 February 2020

import argparse
import sys
import csv

def round_down(num, divisor):
	return num-(num%divisor)

def round_up(num, divisor):
	return (num+(divisor-1))//divisor*divisor

# parse arguments
parser = argparse.ArgumentParser(description='Given an intrachromosomal matrix, output a vector of Hi-C read counts per bin from a given viewpoint.')
parser.add_argument('res', metavar='resolution', type=int, help='Resolution (bin size in base pairs)')
parser.add_argument('start', metavar='start', type=int, help='Start coordinate of viewpoint bin')
parser.add_argument('end', metavar='end', type=int, help='End coordinate of viewpoint bin')
parser.add_argument('hic', metavar='matrix', type=str, help='Triangular Hi-C matrix (output of "juicer dump")')
args = parser.parse_args()

start = round_down(args.start, args.res) # start at beginning of bin containing start coord
end = round_up(args.end, args.res) # stop at end of bin containing end coord

# read matrix
print("reading matrix...")
hic = open(args.hic).readlines()

# initialize zero vector of output signal
coord = max(int(binpair.split('\t')[0]) for binpair in hic) # range of bins
nbins = int(float(int(coord) / args.res))
signal = [0]*nbins

# 4C profile
print("extracting signal from viewpoint bins...")
for bin in hic:
	bin = bin.strip('\n').strip('\r')
	bin = bin.split('\t')
	if start <= int(bin[0]) <= end: # assign value from bins matching x-coord to vector, using y-coord
		y = int(float(bin[1]) / args.res)
		if bin[2] != 'NaN':
			signal[y-1] = signal[y-1] + float(bin[2])
	elif start <= int(bin[1]) <= end: # assign value from bins matching y-coord to vector, using x-coord
		y = int(float(bin[0]) / args.res)
		if bin[2] != 'NaN':
                	signal[y-1] = signal[y-1] + float(bin[2])

# create output
print("saving output...")
with open('%s.%s_%s-%s.v4c.txt' % (args.hic.split('.')[0], args.hic.split('.')[1], args.start, args.end), 'w') as csvfile:
	writer = csv.writer(csvfile, dialect='excel-tab')
	bin = 0
	for value in signal:
		bin += args.res
		writer.writerow((bin, value))
