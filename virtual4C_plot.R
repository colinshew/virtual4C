#!/usr/bin/env Rscript

# Plot virtual 4C profile from output of virtual4C.py (read counts per bin)
# Usage:
# Rscript v4c_plot.R {input.v4c.txt} {lib name} {viewpoint chr} {viewpoint start coord} {viewpoint end coord} {res in kb} {viewpoint name}

# parse arguments
args = commandArgs(trailingOnly=TRUE)
profile = read.table(args[1])
lib = args[2]
chr = args[3]
start = as.numeric(args[4])
end = as.numeric(args[5])
res = args[6]
gene = args[7]

# set plot limits within 500 kb of anchor
min = start-200000
max = end+200000

# save plot
png(paste("plot_", gene, "_", res, "kb.png", sep=""), width=800, height=600)
plot(profile, type="l", main=paste(lib, ": anchored at ", chr, ":", start, "-", end, " (", res, " kb)", sep=""), xlab=paste(chr, " coords (bp)", sep=""), ylab="normalized read count", xlim=c(min,max))
invisible(dev.off())
