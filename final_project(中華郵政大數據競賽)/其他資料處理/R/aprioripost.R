setwd("C:/Users/James")
dd<-NULL
for(i in c(0:89)){
  path <- paste0("ttapriori",i)
  ttapriori89 <- read_csv(file = path, col_names = FALSE, 
                    locale = locale(encoding = "ASCII"), 
                    na = "null", skip = 1)
  try<-subset(ttapriori89,X1=='I1'|X1=='I2'|X1=='I3'|X1=='I4'|X1=='I5'|X1=='I6'|X1=='I7'|X1=='I8'|X1=='I9')
  try$X8 <- as.factor(try$X8)
  path2<-c()
  for (i in levels(try$X8)){
    path <- paste0("X8=",i)
    path2<- c(path2,path)
  }
  try$X7 <- as.factor(try$X7)
  path3<-c()
  for (i in levels(try$X7)){
    path <- paste0("X7=",i)
    path3<- c(path3,path)
  }
  rule <- apriori(try, 
                  # min support & confidence, 最小規則長度(lhs+rhs)
                  parameter=list(minlen=1, supp=0, conf=0.6),  
                  appearance = list(
                    lhs=path3,
                    rhs=path2) 
                  # 右手邊顯示的特徵
  )
  dd<-rbind(dd,inspect(rule))
}
write.table(dd,file="aprioriresult2",sep=",",row.names=F, na = "NA")
