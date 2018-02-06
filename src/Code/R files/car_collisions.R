##  Loading libraries
#dm
library(dplyr)
#dv
library(ggplot2)
library(plotly)
library(rbokeh)
library(scales)

##  Loading data
setwd("C:/Users/chhed/Google Drive/College/Sem 3/CSCI720 - Big Data Analytics/Project/New Investigation")
load("car_collisions.RData")

seasons <- car_collision %>%
  group_by(season) %>%
  summarize(season_sum=n())

seasons <- arrange(seasons, desc(season_sum))
seasons$season <- factor(seasons$season,
                         levels=c("SUMMER", "FALL", "SPRING", "WINTER", "NA"),
                         ordered=TRUE)

plot_ly(seasons, x = ~
          season, y = ~season_sum, color = ~season, text = ~paste("people_killed: ", season_sum)) %>%
  layout(title = "2015-2016 Seasons With Highest Number of Car Collisions",
         scene = list(
           xaxis = list(title = "Seasons from 2015-2016"), 
           yaxis = list(title = "Total Number of Car Collisions")))
#################################################################################################

boroughs <- car_collision %>%
  group_by(borough) %>%
  summarize(borough_sum=n())

boroughs <- arrange(boroughs, desc(borough_sum))
boroughs <- boroughs[2:6,]

boroughs$borough <- factor(boroughs$borough, 
                           levels=c("BROOKLYN", "MANHATTAN", "QUEENS", "BRONX", 
                                    "STATEN ISLAND"),
                           ordered=TRUE)

plot_ly(boroughs, x = ~borough, y = ~borough_sum, color = ~borough, text = ~paste("accidents: ", borough_sum)) %>%
  layout(title = "Boroughs with the highest number of car collisions",
         scene = list(
           xaxis = list(title = "Boroughs from 2015 to 2016"), 
           yaxis = list(title = "Total Number of Car Collisions")))
#################################################################################################
car_collision <- mutate(car_collision, day_w = strftime(car_collision$date_time, format = "%A"))

#plot how many total accidents there are by day
day_accidents <- car_collision %>% group_by(day) %>% summarise(total_day = n())
day_accidents <- filter(day_accidents, day != "NA")
day_accidents <- arrange(day_accidents, desc(total_day))

day_accidents$day <- 
  factor(day_accidents$day, 
         levels = c("Friday", "Tuesday", "Thursday", "Wednesday", "Monday",
                    "Saturday", "Sunday"), ordered = T)

plot_ly(day_accidents, x = ~day, y = ~total_day, color = ~day, text = ~paste("t_accidents_p_day: ", total_day)) %>%
  layout(title = "Total accidents per day from 2015 to 2016",
         scene = list(
           xaxis = list(title = "Day of the week"), 
           yaxis = list(title = "Total Number of Car Collisions")))
#################################################################################################
a_type <- car_collision %>% 
  group_by(year, season, reason_vehicle1_crashed) %>% 
  summarize(accidents = n())

a_type <- filter(a_type, reason_vehicle1_crashed !="Unspecified")
a_type <- filter(a_type, year!="NA")
a_type <- filter(a_type, reason_vehicle1_crashed !="")
a_type <- arrange(a_type, desc(accidents))

a_type_highest <- filter(a_type, accidents >= 417)
a_type_lowest <- filter(a_type, accidents <= 416 & accidents >=20)

ggplot(a_type_highest, aes(x=year, y=accidents, fill=reason_vehicle1_crashed))+
  geom_bar(stat="identity")+
  ggtitle("Highest contribution factors that most car accidents occured >= 417") +
  xlab("2015 to 2016 Years")+
  ylab("Total Number of Car Collisions")


ggplot(a_type_lowest, aes(x=year, y=accidents, fill=reason_vehicle1_crashed))+
  geom_bar(stat="identity")+
  ggtitle("Lowest Reasons that most car accidents occured <= 416") +
  xlab("2015 to 2016 Years")+
  ylab("Total Number of Car Collisions")
