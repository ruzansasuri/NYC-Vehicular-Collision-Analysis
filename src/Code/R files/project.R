setwd("C:/Users/chhed/Google Drive/College/Sem 3/CSCI720 - Big Data Analytics/Project")
library(ggplot2)
library(dplyr)
library(plotly)
library(highcharter)
library(lubridate)
library(ggthemes)
library(tidyr)
library(viridis)
library(ggmap)

create_clean_file = function(inputFile, outputFile) {
  col <- read.csv(inputFile,stringsAsFactors = F,header=T)
  col <- col[complete.cases(col), ]
  while(!is.na(match(0,col$LATITUDE))) {
    col <- col[-c(match(0,col$LATITUDE)),]
  }
  Class <- rep(0,length(col$UNIQUE.KEY))
  for (index in 1:length(Class)){
    if (col$PERSONS.KILLED[index]!=0){
      Class[index] = "KILLED"
    }
    else if(col$PERSONS.INJURED[index]!=0) {
      Class[index] = "INJURED"
    }
    else{
      Class[index] = "SAFE"
    }
  }
  col$DATE_TIME <- paste(col$DATE,col$TIME)
  col$DATE <- mdy(col$DATE)
  col$DATE_TIME <-mdy_hm(col$DATE_TIME)
  col$day <- wday(col$DATE_TIME,label = T)
  col$month <- month(col$DATE_TIME,label = T)
  col$hour <- hour(col$DATE_TIME)
  col$DATE_TIME <- NULL
  col$Classify <- Class  
  col$UNIQUE.KEY <- NULL
  col$PEDESTRIANS.INJURED <- NULL
  col$PEDESTRIANS.KILLED <- NULL
  col$MOTORISTS.INJURED <- NULL
  col$MOTORISTS.KILLED <- NULL
  #col$PERSONS.INJURED <- NULL
  #col$PERSONS.KILLED <- NULL
  col$CYCLISTS.INJURED <- NULL
  col$CYCLISTS.KILLED <- NULL
  #col$VEHICLE.2.TYPE <- NULL
  col$VEHICLE.3.TYPE <- NULL
  col$VEHICLE.4.TYPE <- NULL
  col$VEHICLE.5.TYPE <- NULL
  col$CROSS.STREET.NAME <- NULL
  col$OFF.STREET.NAME <- NULL
  col$ON.STREET.NAME <- NULL
  col$LOCATION <- NULL
  #col$DATE <- NULL
  col$TIME <- NULL
  write.csv(col, outputFile, row.names = F)
  return(col)
}
col = create_clean_file("March April 2015.csv","clean.csv")

#Per population accidents in each borough
per_pop<- col %>% group_by(BOROUGH) %>% summarise(n=n())
per_pop$pop <- rep(0,dim(per_pop)[1])
per_pop$pop <- ifelse(per_pop$BOROUGH=="MANHATTAN",1640000,per_pop$pop)
per_pop$pop <- ifelse(per_pop$BOROUGH=="BRONX",1450000,per_pop$pop)
per_pop$pop <- ifelse(per_pop$BOROUGH=="QUEENS",2330000,per_pop$pop)
per_pop$pop <- ifelse(per_pop$BOROUGH=="STATEN ISLAND",476000,per_pop$pop)
per_pop$pop <- ifelse(per_pop$BOROUGH=="BROOKLYN",2630000,per_pop$pop)
per_pop$per_cap <- per_pop$n/per_pop$pop
per_pop %>% ggplot(aes(x=BOROUGH,y=per_cap), )+geom_bar(stat="identity",fill='blue')+ggtitle("Number of Accidents Per Person")


#Accidents time plot
col %>% filter(BOROUGH!="") %>%  group_by(DATE,BOROUGH) %>% summarise(n=mean(n())) %>% na.omit() %>%
  ggplot(aes(x=DATE, y=n, colour=BOROUGH),) + geom_line() +geom_point(size=.8,shape=1)+theme_hc(bgcolor = "darkunica") +
  scale_fill_hc("darkunica") +ggtitle("Borough Accidents by Date")+geom_text(aes(label=ifelse(n>190,n,"")), size=2,hjust=1.2)


#Collisions per day in every Borough
col %>% group_by(BOROUGH,day)%>% summarise(n=mean(n())) %>% filter(BOROUGH!="") %>%
  ggplot(aes(x=day, y=n, fill=BOROUGH)) +
  geom_bar(position="dodge",stat = "identity")+geom_text(aes(label=n), vjust=1.5, colour="black",
                                                         position=position_dodge(.9), size=3)+ggtitle("Mean Number of Collisions Per Day")


df <- col %>% select(LATITUDE,LONGITUDE,PERSONS.INJURED) %>% gather(type,value,3) %>% na.omit() %>% group_by(LATITUDE,LONGITUDE,type) %>% summarise(total=sum(value,na.rm=T)) %>% filter(total!=0)
nyc <- get_map("new york",zoom=10)
g1 <- ggmap(nyc)+geom_point(data=subset(df,type=="PERSONS.INJURED"), 
                            aes(x=LONGITUDE, y=LATITUDE, colour=total),size=1,alpha=0.2) +
  ggtitle("Persons Injured")+scale_color_continuous(low = "red",  high = "black")
g1
