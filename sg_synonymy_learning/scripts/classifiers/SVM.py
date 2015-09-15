from sklearn import svm
import sys, numpy, pickle
from sklearn.preprocessing import normalize
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

def writeModel(classifier, model_file):
        pickle.dump(classifier, open(model_file, "wb"))

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
        return X, Y

def writeLabels(labels, file):
	c = -1
	for l in labels:
		c += 1
		file.write(str(l) + '\n')
	file.close()

def writeModel(classifier, model_file):
        pickle.dump(classifier, open(model_file, "wb"))

C = float(sys.argv[1])
kernel = sys.argv[2]
degree = int(sys.argv[3])
gamma = float(sys.argv[4])
coef0 = float(sys.argv[5])
Xtr, Ytr = readXY(sys.argv[6])
Xte, Yte = readXY(sys.argv[7])
o = open(sys.argv[8], 'w')
model_file = sys.argv[9]

classifier = svm.SVC(C=C, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0)
classifier.fit(Xtr, Ytr)

labels = classifier.predict(Xte)

writeLabels(labels, o)
writeModel(classifier, model_file)
