options(stringsAsFactors = FALSE)

lifeexp <- read.csv("lifeexp-2010.csv")
mps <- read.csv("result.csv",header=F)
lad <- read.csv("LAD11_PCON11_UK_LU.csv")
leconst <- merge(lifeexp, lad, by.x="area", by.y="LAD11CD")
m <- merge(leconst,mps, by.x="PCON11NM",by.y="V1")

m <- m[,c("PCON11NM","area","male.le","female.le","V2")]
names(m) <- c("const","area","male.le","female.le","Party.Name")

spend <- read.csv("2010-UK-Parliament-spending-data-CSV.csv")
spend <- spend[,c("Constituency.Name","Position","Votes..","Party.Name")]
names(spend) <- c("const","position","votespct","party")
library(sqldf)
sp <- sqldf("select a.const, a.votespct-b.votespct as margin,a.party from spend a inner join spend b on a.const=b.const and b.position=2 where a.position=1")
m <- merge(sp,m)
write.csv(m,"lifeexp-mp-margin.csv",row.names=F)

efac <- read.csv("death-extraFactors.csv")
names(efac)[2] <- "area"
efac <- efac[,grep("X", names(efac), invert=T)]
g <- unique(merge(m,efac))

mlsoa <- read.csv("~/ohdh14/lsoa.csv",header=F)
mlsoa <- unique(mlsoa[,c(3,5)])
names(mlsoa) <- c("area","MSOA")

income <- read.csv("201308NIC-MSOA-practices.csv")
income <- merge(mlsoa, income)
income <- aggregate(annual_income ~ area, income, median)
g <- merge(g, income)
write.csv(g,"lifeexp-extrafac.csv",row.names=F)
