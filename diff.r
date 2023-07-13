rm(list=ls())
setwd('D:/desk/XMSH_202307_4956')
file <- 'Alpha_diversity_Index.xls'
df <- read.table(file, sep = '\t', quote = "", header = T)

df$Group <- c(rep('T_CRC',90),rep('T_CRN',90))


ve_t <- c()
ve_w <- c()
for (i in names(df)[2:4]) {
  x <- df[df$Group == 'T_CRC',i]
  y <- df[df$Group == 'T_CRN',i]
  
  ret_t <- t.test(x,y)
  ret_w <- wilcox.test(x,y)
  ve_t <- c(ve_t,ret_t$p.value)
  ve_w <- c(ve_w,ret_w$p.value)
}