##################################################################################################
# a) Calculations
reasons_type <- car_collision %>% 
  group_by(borough, year_month, season, reason_vehicle1_crashed) %>% 
  summarize(reasons = n())

# b) Arranging the data so I can obtain the high reasons that caused car collisions
reasons_type <- filter(reasons_type, reason_vehicle1_crashed != "Unspecified")
reasons_type <- filter(reasons_type, reason_vehicle1_crashed != "")
reasons_type <- filter(reasons_type, season != "NA")
reasons_type <- filter(reasons_type, borough != "")
reasons_type <- filter(reasons_type, reasons >= 100)

# c) Plot the highest causes of car collisions 
ggplot(reasons_type, aes(x = reason_vehicle1_crashed, y = reasons,color = as.factor(borough)))+
  geom_point(stat="identity")+
  geom_point(aes(shape = as.factor(borough)))+
  scale_size_manual(values=c(3,3,3,3))+
  ggtitle("Reasons That Most Car Accidents Occured")+
  xlab("Reasons vehicle crashed")+
  ylab("Total Number of invididuals injured")+
  facet_wrap(~ season)+
  scale_y_continuous(limits=c(100, 600))+
  theme(legend.title=element_blank(),
        axis.text.x=element_text(angle=80, hjust=1),
        legend.background = element_rect(fill = "transparent"))
#################################################################################################
##  5) For each ym and borough, -What was the type of vehicle that had the most number of accidents?
# a) Calculations
vehicle_type <- car_collision %>% 
  group_by(borough, year_month, reason_vehicle1_crashed, type_of_vehicle) %>% 
  summarize(vehicle_types = n())

# b) Arranging the data so I can plot the highest vehicle class reasons and getting rid of unspefied
vehicle <- filter(vehicle_type, vehicle_types >= 30  & 
                    reason_vehicle1_crashed != "Unspecified")
vehicle <- filter(vehicle, borough!="")
vehicle <- filter(vehicle, year_month!="NA")
vehicle <- filter(vehicle, type_of_vehicle!="")

# Graphing the type of vehicle
ggplot(vehicle, aes(x = year_month, y = vehicle_types, colour = type_of_vehicle))+
  geom_point()+
  ggtitle("Car Accidents by Vehicle type by Borough")+
  xlab("Month of Year of the Accident")+
  ylab("Total Number of invididuals killed")+
  facet_wrap(~ borough)+
  scale_y_continuous(limits=c(10, 340))+
  theme(legend.title=element_blank(),
        axis.text.x=element_text(angle=80, hjust=1),
        legend.background = element_rect(fill = "transparent"))
###############################################################################################
# a) calculations
injured <- car_collision %>% 
  group_by(borough, season, year_month, total_people_injured) %>% 
  summarize(t_p_injured = n())

injured <- filter(injured, total_people_injured >=1)
injured <- arrange(injured, desc(t_p_injured))
injured <- filter(injured, season!="NA")
injured <- filter(injured, year_month!="NA")
injured <- filter(injured, borough!="")
#View(injured)

# b) Plotting
ggplot(injured, aes(x = year_month, y = t_p_injured, color = as.factor(borough)))+
  geom_point(aes(shape = as.factor(borough), size = 2))+
  ggtitle("Perilous location where pedestrian have been injured the most")+
  xlab("Year and Month")+
  ylab("Total Number of People Injured")+
  theme(legend.title=element_blank(),
        axis.text.x=element_text(angle=80, hjust=1),
        legend.background = element_rect(fill = "transparent"))

# For each borough how many people were injured?
injured1 <- car_collision %>%
  group_by(borough, total_people_injured)%>%
  summarize(t_inj=n())
injured1 <- filter(injured1, borough != "")
injured1 <- filter(injured1, total_people_injured != "NA")
injured1 <- arrange(injured1, desc(t_inj))

