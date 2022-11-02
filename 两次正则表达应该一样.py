#!/bin/env python
# python motif_detect.py -i genome.fa -m ATARYGAG -f 5 -o motif.txt
import re
import argparse
print('该脚本运行缓慢，请耐心等待！')
Output = 'testTmp.txt'
# Motif
Pattern = 'ATA[A|G][C|T]GAG'
Pattern_ud = '.{0,5}ATA[A|G][C|T]GAG.{0,5}'

All = ''
counts = 0
with open('./genome.fa', 'r') as f:
    while True:
        line = f.readline()
        if not line:
            All += line
            All += '\n'
            break
        if '>' in line:
            line = line + '>'
        All += line
All = All.split('>')
f = open('test.txt', 'w')
print('chrom\tpos\tmotif\tflank',file=f)
counts = 0
for i in All:
    if not i:
        continue
    fa = i.replace(" ","").replace("\n","")
    counts += 1
    if counts % 2 == 0:
        Motif = re.findall(Pattern, fa, re.I|re.S)
        for M in Motif:
            motif = re.search(M, fa)
            motif_seq = motif.group()
            motif_pos = motif.end()
            motif_ud = re.search('.{0,5}%s.{0,5}' %(M), fa).group()
            print(Chr, motif_pos, motif_seq, motif_ud,sep='\t')
            print(Chr, motif_pos, motif_seq, motif_ud,sep='\t',file=f)
            fa = fa.replace(M, 'N'*len(M),1)
    else:
        Chr = re.search('^.', i).group()

f.close
