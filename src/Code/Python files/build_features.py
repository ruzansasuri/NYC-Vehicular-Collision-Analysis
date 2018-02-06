"""
Authors: Ruzan Sasuri(rps7183)
		 Anuj Chheda(akc9782)
Date: Dec 4th, 2017.
"""
from matplotlib import pyplot as plt
import numpy as np
from matplotlib import ticker as tick
import datetime as dt

CLASSES = ['Safe', 'Injured', 'Killed']
DAYS = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
BOROUGHS = ['MANHATTAN', 'BRONX', 'QUEENS', 'BROOKLYN', 'STATEN ISLAND']
MARKERS = ['go', 'bo', 'ko']
COLORS = ['lightgreen', 'cornflowerblue', 'magenta']
# BOROUGH_COLORS = ['lightgreen', 'cornflowerblue', 'goldenrod', 'salmon', 'olive']
# BOROUGH_COLORS = ['r', 'y', 'g', 'b', 'k']
BOROUGH_COLORS = ['mediumslateblue', 'k', 'gold', 'fuchsia', 'dimgrey']


class Incident:
	"""
	Stores the detail of a single collision.
	"""
	__slots__ = 'id', 'date', 'day', 'time', 'time_class', 'borough', 'latitude', 'longitude', 'injured', 'killed',\
				'pedestrian_injured', 'pedestrian_killed', 'safety_class'

	def __init__(self, point):
		self.id = int(point[1])
		self.date = point[2]
		self.day = self.find_day()
		self.time = point[3]
		self.time_class = self.find_time()
		self.borough = BOROUGHS.index(point[4])
		self.latitude = float(point[6])
		self.longitude = float(point[7])
		self.injured = int(point[13])
		self.killed = int(point[14])
		self.pedestrian_injured = int(point[15])
		self.pedestrian_killed = int(point[16])
		self.safety_class = self.find_safety()

	def find_day(self):
		if '/' in self.date:
			day = dt.datetime.strptime(self.date, '%m/%d/%Y').date().weekday()
		else:
			day = dt.datetime.strptime(self.date, '%m-%d-%y').date().weekday()
		return day

	def find_time(self):
		return int(self.time.split(':')[0])

	def find_safety(self):
		if self.killed > 0:
			return 2
		elif self.injured > 0:
			return 1
		else:
			return 0

	def __str__(self):
		return str(self.id) + ',' + str(self.day) + ',' + str(self.time_class) + ',' + str(self.borough) + ',' +\
			   str(self.latitude) + ',' + str(self.longitude) + ',' + str(self.safety_class)


def file_check(file, permission):
	"""
    Creates a file handler.
    :param file: Name of t`he file
    :param permission: Permission
    :return: File handler
    """
	try:
		f = open(file, permission)
		return f
	except FileNotFoundError:
		print("File", file, "does not exist...")
		exit()


def read_csv(file):
	"""
	Reads the csv file and converts it into data points and attriutes.
    :param file: File handler
    :return: list of attributes and a list of data points.
    """
	attrs = 'ID,DATE,TIME,BOROUGH,LATITUDE,LONGITUDE,CLASS'
	data_points = []
	# j = 0
	# matplot.figure("Map", (30, 10))
	# matplot.title('Map')
	# j = 0
	file.readline()
	for line in file:
		if line == '\n' or line.strip() == '':
			continue
		line = line.strip().split(',')
		for i in range(len(line)):
			line[i] = line[i].strip('"')
		data_points.append(Incident(line))
	return attrs, data_points


