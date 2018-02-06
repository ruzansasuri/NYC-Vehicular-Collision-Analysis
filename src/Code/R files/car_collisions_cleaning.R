library(dplyr)
library(ggplot2)

### Setting the work directory
setwd("C:/Users/chhed/Google Drive/College/Sem 3/CSCI720 - Big Data Analytics/Project/New Investigation")

### Reading the collisions dataset
motor_collisions <- data.frame(read.csv("database_2_years.csv"), 
                               stringsAsFactors = F, sep=',', header=F)

### Checking all columns to grab the most important
names(motor_collisions)

### Selecting the useful colums
collisions <- motor_collisions[ , c(2:20, 25)]

### Taking a lot of what type of data we have
names(collisions)
head(collisions)

### Changing the names on the car collision columns into a readable format
columns <- c("date", "time","borough","zip_code","latitude","longitude","location",
             "on_street_name", "cross_street_name", "off_street_name", "total_people_injured",
             "total_people_killed", "total_pedestrians_injured", "total_pedestrians_killed",
             "total_cyclist_injured", "total_cyclist_killed","total_motorist_injured",
             "total_motorist_killed", "type_of_vehicle","reason_vehicle1_crashed")
colnames(collisions) <- columns

### Getting rid of the empty rows in location
# collisions <-  filter(collisions, !is.na(latitude) & 
#                   !is.na(longitude) &
#                   !is.na(zip_code) & 
#                   !is.na(borough))

### Add a column for year/month/day (with time of day)
collisions <- transform(collisions, date_time = as.character(paste(date, time, sep = " ")))
collisions$date_time <- as.POSIXct(collisions$date_time, format = "%m/%d/%Y %H:%M")
collisions$date <- NULL 
collisions$time <- NULL

### Bring the date_time to the front = collision is the clean data
collisions <- collisions[ , c(19, 1:18)]

### Arranging the rows in decending order to obtain the latest and the oldest car accident
collisions <- arrange(collisions, desc(date_time)) 

### Adding another column that has the y, m, and day
collisions <- transform(collisions, date = strftime(date_time, format = "%Y-%m-%d")) 

### Adding a column that has only the y and the month on it
collisions <- transform(collisions, year_month = strftime(date_time, format = "%Y-%m"))

### Adding the day of the week to the df
collisions <- mutate(collisions, day = strftime(collisions$date_time, format = "%A"))

### Adding a column that has only the year on it
collisions <- transform(collisions, year = strftime(date_time, format = "%Y"))

### Adding a column that has only the month on it
collisions <- transform(collisions, month = strftime(date_time, format = "%m"))


## Adding the season column to the collisions df
collisions <- transform(collisions, season = ifelse(month == "12" | month == "01" | month == "02","WINTER",
                                                    ifelse(month == "03" | month == "04" | month == "05","SPRING",
                                                           ifelse(month == "06" | month == "07" | month == "08","SUMMER", 
                                                                  "FALL"))))

### Bring the last columns to the first ones
car_collision <- collisions[ , c(1, 20:25, 2:19)]

### Save the clean data frame
save(car_collision, file = sprintf('car_collisions.RData'))
