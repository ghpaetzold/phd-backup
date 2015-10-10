from sklearn import linear_model
import sys, numpy, pickle
from sklearn.preprocessing import normalize
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

def readXY(xf):
	X = []
	Y = []
	for line in open(xf):
		data = line.strip().split('\t')
		values = [float(v) for v in data[0].split(' ')]
		X.append(values)
		Y.append(int(data[1]))
	X = numpy.array(X)
	Y = numpy.array(Y)
	print(str(X))
	print(str(Y))
	return X, Y

def writeLabels(labels, file):
	c = -1
	for l in labels:
		c += 1
		file.write(str(l) + '\n')
	file.close()

def writeModel(classifier, model_file):
	pickle.dump(classifier, open(model_file, "wb"))

loss = sys.argv[1]
penalty = sys.argv[2]
alpha = float(sys.argv[3])
l1_ratio = float(sys.argv[4])
Xtr, Ytr = readXY(sys.argv[5])
Xte, Yte = readXY(sys.argv[6])
o = open(sys.argv[7], 'w')

classifier = linear_model.SGDClassifier(loss=loss, penalty=penalty, alpha=alpha, l1_ratio=l1_ratio)
classifier.fit(Xtr, Ytr)

labels = classifier.predict(Xte)

writeLabels(labels, o)