def draw_map(data, name='ALL'):
	"""
	Draws a map of the data points based on the latitude and longitude of each collision.
	:param data: The data.
	:param name: The name of the map. Default value is 'ALL'
	:return: None.
	"""
	class2 = False
	class1 = False
	class0 = False
	plt.figure(name, (20, 20))
	plt.title(name)
	minx = float('inf')
	maxx = -float('inf')
	miny = float('inf')
	maxy = -float('inf')
	for incident in data:
		x = incident.longitude
		if x < minx:
			minx = x
		elif x > maxx:
			maxx = x
		y = incident.latitude
		if y < miny:
			miny = y
		elif y > maxy:
			maxy = y
		safety_class = incident.safety_class
		if not class2 and safety_class == 2 and class1:
			plt.plot(x, y, MARKERS[safety_class], label=CLASSES[safety_class])
			class2 = True
		elif not class1 and safety_class == 1 and class0:
			plt.plot(x, y, MARKERS[safety_class], label=CLASSES[safety_class])
			class1 = True
		elif not class0 and safety_class == 0:
			plt.plot(x, y, MARKERS[safety_class], label=CLASSES[safety_class])
			class0 = True
		else:
			plt.plot(x, y, MARKERS[safety_class])
	plt.plot(minx, miny, '')
	plt.plot(maxx, maxy, '')
	plt.gca().set_aspect('equal', adjustable='box')
	plt.legend(loc='upper right')
	plt.show()


def split_by_day(data):
	"""
	Splits the list of collisions by the day of the week they occur on.
	:param data: The data.
	:return: A list of data for collisions that occur on each day.
	"""
	day_data = [[] for _ in range(7)]
	for incident in data:
		day_data[incident.day].append(incident)
	return day_data


def split_by_borough(data):
	"""
	Splits the list of collisions by the borough in which they occur.
	:param data: The data.
	:return: A list of data for collisions that occur in each borough.
	"""
	borough_data = [[] for _ in range(len(BOROUGHS))]
	for incident in data:
		borough_data[incident.borough].append(incident)
	return borough_data


def split_by_time(data):
	"""
	Splits the list of collisions by the day of the hour in the day on which they occur.
	:param data: The data.
	:return: A list of data for collisions that occur at each hour of the day it occurred on.
	"""
	time_data = [[] for _ in range(24)]
	for incident in data:
		time_data[incident.time_class].append(incident)
	return time_data


def draw_days(data):
	"""
	Draws a map for each day of the week.
	:param data: The data
	:return: None.
	"""
	day_data = split_by_day(data)
	print('split')
	for day in range(len(DAYS)):
		draw_map(day_data[day], DAYS[day])


def draw_boroughs(data):
	"""
	Draws a map for each of the boroughs in NYC.
	:param data: The data.
	:return: None.
	"""
	boroughs = split_by_borough(data)
	for borough in range(len(BOROUGHS)):
		draw_map(boroughs[borough], BOROUGHS[borough])


def draw_hist(data, name='ALL'):
	"""
	Draws a histogram of the count of collisions based on the borough they occur in and the type of incident they
	result in.
	:param data: The data
	:param name: The name off the histogram.
	:return: None.
	"""
	data = split_by_borough(data)
	plt.figure('Histogram', (40, 30))
	# bars = []
	x = np.arange(len(BOROUGHS))
	zero_list = []
	one_list = []
	two_list = []
	for b in range(len(data)):
		zero = 0
		one = 0
		two = 0
		for incident in data[b]:
			if incident.safety_class == 0:
				zero += 1
			elif incident.safety_class == 1:
				one += 1
			else:
				two += 1
		# bars += [zero, one, two, 0]
		zero_list.append(zero)
		one_list.append(one)
		two_list.append(two)
	# matplot.hist(bars, bins=len(bars))#, color=COLORS, label=CLASSES)
	# xt = []
	# for b in BOROUGHS:
	# 	xt += ['', b, '', '']
	y_list = [zero_list, one_list, two_list]
	f, a = plt.subplots()# 40, 30)
	a.set_title(name)
	a.grid(zorder=0)
	width = 0.2
	for i in range(len(CLASSES)):
		a.bar(x + (width * i), y_list[i], width=width, color=COLORS[i], label=CLASSES[i], zorder=3)
	a.set_xticks(x + (3 * width / 2))
	a.set_xticklabels(BOROUGHS)
	a.set_yticks([0, 10, 100, 1000, 10000])
	a.set_yscale('log')
	a.get_yaxis().set_major_formatter(tick.ScalarFormatter())
	a.set_xlabel('BOROUGHS')
	a.set_ylabel('COUNT')
	a.legend(CLASSES)#, 'upper right')
	plt.show()