figure(width = NULL, height = NULL, 
       title = "Total people injured in each borough",
       xlab = "Total people injured)",
       ylab = "The sum of total people injured in each borough") %>%
  ly_points(total_people_injured, t_inj, data = injured1, 
            color = borough, glyph = borough,
            hover = list(total_people_injured, t_inj))
##########################################################################################
# a) Calculations
motorist_accidents <- car_collision %>% 
  group_by(borough, season, year_month, total_motorist_killed) %>% 
  summarize(n_motorist_killed = n())

motorist_killed <- filter(motorist_accidents, total_motorist_killed == "1")
motorist_killed <- arrange(motorist_killed, desc(n_motorist_killed))
motorist_killed <- filter(motorist_killed, season!="NA")
motorist_killed <- filter(motorist_killed, borough!="")
motorist_killed <- filter(motorist_killed, year_month!="NA")
#head(motorist_killed, n=10)

# b) Plotting
ggplot(motorist_killed, aes(x = year_month, y = n_motorist_killed, color = as.factor(year_month)))+
  geom_point(aes(shape = as.factor(season), size = .2))+
  ggtitle("Boroughs where most motorist were killed the most")+
  xlab("Year and month")+
  ylab("Total number of motorist killed")+
  facet_wrap(~ borough) +
  theme(legend.title=element_blank(),
        axis.text.x=element_text(angle=80, hjust=1),
        legend.background = element_rect(fill = "transparent"))


ggplot(motorist_killed, aes(x = year_month, y = n_motorist_killed, color = as.factor(season)))+
  geom_point(aes(shape = as.factor(season), size = .2))+
  ggtitle("Boroughs Where Most Motorist Were Killed The Most")+
  xlab("Year and Month color coded by season")+
  ylab("Total Number of Motorist Killed")+
  facet_wrap(~ borough) +
  theme(legend.title=element_blank(),
        axis.text.x=element_text(angle=80, hjust=1),
        legend.background = element_rect(fill = "transparent"))

m_k <- motorist_killed %>%
  group_by(season) %>%
  summarise(total=n())

m_k <- arrange(m_k, desc(total))
m_k$season <- factor(m_k$season, 
                     levels=c("SUMMER", "FALL", "SPRING", "WINTER"),
                     ordered = TRUE)

plot_ly(m_k, x = ~season, y = ~total, color = ~season, text = ~paste("people_killed: ", total)) %>%
  layout(title = "Seasons Where Most Motorist Were Killed The Most",
         scene = list(
           xaxis = list(title = "Seasons"), 
           yaxis = list(title = "Number of Motorist Killed")))
#######################################################################################################
b_ym <- car_collision %>%
  group_by(month, borough) %>%
  summarize(b_ym_sum=n())

b_ym <- arrange(b_ym, desc(b_ym_sum))

b_ym <-  filter(b_ym, 
                !is.na(month) & 
                  !is.na(borough) &
                  !month == "" &
                  !borough == "")

ggplot(b_ym, aes(x=month, y=b_ym_sum, fill=borough)) +
  geom_bar(stat="identity") +
  geom_smooth(se = FALSE, method = "loess") +
  ggtitle("12 Months with highest number of car collisions from 2015-2016") +
  xlab("Months")+
  ylab("Total Number of Car Collisions")
####################################################################################################
#1
july <- car_collision %>%
  group_by(year_month, borough) %>%
  summarize(july_total=n())

july <- filter(july, 
               (year_month == "2015-07" |
                  year_month == "2016-07") & 
                 (!borough == ""))
july <- arrange(july, desc(july_total))
july$year_month <- factor(july$year_month,
                          levels=c("2015-07" ,"2016-07"),
                          ordered=TRUE)

#2
julys <- car_collision %>%
  group_by(date, year_month, borough) %>%
  summarize(julys_total=n())

julys1 <- filter(julys, 
                 (year_month == "2015-07" |
                    year_month == "2016-07") & 
                   (!borough == ""))
julys1 <- arrange(julys1, desc(julys_total))
head(julys1)

