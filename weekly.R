install.packages('gdata')
library(gdata)
#wget http://www.ons.gov.uk/ons/rel/vsob2/weekly-provisional-figures-on-deaths-registered-in-england-and-wales/week-ending-06-03-2015/weekly-deaths---week-10-2015.xls
data <- read.xls("weekly-deaths---week-10-2015.xls",sheet=4,header=T)

getDeaths <- function(data, filter) {
  row <- head(grep(filter, data$Contents),1)
  
  ret <- data.frame()
  age <- c()
  fix_number <- function(d) {
    as.numeric(gsub(",","",d))
  }
  for (i in 2:8) {
    x <- data[row+i,2:length(data)]
    x <- sapply(x, function(g) if (is.na(g)) g else fix_number(g))
    ah <- data[row+i,"Contents"]
    age <- c(age,if (is.na(ah)) ah else as.character(ah))
    ret <- rbind(ret, x)
  }
  ret <- cbind(age,ret)
  header <- data[grep("Week ended",data$Contents),2:length(data)]
  names(ret) <- c("Contents",as.matrix(header))
  n <- names(ret)
  ret <- ret[,n[!is.na(n)]]
  ret$filter <- filter
  ret
}