def draw_time_hist(data):
	"""
	Draws a histogram of the count of collisions based on the hour in the day and the type of incident they
	result in.
	:param data: The data
	:return: None.
	"""
	data = split_by_time(data)
	plt.figure('Time based Histogram', (40, 30))
	# bars = []
	x = np.arange(24)
	zero_list = []
	one_list = []
	two_list = []
	for t in range(len(data)):
		zero = 0
		one = 0
		two = 0
		for incident in data[t]:
			if incident.safety_class == 0:
				zero += 1
			elif incident.safety_class == 1:
				one += 1
			else:
				two += 1
		# bars += [zero, one, two, 0]
		zero_list.append(zero)
		one_list.append(one)
		two_list.append(two)
	# matplot.hist(bars, bins=len(bars))#, color=COLORS, label=CLASSES)
	# xt = []
	# for b in BOROUGHS:
	# 	xt += ['', b, '', '']
	y_list = [zero_list, one_list, two_list]
	f, a = plt.subplots()  # 40, 30)
	a.set_title('Time Based Histogram')
	a.grid(zorder=0)
	width = 0.2
	for i in range(len(CLASSES)):
		a.bar(x + (width * i), y_list[i], width=width, color=COLORS[i], label=CLASSES[i], zorder=3)
	a.set_xticks(x + (3 * width / 2))
	a.set_xticklabels([i for i in range(24)])
	a.set_yticks([0, 10, 100, 1000, 10000])
	a.set_yscale('log')
	a.get_yaxis().set_major_formatter(tick.ScalarFormatter())
	a.set_xlabel('HOUR')
	a.set_ylabel('COUNT')
	a.legend(CLASSES)  # , 'upper right')
	plt.show()


def draw_time_hist_borough(data):
	"""
	Draws a histogram of the count of collisions based on the hour in the day and the borough they occur in.
	:param data: The data
	:return: None.
	"""
	data = split_by_time(data)
	plt.figure('Time based Histogram', (40, 30))
	# bars = []
	x = np.arange(24)
	man_list = []
	bronx_list = []
	queens_list = []
	brook_list = []
	staten_list = []
	for t in range(len(data)):
		man = 0
		bronx = 0
		queens = 0
		brook = 0
		staten = 0
		# BOROUGHS = ['MANHATTAN', 'BRONX', 'QUEENS', 'BROOKLYN', 'STATEN ISLAND']
		for incident in data[t]:
			if incident.borough == 0:
				man += 1
			elif incident.borough == 1:
				bronx += 1
			elif incident.borough == 2:
				queens += 1
			elif incident.borough == 3:
				brook += 1
			else:
				staten += 1
		# bars += [zero, one, two, 0]
		man_list.append(man)
		bronx_list.append(bronx)
		queens_list.append(queens)
		brook_list.append(brook)
		staten_list.append(staten)
	# matplot.hist(bars, bins=len(bars))#, color=COLORS, label=CLASSES)
	# xt = []
	# for b in BOROUGHS:
	# 	xt += ['', b, '', '']
	y_list = [man_list,	bronx_list, queens_list, brook_list, staten_list]
	f, a = plt.subplots()  # 40, 30)
	a.set_title('Time Based Histogram')
	a.grid(zorder=0)
	width = 0.18
	for i in range(len(BOROUGHS)):
		a.bar(x + (width * i), y_list[i], width=width, color=BOROUGH_COLORS[i], label=BOROUGHS[i], zorder=3)
	a.set_xticks(x + (5 * width / 2))
	a.set_xticklabels([i for i in range(24)])
	# a.set_yticks([0, 10, 100, 1000, 10000])
	# a.set_yscale('log')
	# a.get_yaxis().set_major_formatter(tick.ScalarFormatter())
	a.set_xlabel('HOUR')
	a.set_ylabel('COUNT')
	a.legend(BOROUGHS)  # , 'upper right')
	plt.show()

