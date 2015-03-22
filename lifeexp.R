library(gdata)
getLifeExp <- function(s, type) {
  data <- read.xls("~/Downloads/referencetable1_tcm77-332890.xls",sheet=s,header=F)
  ret <- data[grep("^E[0-9]+$", data$V1),c("V1","V80")]
  names(ret) <- c("area", "le")
  ret$le <- as.numeric(as.vector(ret$le))
  ret <- ret[!is.na(ret$le),]
  names(ret)[2] <- paste0(type, ".le")
  ret
}
male <- getLifeExp(18,"male")
female <- getLifeExp(22,"female")
ret <- merge(male,female)
write.csv(ret,"lifeexp-2010.csv")

