# virtual4C

## Description

Plot interaction profiles of an arbitrary viewpoints from a .hic matrix. Example output:

<img src=plot_ARHGEF35_1_5kb.png width="600" height="450" />

## Dependencies

- Python3
- R
- [Juicer Tools JAR](https://github.com/aidenlab/juicer/wiki/Download)

## Contents

**virtual4C.py**: Sums interactions (by default, normalized read counts) for a specified viewpoit in an intrachromosomal interaction matrix.

**virtual4C_plot.R**: Plots virtual 4C profile from Python output.

**v4c.sh**: Wrapper script for plotting virtual 4C profiles for an input .hic matrix and bed file of viewpoints. Usage documented here:

```
./v4c.sh -h
```

**virtual4C-inter.py**: Bonus script for extracting interchromosomal interactions. For example:

```
java -jar juicer_tools.jar dump observed KR https://hicfiles.s3.amazonaws.com/hiseq/gm12878/in-situ/combined.hic 6 16 BP 5000 gm20818_chr6x16_5kb.txt
./virtual4C-inter.py gm20818_chr6x16_5kb.txt 5000 290000 295000 2
```