#
# def draw_time_hist_day(data):
# 	"""
# 	Draws a histogram of the count of collisions based on the hour in the day and the borough they occur in.
# 	:param data: The data
# 	:return: None.
# 	"""
# 	data = split_by_time(data)
# 	plt.figure('Time based Histogram', (40, 30))
# 	# bars = []
# 	x = np.arange(24)
# 	man_list = []
# 	bronx_list = []
# 	queens_list = []
# 	brook_list = []
# 	staten_list = []
# 	for t in range(len(data)):
# 		man = 0
# 		bronx = 0
# 		queens = 0
# 		brook = 0
# 		staten = 0
# 		# BOROUGHS = ['MANHATTAN', 'BRONX', 'QUEENS', 'BROOKLYN', 'STATEN ISLAND']
# 		for incident in data[t]:
# 			if incident.borough == 0:
# 				man += 1
# 			elif incident.borough == 1:
# 				bronx += 1
# 			elif incident.borough == 2:
# 				queens += 1
# 			elif incident.borough == 3:
# 				brook += 1
# 			else:
# 				staten += 1
# 		# bars += [zero, one, two, 0]
# 		man_list.append(man)
# 		bronx_list.append(bronx)
# 		queens_list.append(queens)
# 		brook_list.append(brook)
# 		staten_list.append(staten)
# 	# matplot.hist(bars, bins=len(bars))#, color=COLORS, label=CLASSES)
# 	# xt = []
# 	# for b in BOROUGHS:
# 	# 	xt += ['', b, '', '']
# 	y_list = [man_list,	bronx_list, queens_list, brook_list, staten_list]
# 	f, a = plt.subplots()  # 40, 30)
# 	a.set_title('Time Based Histogram')
# 	a.grid(zorder=0)
# 	width = 0.18
# 	for i in range(len(BOROUGHS)):
# 		a.bar(x + (width * i), y_list[i], width=width, color=BOROUGH_COLORS[i], label=BOROUGHS[i], zorder=3)
# 	a.set_xticks(x + (5 * width / 2))
# 	a.set_xticklabels([i for i in range(24)])
# 	# a.set_yticks([0, 10, 100, 1000, 10000])
# 	# a.set_yscale('log')
# 	# a.get_yaxis().set_major_formatter(tick.ScalarFormatter())
# 	a.set_xlabel('HOUR')
# 	a.set_ylabel('COUNT')
# 	a.legend(BOROUGHS)  # , 'upper right')
# 	plt.show()


def find_sums(data):
	"""
	Finds the total number of people and the number of pedestrians that were injured and killed.
	:param data: The data.
	:return: The number of people injured and killed, and the number of pedestrians injured and killed.
	"""
	ped_kill = 0
	ped_inj = 0
	kill = 0
	inj = 0
	for d in data:
		ped_kill += d.pedestrian_killed
		ped_inj += d.pedestrian_injured
		kill += d.killed
		inj += d.injured
	return inj, kill, ped_inj, ped_kill


def write_file(attrs, data, file):
	"""
	Writes the built data into a file.
	:param attrs: A list of the features.
	:param data: The data.
	:param file: The file.
	:return: None.
	"""
	file.write(attrs.strip(',') + '\n')
	for incident in data:
		file.write(str(incident) + '\n')


def main():
	file_in = file_check('clean.csv', 'r')
	file_out = file_check('clean_classified.csv', 'w')
	attrs, data_points = read_csv(file_in)
	print('read')
	write_file(attrs, data_points, file_out)
	print('written')
	print(find_sums(data_points))
	draw_boroughs(data_points)
	draw_map(data_points)
	draw_days(data_points)
	draw_hist(data_points)
	draw_time_hist(data_points)
	draw_time_hist_borough(data_points)

if __name__ == '__main__':
	# print(list(CLASSES + ['']) * len(BOROUGHS))
	main()
