#!/bin/env python
# python blast_filter.py -i est.fa -db database.fa -m blastn -len 100 -identity 80 -e 0.00001 -o blast.txt
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='blast query file', required=True)
parser.add_argument('-db', help='blast in file', required=True)
parser.add_argument('-m', help='blast mode', required=True)
parser.add_argument('-len', help='The length of the threshold', required=True)
parser.add_argument('-identity', help='The percentage of consistency of the sequence alignment', required=True)
parser.add_argument('-e', help='E-Value', required=True)
parser.add_argument('-o', help='output file', required=True)

args = parser.parse_args()
Input_Blast = args.i
Build_index = args.db
mode = args.m
Len = args.len
Identity = args.identity
Evalue = args.e
Output = args.o


makeblastdb = '/public/store5/DNA/Test/zhengfuxing/blast/ncbi-blast-2.11.0+/bin/makeblastdb'
os.system('%s \
 -dbtype nucl \
 -in %s \
 -input_type fasta \
 -parse_seqids \
 -out database.fa' 
 %(makeblastdb, Build_index))

print('bulid index finish!\nnow start blast!')

blastn = '/public/store5/DNA/Test/zhengfuxing/blast/ncbi-blast-2.11.0+/bin/' + mode
os.system('%s \
 -query %s \
 -outfmt 6 \
 -db database.fa \
 -out blastn_results.xls \
 -task blastn' 
 %(blastn, Input_Blast,))


f = open('blastn_results.xls', 'r')
f2 = open(Output, 'w')
while True:
    line2 = f.readline()
    if not line2:
        break
    line = line2.split('\t')
    if float(line[2]) >= int(Identity) and int(line[3]) >= Len and float(line[10]) <= Evalue:
        f2.write(line2+'\n')

f.close
f2.close
