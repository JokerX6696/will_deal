#!/bin/env python
# python samtools.py -i aligned.sorted.bam -r 1:1000000-2000000 -o out.sam 
from os import system
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='input bam file', required=True)
parser.add_argument('-r', help='input region; such as: -r 1:1000000-2000000', required=True)
parser.add_argument('-o', help='output sam file', required=True)

args = parser.parse_args()
Input = args.i
Output = args.o
Region = args.r

system('samtools view -F 268 %s %s > %s' %(Input, Region, Output))

# 这里只考虑 4 + 8 + 256 



system('module purge')
system('module load samtools')
