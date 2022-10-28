#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 知识点：
# samtools 是处理sam,bam,cram格式非常高效的工具
# 在sam中 flag 则是对reads比对形式的描述
# 1   ：代表这个序列采用的是PE双端测序
# 2   ：代表这个序列和参考序列完全匹配，没有插入缺失
# 4   ：代表这个序列没有mapping到参考序列上
# 8   ：代表这个序列的另一端序列没有比对到参考序列上，比如这条序列是R1,它对应的R2端序列没有比对到参考序列上
# 16  ：代表这个序列比对到参考序列的负链上
# 32  ：代表这个序列对应的另一端序列比对到参考序列的负链上
# 64  ：代表这个序列是R1端序列， read1;
# 128 ：代表这个序列是R2端序列，read2；
# 256 ：代表这个序列不是主要的比对，一条序列可能比对到参考序列的多个位置，只有一个是首要的比对位置，其他都是次要的
# 512 ：代表这个序列在QC时失败了，被过滤不掉了
# 1024：代表这个序列是PCR重复序列
# 2048：代表这个序列是补充的比对

# samtools view -f / -F 两种模式，可以根据flag值从bam结果中快速提取需要的比对结果。


# 题目：
# 利用 samtools 提取 bam 中的 1:1000000-2000000 区域内 paired-reads 都唯一比对上基因组的比对结果


# 文件：
# aligned.sorted.bam
# aligned.sorted.bam.bai

# 脚本名：
# samtools.py

# 脚本执行方式：
# python tmp.py -i aligned.sorted.bam -r 1:1000000-2000000 -o out.sam
# /public/store5/DNA/Test/capture_test/python_exercise/lianxi2 #本地集群
# 结果示例：
# E00495:589:H3M7MCCX2:2:1116:19918:52414	99	1	1000393	60	6S144M	=	1000711	468	ACTGCAGGGACACCCGGGGGTGGGCGGAGTCTCGGGGCTCACTCTCCCGCCCAGGGGGCCGGGAGCCGGGGCTGGACGGAGCTGGGGCTGTGGCCGCGCGGGAAGTCGGGAAGGAAATTCCCCCAGTGGCGCAGGGTCCGGCGGCGCCGA	AAFFFJJJJJJJJJJJJJJJJJJJJJJJJJJFJJJJFJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJAJFJJJ7F7AJJJJJJJJFA-<FJJJJJJJJJFFJFAJF7FJFJJJJJJJJJJJJFFJJJJJJJJJJ-	NM:i:2	MD:Z:5C7C130	AS:i:134	XS:i:0	RG:Z:1
# E00495:589:H3M7MCCX2:2:1116:20273:52643	99	1	1000393	60	6S144M	=	1000711	468	ACTGCAGGGACACCCGGGGGTGGGCGGAGTCTCGGGGCTCACTCTCCCGCCCAGGGGGCCGGGAGCCGGGGCTGGACGGAGCTGGGGCTGTGGCCGCGCGGGAAGTCGGGAAGGAAATTCCCCCAGTGGCGCAGGGTCCGGCGGCGCCGA	AAAFFJJJJJJJFJJJJJAJ<FAJJJJAAFA7FJFJJJ<<JJFFJJJFJJJJFJJJJJJ<AJJJJAFFFJJF<JJFAJJFJAJJJJJJJJFJJJJJFJJJFJFJJJJJJJ<AFJ7JJFJJFFAFJJ<AJFJJJAAFF)AAAJFJJF<JJ<	NM:i:2	MD:Z:5C7C130	AS:i:134	XS:i:0	RG:Z:1

print('##################################################################')

import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--infile', required=True, help='inputfile for bam mapping')
parser.add_argument('-r', '--region', required=True, help='region for mapping')
parser.add_argument('-o', '--output', required=True, help='output')

args = parser.parse_args()
a = args.infile
b = args.region
c = args.output
#    return args.infile, args.region, args.output

print(a,b,c)


os.system("/data/software/samtools/samtools-v1.9/bin/samtools view -F 12 %s %s > %s" %(a,b,c))





