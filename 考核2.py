#!/bin/env python
# python fasta_stat.py -i genome.fa -o stat.txt
# 该脚本使用了字典 若想知道 n50 对应的 contigs 名称 => Contig_Name 
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='input *.fastq', required=True)
parser.add_argument('-o', help='output *.fasta', required=True)
args = parser.parse_args()

Input = args.i
Output = args.o
stat = {}
StrNum = 0
Name = 'None'
NumLine = 0
GC_num = 0
with open(Input, 'r') as f:
    while True:
        line = f.readline()
        if not line:
            stat[Name] = StrNum  # 防止最后一个 contig 损失
            break
        elif ">" in line:
            NumLine += 1
            if StrNum != 0:
               stat[Name] = StrNum
            Name = re.match(">.*\.\d", line).group().replace('>', '')
            StrNum = 0
        else:
            StrNum += len(line)-1  # 换行符也算一个字节
            for i in line:
                if i == 'c' or i == 'C' or i == 'g' or i == 'G':
                    GC_num += 1

f.close()
All = sum(stat.values())
Stat = sorted(stat.items(), key=lambda x:x[1], reverse=True)
counts = 0
Contig = ''
for i in Stat:
    Contig = i[1]
    counts += i[1]
    Contig_Name = i[0]
    if counts >= All*0.5:
         break
Max_len = max(stat.values())
Min_len = min(stat.values())

# print(Contig_Name)
GC = (GC_num/All)*100
f = open(Output, 'w')
f.write('Number\tSize\tMax_len\tMin_len\tN50\tGC(%)\n')
f.write('%d\t%d\t%d\t%d\t%s\t%.2f\n' %(NumLine, All, Max_len, Min_len, Contig, GC))
f.close()
