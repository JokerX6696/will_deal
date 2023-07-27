rm(list = ls())

args = commandArgs(trailingOnly=T)

if(length(args) != 6){

	cat(
	"============== Indicator ===========
	Usage: 
	Rscript amplicon.OTU.Indicator.r otufile groupfile type Threshold N outputpath
		parameters ->
			  otufile: [file -> always otu.tax.0.03.xls];
			groupfile: [file -> always sample.groups with header and must have #SampleID and Group columns];
			     Type: [character -> P or FDR, always P];
			Threshold: [number -> significance, always 0.05];
			        N: [number -> N most abundant taxa to plot bubble, always 100];
		       outputpath: [path -> path for output]; \n")
	options("show.error.messages" = F) 
	stop()

}

#https://github.com/tidyverse/ggplot2
if(packageVersion("ggplot2") != "2.2.0"){
	#devtools::install_github("tidyverse/ggplot2")
}

library(labdsv)
library(ggplot2)
library(gtools)

otufile = normalizePath(args[1])
groupfile = normalizePath(args[2])
Type = as.character(args[3])
Threshold = as.numeric(args[4])
N = as.numeric(args[5])
outputpath = normalizePath(args[6])

#otufile = normalizePath("D:/Softwares/group4/otu.tax.0.03.xls")
#groupfile = normalizePath("D:/Softwares/group4/sample.groups")
#Type = "P"
#Threshold = 0.05
#N = 100
#outputpath = normalizePath("D:/Softwares/group4")

setwd(outputpath)

# ====================== prepare data =======================
SampleInfo = read.table(groupfile, header = T, sep="\t", comment.char="")
SampleInfo = SampleInfo[, c("X.SampleID", "Group")]
colnames(SampleInfo) = c("Sample", "Group")
rownames(SampleInfo) = SampleInfo[,1]
Group = as.character(SampleInfo[,2])

OTUFile = read.table(otufile, header = T, sep = "\t", row.names = 1, check.name = F, comment.char = "", quote= "")
otu_data = OTUFile[,rownames(SampleInfo)]

otu_data = otu_data[rowSums(otu_data) != 0,]

loc = grep("All", rownames(otu_data))
if(length(loc) > 0) otu_data = otu_data[-loc,]

# decreasing sort by OTU Abundance
A = apply(otu_data, 1, function(x) sum(x))
otu_data = otu_data[order(A/sum(A), decreasing = T),]

# indval
indval.out = indval(t(otu_data), Group, numitr = 999, digits = 3)

indval = indval.out$indval		# the indicator value for each species
pval = indval.out$pval			# significance of identified as indicator species

fdr = p.adjust(pval, method = "BH")
if(toupper(Type) == "P"){
	
	sig = names(pval)[which(pval < Threshold)]
	
	if (length(sig) < 2){
	
		cat("ERROR: We can not get significance result with pvalue and Threshold you give, so you can modify Threshold!\n")
        q()
	
	}
	
}else{

	sig = names(fdr)[which(fdr < Threshold)]

	if (length(sig) < 2){
	
		cat("ERROR: We can not get significance result with FDR and Threshold you give, so you can turn to use P or modify Threshold!\n")
        q()
	
	}

}

# 将物种的 "." 替换为 "-"
#sig <- sub("\\.","-",sig)

indicator = cbind(indval[sig,], pval[sig], fdr[sig])
colnames(indicator)[ncol(indicator)-1] = "Pvalue"
colnames(indicator)[ncol(indicator)] = "FDR"

# plot Abundance top 50
if(length(sig) > N) sig = sig[1:N]
plot_relabun = (A/sum(A))[sig]*100
plot_indval = indval[sig,]

indicator = cbind(rownames(indicator), indicator)
colnames(indicator)[1] = "OTUId"

write.table(indicator, "indicators_indicator_value.xls", sep = "\t", row.names = F, quote = F)

# Add annotation
plot_anno = OTUFile[sig, c("order", "family")]
# sort
order = order(plot_anno$family, decreasing = T)
plot_anno = plot_anno[order,]
plot_indva = plot_indval[order,]
plot_relabun = plot_relabun[order]

# prepare data
data = stack(as.data.frame(plot_indva))
data$ylabel = as.factor(rep(rownames(plot_indva), times = ncol(plot_indva)))
data$groups = rep(unique(as.character(SampleInfo[,2])), each = nrow(plot_indva))
colnames(data) <- c("Indicator.values", "xlabel", "ylabel", "Groups")

# sort
data$xlabel = factor(data$xlabel, levels = mixedsort(levels(data$xlabel)))
data$ylabel = factor(data$ylabel, levels = rownames(plot_indva))

nm = 0.09*apply(plot_anno, 2, function(p) max(nchar(p), na.rm=T))
ng = ifelse(0.8*ncol(plot_indva) > 5, 0.8*ncol(plot_indva), 5)		# groups num

width = sum(nm) + 3 + ng
height = 0.2*nrow(plot_indva)

# plot
mycol = c(119,132,147,454,89,404,123,529,463,461,128,139,552,28,54,84,100,258,558,376,43,652,165,31,610,477,256,588,99,632,81,503,104,562,76,96,495,598,645,507,657,33,179,107,62)
mycol = colors()[mycol[1:length(unique(data$Groups))]]

library(gridExtra)
top = -4.6
rig = -1
bot = -1.1
lef = -1

pdf("indicatorsNew.pdf", height = height+2, width = width)

# order
p1 = ggplot() + annotate("text", x = rep(1, nrow(plot_indva)), y = 0.15*c(1:nrow(plot_indva)), size = 3.5, label = as.character(plot_anno[,1])) + theme_bw() +
theme_void() + 	# with no axes or grid
scale_x_continuous(expand = c(0, 0)) + 		# 原点 0,0 
#theme(plot.margin = unit(c(-1.1, 0, -1.4+0.16*(max(nchar(as.character(data$Groups)))), 0), "cm"))		# 上、右、下、左
#theme(plot.margin = unit(c(0.9, 0, 0.4+0.16*(max(nchar(as.character(data$Groups)))), 0), "cm"))		# 上、右、下、左
theme(plot.margin = unit(c(top, rig, bot, lef), "cm"))		# 上、右、下、左

# family
p2 = ggplot() + annotate("text", x = rep(1, nrow(plot_indva)), y = 0.15*c(1:nrow(plot_indva)), size = 3.5, label = as.character(plot_anno[,2])) + theme_bw() +
theme_void() + 	# with no axes or grid
scale_x_continuous(expand = c(0, 0)) + 
#theme(plot.margin = unit(c(-1.1, 0, -1.4+0.16*(max(nchar(as.character(data$Groups)))), 0), "cm"))
theme(plot.margin = unit(c(top, rig, bot, lef), "cm"))

# barplot
DataForPlot = data.frame(OTUId = names(plot_relabun), rela = plot_relabun)
DataForPlot$OTUId = factor(DataForPlot$OTUId, levels = names(plot_relabun))
DataForPlot = na.omit(DataForPlot)
p3 = ggplot(DataForPlot, aes(x = OTUId, y = rela)) + 
geom_bar(position = position_dodge(), stat = "identity", size = 0.3, colour = "black" ) +	  # Use black outlines,
coord_flip() +	 # 横向绘图
theme_bw() + ylab("Abundance(%)      ") + xlab("") +
#theme(panel.border = element_blank()) +		# 无边框
theme(plot.margin = unit(c(0.25, 0.2, 1.35, 0), "cm")) +
#theme(plot.margin = unit(c(1.2, 0.2, 0.95+0.15*(max(nchar(as.character(data$Groups)))), 0), "cm")) +
scale_y_continuous(position = "right", expand = c(0, 0), limits = c(0, max(plot_relabun)*1.2))		# x 轴刻度线在图形上方; 原点 0,0   # ggplot2 version 2.2.0
# Bubble plot
p4 = ggplot(data, aes(x = xlabel, y = ylabel, size = Indicator.values, colour = Groups)) +  # 
guides(color = FALSE) +		# 不用颜色标签
#guides(colour = guide_legend()) +		 # combine size and color legend
geom_point() + theme_bw() +
theme(axis.text.x = element_text(angle = 45, hjust = 1)) +    # x轴标签倾斜
scale_size(range = c(0,6)) + labs(x = "Groups", y = "") +
theme(plot.margin = unit(c(-0.2, 0.5, 0.2, 0), "cm")) +
scale_color_manual(values = mycol) +		# custom colors
theme(axis.text.y = element_blank(), axis.ticks.y = element_blank(), legend.position = "top")	# 去除 y轴标签及刻度线；标签位置

# combine plots
grid.arrange(p1, p2, p3, p4, ncol = 4, nrow = 1, widths = c(1.7,1.8, 4, ng))
#grid.arrange(p3, p4, ncol = 4, nrow = 1, widths = c(nm, 3, ng))
dev.off()
saveRDS(plot_indva, "plot_indva.rds" )
saveRDS(data, "data.rds")
saveRDS(DataForPlot, "DataForPlot.rds")

