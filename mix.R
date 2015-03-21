options(stringsAsFactors = FALSE)

lifeexp <- read.csv("lifeexp-male-2010.csv")
mps <- read.csv("result.csv",header=F)
#names(mps) <- c("")
lad <- read.csv("LAD11_PCON11_UK_LU.csv")
leconst <- merge(lifeexp, lad, by.x="area", by.y="LAD11CD")
m <- merge(leconst,mps, by.x="PCON11NM",by.y="V1")

m <- m[,c("PCON11NM","area","le","V2")]
names(m) <- c("const","area","le","Party")

#plot(m$V2, m$le)

spend <- read.csv("2010-UK-Parliament-spending-data-CSV.csv")
spend <- spend[,c("Constituency.Name","Position","Votes..","Party.Name")]
names(spend) <- c("const","position","votespct","party")
library(sqldf)
sp <- sqldf("select a.const, a.votespct-b.votespct as margin,a.party from spend a inner join spend b on a.const=b.const and b.position=2 where a.position=1")
m <- merge(sp,m)
write.csv(m,"lifeexp-mp-margin.csv",row.names=F)

efac <- read.csv("death-extraFactors.csv")
names(efac)[2] <- "area"
m <- merge(m,efac)
write.csv(m,"lifeexp-extrafac.csv",row.names=F)
