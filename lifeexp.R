library(gdata)
data <- read.xls("~/Downloads/referencetable1_tcm77-332890.xls",sheet=18,header=F)
ret <- data[grep("^E[0-9]+$", data$V1),c("V1","V81")]
names(ret) <- c("area","le")
ret$le <- as.numeric(as.vector(ret$le))
ret <- ret[!is.na(ret$le),]
head(ret)
write.csv(ret,"lifeexp-male-2010.csv")

