#!/bin/env python
# python motif_detect.py -i genome.fa -m ATARYGAG -f 5 -o motif.txt
import re,argparse

# Motif
Pattern = '.{0,5}ATA[A|G][C|T]GAG.{0,5}'


All = ''
counts = 0
with open('genome.fa', 'r') as f:
    while True:
        counts += 1
        line = f.readline()
        if not line:
            All = All + '\n'
            break
        elif '>' in line:
            if counts != 1:
                All = All + '\n'
            All = All + line
        else:
            All = All + line.replace('\n', "")
f.close
All = All.split('\n')
counts = 0
for i in All:
    counts += 1
    if counts % 2 != 0 and i:
        Chr = re.match('^>.', i).group().replace('>', '')
    elif counts % 2 == 0 and i:
        Motif = re.findall(Pattern, i, re.I)
        print(Chr, Motif)
        break




