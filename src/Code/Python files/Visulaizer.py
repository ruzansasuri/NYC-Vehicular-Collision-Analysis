from matplotlib import pyplot as matplot

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

	attrs = file.readline().strip().split(',')
	for i in range(len(attrs)):
		attrs[i] = attrs[i].strip()
	data_points = []
	i = 0
	while i < len(attrs):
	# for i in range(len(attrs)):
		if attrs[i].lower() == 'latitude':
			break
		i += 1
	j = 0
	matplot.figure("Map", (30, 10))
	matplot.title('Map')
	j = 0
	for line in file:
		if line == '\n' or line.strip() == '':
			continue
		line = line.strip().split(',')
		# point = []
		# for ind in range(len(line)):
		# 	point.append(line[ind]))
		data_points.append(line)
		if line[i] != '' and line[i + 1] != '':
			matplot.plot(float(line[i]), float(line[i + 1]), 'b^')
			# print(float(line[i]), float(line[i + 1]))
		print(j)
		j += 1
	print('ready')
	matplot.show()
	return attrs, data_points


def draw_map(data, idx):
	# x_list = []
	# y_list = []
	for point in data:
		# x_list.append(point[idx])
		# y_list.append(point[idx + 1])
		if point[idx] != '' and point[idx + 1] != '':
			matplot.plot(float(point[idx]), float(point[idx + 1]))
	matplot.figure("Map", (30, 10))
	matplot.title('Map')
	matplot.show()


def main():
	file_in = file_check('database.csv', 'r')
	attrs, data_points = read_csv(file_in)
	# draw_map(data_points, i)


if __name__ == '__main__':
    main()