library(gdata)
getLifeExp <- function(s, type) {
  data <- read.xls("referencetable1_tcm77-332890.xls",sheet=s,header=F)
  # Match 1991-1993 Life expectancy at birth 
  cols <- paste0("V",seq(4,80,4))
  ret <- data[grep("^E[0-9]+$", data$V1),c("V1",cols)]
  names(ret) <- c("area",paste0(type,".le.",data[5,cols]))
  ret[,2:length(ret)] <- as.numeric(as.matrix(ret[,2:length(ret)]))
  # male.le.1991-1993 -> male.le.1991
  names(ret) <- gsub("(.*?)-.*","\\1",names(ret))
  na.omit(ret)
}
male <- getLifeExp(18,"male")
female <- getLifeExp(22,"female")
ret <- merge(male,female)
ml <- melt(ret)
ml$year <- as.numeric(gsub(".*?le.(\\d+)", "\\1", ml$variable))
ml$gender <- gsub("(.*?)\\.le.*", "\\1", ml$variable)
ml$le <- ml$value
ml <- ml[,c("area","year","gender","le")]
write.csv(ml,"lifeexp-1991-2010.csv")

