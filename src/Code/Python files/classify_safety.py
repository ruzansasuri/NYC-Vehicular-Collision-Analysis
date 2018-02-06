from matplotlib import pyplot as matplot
import datetime as dt

CLASSES = ['Safe', 'Injured', 'Killed']
DAYS = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
BOROUGHS = ['MANHATTAN', 'BRONX', 'QUEENS', 'BROOKLYN', 'STATEN ISLAND']


class Incident:
	__slots__ = 'id', 'date', 'day', 'time', 'time_class', 'borough', 'latitude', 'longitude', 'injured', 'killed', \
				'safety_class'

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
		return str(self.id) + ',' + str(self.day) + ',' + str(self.time_class) + ',' + BOROUGHS[self.borough] + ',' +\
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
    :return: list of attributes, list of data points and list of attributes to ignore.
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
	class2 = False
	class1 = False
	class0 = False
	matplot.figure(name, (30, 10))
	matplot.title(name)
	point = ['ro', 'go', 'bo']
	for incident in data:
		x = incident.longitude
		y = incident.latitude
		safety_class = incident.safety_class
		if not class2 and safety_class == 2:
			matplot.plot(x, y, point[safety_class], label=CLASSES[safety_class])
			class2 = True
		elif not class1 and safety_class == 1:
			matplot.plot(x, y, point[safety_class], label=CLASSES[safety_class])
			class1 = True
		elif not class0 and safety_class == 0:
			matplot.plot(x, y, point[safety_class], label=CLASSES[safety_class])
			class0 = True
		else:
			matplot.plot(x, y, point[safety_class])
	matplot.legend(loc='upper right')
	matplot.show()


def split_by_day(data):
	day_data = [[] for _ in range(7)]
	for incident in data:
		day_data[incident.day].append(incident)
	return day_data


def split_by_borough(data):
	borough_data = [[] for _ in range(len(BOROUGHS))]
	for incident in data:
		borough_data[incident.borough].append(incident)
	return borough_data


def draw_days(data):
	day_data = split_by_day(data)
	print('split')
	for day in range(len(DAYS)):
		draw_map(day_data[day], DAYS[day])


def draw_boroughs(data):
	boroughs = split_by_borough(data)
	for borough in range(len(BOROUGHS)):
		draw_map(boroughs[borough], BOROUGHS[borough])


def write_file(attrs, data, file):
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
	# draw_map(data_points)
	# draw_days(data_points)
	draw_boroughs(data_points)

if __name__ == '__main__':
    main()