print("This first graph displays all the months of July from the year 2012 to 2016. This graph, displays the total number of car collision as a function of month and year. Our results show that on July 2015 we had the highest number of car collisions")
ggplot(july, aes(x=year_month, y=july_total, fill=year_month)) +
  geom_bar(stat="identity") +
  geom_smooth(se = FALSE, method = "loess") +
  ggtitle("Comparing each July months from 2015 to 2016") +
  xlab("Months")+
  ylab("Total Number of Car Collisions")

print("This second graph displays the total number of car collision as a function of months color coded by borough. In this graph we can see how Brooklyn has the highest number in car collisions on July 2015")
ggplot(na.omit(julys1), aes(x = year_month, y = julys_total, colour=borough)) + 
  geom_boxplot(aes(fill = borough), alpha = 0.1) + 
  guides(fill=FALSE) + 
  labs(x = "Months", 
       y = "Total Number of Car Collisions", 
       title = "July months with highest number of car collisions by borough") 

print("This third graph displays the total number of car collision as a function of dates color coded by borough. This graph shows that on July 20 2015 we have highest number of car collisions on Brooklyn")
p <- ggplot(julys1, aes(x=date, y=julys_total, group=borough, colour=borough))
p + geom_line(arrow = arrow())+
  geom_point(aes(shape = as.factor(borough), size = .2))+
  ggtitle("July months with highest number of car collisions by borough") +
  xlab("Dates")+
  ylab("Total Number of Car Collisions")+
  theme(legend.title=element_blank(),
        axis.text.x=element_text(angle=90, hjust=1),
        legend.background = element_rect(fill = "transparent")) 
##################################################################################################
may <- car_collision %>%
  group_by(year_month, borough) %>%
  summarize(may_total=n())

may <- filter(may, 
              (year_month == "2015-05" |
                 year_month == "2016-05") & 
                (!borough == ""))
may <- arrange(may, desc(may_total))
may$year_month <- factor(may$year_month,
                         levels=c("2015-05" ,"2016-05"),
                         ordered=TRUE)

#2
mays <- car_collision %>%
  group_by(date, year_month, borough) %>%
  summarize(mays_total=n())

mays1 <- filter(mays, 
                (year_month == "2015-05" |
                   year_month == "2016-05") & 
                  (!borough == ""))
mays1 <- arrange(mays1, desc(mays_total))
head(mays1)

print("This first graph displays all the months of may from the year 2012 to 2016. This graph, displays the total number of car collision as a function of month and year. Our results show that on may 2015 we had the highest number of car collisions")
ggplot(may, aes(x=year_month, y=may_total, fill=year_month)) +
  geom_bar(stat="identity") +
  geom_smooth(se = FALSE, method = "loess") +
  ggtitle("Comparing each may months from 2015 to 2016") +
  xlab("Months")+
  ylab("Total Number of Car Collisions")

print("This second graph displays the total number of car collision as a function of months color coded by borough. In this graph we can see how Brooklyn has the highest number in car collisions on may 2015")
ggplot(na.omit(mays1), aes(x = year_month, y = mays_total, colour=borough)) + 
  geom_boxplot(aes(fill = borough), alpha = 0.1) + 
  guides(fill=FALSE) + 
  labs(x = "Months", 
       y = "Total Number of Car Collisions", 
       title = "may months with highest number of car collisions by borough") 

print("This third graph displays the total number of car collision as a function of dates color coded by borough. This graph shows that on may 20 2015 we have highest number of car collisions on Brooklyn")
p <- ggplot(mays1, aes(x=date, y=mays_total, group=borough, colour=borough))
p + geom_line(arrow = arrow())+
  geom_point(aes(shape = as.factor(borough), size = .2))+
  ggtitle("may months with highest number of car collisions by borough") +
  xlab("Dates")+
  ylab("Total Number of Car Collisions")+
  theme(legend.title=element_blank(),
        axis.text.x=element_text(angle=90, hjust=1),
        legend.background = element_rect(fill = "transparent")) 
