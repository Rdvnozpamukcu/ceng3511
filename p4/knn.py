from random import randrange
from csv import reader
from math import sqrt
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def load_csv(filename):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset

def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())

def str_column_to_int(dataset, column):
    class_values = [row[column] for row in dataset]
    unique = set(class_values)
    lookup = dict()
    for i, value in enumerate(unique):
        lookup[value] = i
        print('[%s] => %d' % (value, i))
    for row in dataset:
        row[column] = lookup[row[column]]
    return lookup

def dataset_minmax(dataset):
    minmax = list()
    for i in range(len(dataset[0])):
        col_values = [row[i] for row in dataset]
        value_min = min(col_values)
        value_max = max(col_values)
        minmax.append([value_min, value_max])
    return minmax

def normalize_dataset(dataset, minmax):
    for row in dataset:
        for i in range(len(row)):
            row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])

def cross_validation_split(dataset, n_folds):
    dataset_split = list()
    dataset_copy = list(dataset)
    fold_size = int(len(dataset) / n_folds)
    for _ in range(n_folds):
        fold = list()
        while len(fold) < fold_size:
            index = randrange(len(dataset_copy))
            fold.append(dataset_copy.pop(index))
        dataset_split.append(fold)
    return dataset_split

def accuracy_metric(actual, predicted):
    correct = 0
    for i in range(len(actual)):
        if actual[i] == predicted[i]:
            correct += 1
    return correct / float(len(actual)) * 100.0

def euclidean_distance(row1, row2):
    distance = 0.0
    for i in range(len(row1)-1):
        distance += (row1[i] - row2[i])**2
    return sqrt(distance)

def get_neighbors(train, test_row, num_neighbors):
    distances = list()
    for train_row in train:
        dist = euclidean_distance(test_row, train_row)
        distances.append((train_row, dist))
    distances.sort(key=lambda tup: tup[1])
    neighbors = list()
    for i in range(num_neighbors):
        neighbors.append(distances[i][0])
    return neighbors

def predict_classification(train, test_row, num_neighbors):
    neighbors = get_neighbors(train, test_row, num_neighbors)
    output_values = [row[-1] for row in neighbors]
    prediction = max(set(output_values), key=output_values.count)
    return prediction

def confusion_matrix(actual, predicted):
    classes       = np.unique(np.concatenate((actual,predicted)))
    confusion_mtx = np.empty((len(classes),len(classes)),dtype=np.int)
    for i,a in enumerate(classes):
        for j,p in enumerate(classes):
            confusion_mtx[i,j] = np.where((actual==a)*(predicted==p))[0].shape[0]
    return confusion_mtx


n_folds = 4
num_neighbors = 10
train_file = './train.txt'
test_file = './test.txt'
dataset = load_csv(train_file)[1:]
test_dataset = load_csv(test_file)[1:]

for i in range(len(test_dataset[0])-1):
    str_column_to_float(test_dataset, i)

test_converter = str_column_to_int(test_dataset, len(test_dataset[0])-1)

print('Test is starting...')
correct_predict = 0
predicts = []
reals = []
for row in test_dataset:
    label = predict_classification(test_dataset, row[:-1], num_neighbors)
    predict = list(test_converter.keys())[list(test_converter.values()).index(label)]
    real = list(test_converter.keys())[list(test_converter.values()).index(row[-1])]
    reals.append(real)
    predicts.append(predict)
    # print('Data=%s, Predicted: %s, Real: %s' % (row[0], predict, real))
    if predict == real:
        correct_predict += 1

print('Test Mean Accuracy: %.3f%%' % (correct_predict/len(test_dataset)))

conf_mat = confusion_matrix(np.array(reals), np.array(predicts))
ax = sns.heatmap(conf_mat, linewidth=0.5)
plt.show()