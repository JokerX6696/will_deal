# 安装和加载biomaRt包
install.packages("biomaRt")
library(biomaRt)

# 连接到Ensembl数据库
ensembl = useMart("ensembl", dataset = "hsapiens_gene_ensembl")  # 目前该步骤失败 证书过期 待研究

# 获取COG功能注释
cog_annotations <- getBM(attributes=c("ensembl_gene_id", "cog_id", "cog_description"),
                         filters="ensembl_gene_id",
                         values="ENSG00000157764", # 输入您感兴趣的基因的Ensembl ID
                         mart=ensembl)

# 打印COG功能注释结果
print(cog_annotations)






