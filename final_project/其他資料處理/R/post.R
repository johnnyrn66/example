#let data divide into 89 days
setwd("C:/Users/James")
for(i in c(0:89)){
  path <- paste0("tt",i)
  ttcsv <- read.csv(file = path, header = FALSE)
  ttsub <- subset(ttcsv, V1=='H'|V1=='H4')
  nam2 = paste('HH',i,sep='')
  assign(nam2,ttsub)
}
#write into a data
setwd("C:/Users/James")
for(i in c(0:89)){
  data <- paste0('HH',i)
  eval(parse(text = paste("write.table(",data,',file="', data,'",sep=",",row.names=F, na = "NA")',sep='')))
}
#let data divide into 1 month
setwd("C:/Users/James")
data <- NULL
for(i in c(0:29)){
  path <- paste0('HH',i)
  csv2 <- read.csv(file = path, header = FALSE)
  data <- rbind(data,csv2)
}
write.table(data,file="HHmonth1",sep=",",row.names=F, na = "NA")
#let data divide into month2
setwd("C:/Users/James")
data <- NULL
for(i in c(29:58)){
  path <- paste0('HH',i)
  csv2 <- read.csv(file = path, header = FALSE)
  data <- rbind(data,csv2)
}
write.table(data,file="HHmonth2",sep=",",row.names=F, na = "NA")
#let data divide into month3
data <- NULL
for(i in c(58:89)){
  path <- paste0('HH',i)
  csv2 <- read.csv(file = path, header = FALSE)
  data <- rbind(data,csv2)
}
write.table(data,file="HHmonth3",sep=",",row.names=F, na = "NA")
#let data all
data <- NULL
for(i in c(0:89)){
  path <- paste0('HH',i)
  csv2 <- read.csv(file = path, header = FALSE)
  data <- rbind(data,csv2)
}
write.table(data,file="HHall",sep=",",row.names=F, na = "NA")

setwd("C:/Users/James")
HHall<-read.csv(file = 'HHall',header=TRUE)
HHall<-HHall[-1,]
data <- NULL
for(i in c(1:dim(HHall)[1])){
data<-rbind(data,substr(HHall$V2[i],start=13,stop=14))
}
summary(data)

setwd("C:/Users/James")
HHall<-read.csv(file = 'HHall.csv',header=TRUE)
for(i in c(1:dim(HHall)[1])){
  HHall[,7]<-substr(HHall[,2],start=13,stop=14)
}

HHall$V7<-substr(HHall$V2,start=13,stop=14)
setwd("C:/Users/James")
HHall<-HHall[-1,]
HHall$V8<-substr(HHall$V2,start=7,stop=12)
HHall$V9<-substr(HHall$V2,start=15,stop=19)
write.table(HHall,file="HHall.csv",sep=",",row.names=F, na = "NA")


ACC01 <- read.csv(file = 'HHall',header = TRUE)
HHall$V8<-as.factor(HHall$V8)
HHall$V9<-as.factor(HHall$V9)
library(readr)
tt0 <- read_csv("HHall")
a<-levels(HHall$V8)
b<-levels(HHall$V9)
c<-c(a,b)
c<-as.factor(c)
 
#postcode
states <- read.table("C:/Users/James/codepost.txt", quote="\"", comment.char="")
setwd("C:/Users/James")
for(i in c(0:89)){
  path <- paste0("tt",i)
  ttcsv <- read.csv(file = path, header = FALSE)
  ttcsv$V5 <- as.factor(ttcsv$V5)
  postcode <- levels(ttcsv$V5)
  for(i in c(1:dim(postcode)[1])){
    if (which(levels(c) == postcode$V5[i]) > 0){
      ttsub <- subset(ttcsv, V1=='H'|V1=='H4')
      nam2 = paste('HH',i,sep='')
      assign(nam2,ttsub)}}
}
setwd("C:/Users/James")
path <- paste0("tt",0)
tcsv <- read.csv(file = path, header = FALSE)
tcsv$V5 <- as.factor(tcsv$V5)
postcode <- levels(tcsv$V5)
ttsub <- matrix( 0,nrow=length(postcode))
for(i in c(1:dim(postcode)[1])){
  if (which(levels(postcode) == tcsv$V5[i]) > 0){
    for(j in c(1:dim(states)[1])){
    ttsub$v1[j] <- subset(tcsv, V1==states$V1[j])
}}}


#eval(parse(text = paste("for( j",' in c(', csv2,'$V2','{',ttsub ,'<- subset(', csv1,', V2 == j)',data,'<- rbind(',data,' <- rbind(,data,ttsub)}',sep='')))
#ACC01$V33<- as.character(ACC01$V33)
#ACC01$V34<- as.character(ACC01$V34)
#HHmonth1$V2 <- as.character(HHmonth1$V2)
#data <- NULL
#for(i in c(1:dim(HHmonth1)[1])){
#    data <- rbind(data,ACC01[which(ACC01$V3 <= HHmonth1$V2[i] & ACC01$V34>= HHmonth1$V2[i]),])
#}
#write.table(data,file="ACCHH01",sep=",",row.names=F, na = "NA")

setwd("C:/Users/James")
postall <- NULL
post <- NULL
for(i in c(0:1)){
  path <- paste0("tt",i)
  ttcsv <- read.csv(file = path, header = FALSE)
  ttcsv$V5 <- as.factor(ttcsv$V5)
  post <- data.frame(levels(ttcsv$V5))
  colnames(post) <- c('office')
  for(b in c('A1','A2')){
    ttsub <- subset(ttcsv, V1 == b)
    ft <- fct_count(ttsub$V5)
    ft <- as.data.frame(ft)
    colnames(ft) <- c('office',b)
    post <- merge(x=post,y=ft,by='office')
  }
#  diffoff <- setdiff(postall$office,post$office)
  for(j in dim(postall)[1]){
    ind <- which(post$office == postall$office )
    postall <- rbind(postall, post[ind,])
    sumtable <- rbind(postall[ind,-1],post[j,-1])
    sumtable <- rbind(sumtable,colSums(sumtable))
    officetable <- data.frame(c(postall[ind,1],postall[ind,1]))
    colnames(officetable) <- c('office')
    sumtable <- cbind(officetable,sumtable)
    postall[ind,] <- subtable[3,]
  }
}
hh<-rbind(postall$office,post$office)
plevel <- levels(as.factor(hh))
ppostall$office <- factor(postall$office, levels=plevel)
post$office <- factor(post$office, levels=plevel)
for(j in c(1:dim(post)[1])){
  #breakVector[,1] <- factor(breakVector[,1], levels=levels(FinalTable[,1]))
  ind <- which(postall$office==post$office[j])
  if (length(ind)>0){
    sumtable <- rbind(postall[ind,-1],post[j,-1])
    sumtable <- rbind(sumtable,colSums(sumtable))
    officetable <- data.frame(c(postall[ind,1],postall[ind,1]))
    colnames(officetable) <- c('office')
    sumtable <- cbind(officetable,sumtable)
    postall[ind,] <- subtable[3,]
  }else{
    postall <- rbind(postall,post[j,])
  }
}