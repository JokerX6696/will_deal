rm(list=ls())
setwd('D:/desk/XMSH_202307_5062')
library(dplyr)
df <- read.table('k_Abundance_Stat.filter.xls',sep = '\t',header = TRUE, quote = "", comment.char = "")

result_k <- df %>%
  group_by_at(names(df)[1]) %>%
  summarize(across(
    where(is.numeric),   # 选择所有数值列
    sum,                 # 合并操作：使用 sum 函数
    .names = "sum_{.col}" # 指定合并后的列名
  ))
names(result_k) <- names(df)
write.table(result_k,file = "K_stat.xls",quote = F,row.names = F,col.names = T,sep = "\t")

df <- read.table('S_Abundance_Stat.filter.xls',sep = '\t',header = TRUE, quote = "", comment.char = "")

result_S <- df %>%
  group_by_at(names(df)[1]) %>%
  summarize(across(
    where(is.numeric),   # 选择所有数值列
    sum,                 # 合并操作：使用 sum 函数
    .names = "sum_{.col}" # 指定合并后的列名
  ))
names(result_k) <- names(df)
write.table(result_S,file = "S_stat.xls",quote = F,row.names = F,col.names = T,sep = "\t")


