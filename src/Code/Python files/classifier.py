"""
Authors: Ruzan Sasuri(rps7183)
		 Anuj Chheda(akc9782)
Date: Dec 4th, 2017.
"""
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from matplotlib import pyplot as plt

ATTRIBUTES = ['ID', 'DATE', 'TIME', 'BOROUGH', 'LATITUDE', 'LONGITUDE', 'CLASS']
SPLIT = .7
COLORS = ['b', 'r', 'k', 'c', 'm', 'y', 'g']


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
    :return: list of attributes, list of data points and list of classes.
    """
	attrs = file.readline().strip().split(',')[1:]
	for i in range(len(attrs)):
		attrs[i] = attrs[i].strip()
	data_points = []
	classes = []
	for line in file:
		if line == '\n' or line.strip() == '':
			continue
		line = line.strip().split(',')[1:]
		point = [int(line[0]), int(line[1]), int(line[2]), float(line[3]), float(line[4])]
		data_points.append(point)
		classes.append(int(line[-1]))
	return attrs, np.array(data_points), np.array(classes)


def train_test_split(data, classes):
	"""
	Splits the data into a training data and test data.
	:param data: The data.
	:param classes: A list of classes.
	:return: Lists of the training data, testing data, training classes and testing classes.
	"""
	split_row = int(len(data) * SPLIT)
	train_data = data[:split_row]
	test_data = data[split_row:]
	train_class = classes[:split_row]
	test_class = classes[split_row:]
	return train_data, test_data, train_class, test_class


def classify(train_data, test_data, train_class, test_class, classifier):
	"""
	Classifies the data based on the given classifier and finds the accuracy of the resulting classes.
	:param train_data: The training data.
	:param test_data: The testing data.
	:param train_class: The list of training classes.
	:param test_class: The list of testing classes.
	:param classifier: The sklearn classifier.
	:return: The accuracy of the testing results.
	"""
	classifier.fit(train_data, train_class)
	correct = 0
	y_pred = classifier.predict(test_data)
	for i in range(len(test_class)):
		if y_pred[i] == test_class[i]:
			correct += 1
	accuracy = correct / len(test_data)
	return accuracy


def knn(train_data, test_data, train_class, test_class):
	"""
	Uses sklearn's KNeighborsClassifier in sklearn. We run it for k values from 1 to 100 that are not multiples of 3 to avoid
	breaking a tie.
	:param train_data: The training data.
	:param test_data: The testing data.
	:param train_class: The list of training classes.
	:param test_class: The list of testing classes.
	:return: The lis of accuracies for each k value.
	"""
	accuracy = []
	k_list = []
	for k in range(1, 101):
		if k % 3 == 0:
			continue
		k_list.append(k)
		knn = KNeighborsClassifier(n_neighbors=k)
		accuracy.append(classify(train_data, test_data, train_class, test_class, knn))
	draw_graph(k_list, accuracy, 'kNN', special_point=(10, accuracy[6]), xt=[i for i in range(1, 101, 3)])
	return accuracy


def random_forest(train_data, test_data, train_class, test_class):
	"""
	Uses sklearn's RandomForestClassifier in sklearn. We run it for n values from 1 to 100.
	:param train_data: The training data.
	:param test_data: The testing data.
	:param train_class: The list of training classes.
	:param test_class: The list of testing classes.
	:return: The lis of accuracies for each k value.
	"""
	accuracy = []
	last_accuracy = -1
	for n in range(1, 101):
		rfc = RandomForestClassifier(n_estimators=n)
		acc = classify(train_data, test_data, train_class, test_class, rfc)
		if n % 2 != 0:
			last_accuracy = acc
		else:
			accuracy.append((acc + last_accuracy) / 2)
	draw_graph([n for n in range(2, 101, 2)], accuracy, 'Random Forest Classifier', special_point=(16, accuracy[7]))
	return accuracy


def draw_graph(x_list, y_list, name='', special_point=None, xt=None):
	"""
	Draws the graph of accuracy vs k.
	:param xt: The list of xticks if needed. Default value is None.
	:param special_point: A speial point to mark on the graph if needed. Default value is None.
	:param x_list: The list of k's used.
	:param y_list: The list of accuracies.
	:param name: Name of the graph.
	:return: None
	"""
	plt.figure(name, (30, 10))
	f, a = plt.subplots()
	a.set_title('Accuracy vs k')
	a.plot(x_list, y_list, 'b-')
	if special_point is not None:
		a.plot([0, special_point[0]], [special_point[1], special_point[1]], 'k--')
		a.plot([special_point[0], special_point[0]], [0.69, special_point[1]], 'k--')
		a.plot(special_point[0], special_point[1], 'r', label='Knee Point when k = ' + str(special_point[0]))
	a.set_xlabel('k')
	a.set_ylabel('Accuracy')
	a.set_xlim(xmin=0)
	a.set_ylim(ymin=0.69)
	if xt is None:
		a.set_xticks(x_list)
	else:
		a.set_xticks(xt)
	a.set_yticks([i / 100 for i in range(70, 85)])
	a.grid()
	plt.show()


def main():
	file = file_check('clean_classified.csv', 'r')
	attrs, data, classes = read_csv(file)
	train_data, test_data, train_class, test_class = train_test_split(data, classes)
	print(data.shape, classes.shape)
	print(data)
	print(classes)
	accuracy_knn = knn(train_data, test_data, train_class, test_class)
	print('knn', accuracy_knn)
	accuracy_rf = random_forest(train_data, test_data, train_class, test_class)
	print('random forest', accuracy_rf)

if __name__ == '__main__':
	main()
