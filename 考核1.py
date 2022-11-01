#!/bin/env python
# run:
# python fastq2fasta.py -i test.fastq -o test.fasta
# 没有压缩 所以在这里直接使用 fastq 文件
import argparse
import os
parser = argparse.ArgumentParser()

parser.add_argument('-i', help='input *.fastq', required=True)
parser.add_argument('-o', help='output *.fasta', required=True)

args = parser.parse_args()

input = args.i
output = args.o
os.system('module purge')
os.system('module load seqtk')
os.system('seqtk seq -A %s > %s' %(input,output))

os.system('module purge')
