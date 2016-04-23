from sklearn import linear_model
import sys, numpy, pickle
from sklearn.preprocessing import normalize
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn import tree
from sklearn import ensemble

def getFeatures():
	Xtr = []
	Xte = []
	f = open('features_training.txt')
	for line in f:
		Xtr.append([float(v) for v in line.strip().split(' ')])
	f.close()
	f = open('features_testing.txt')
	for line in f:
		Xte.append([float(v) for v in line.strip().split(' ')])
	f.close()
	return Xtr, Xte

def getLabels(corpus):
	Y = []
	f = open(corpus)
	for line in f:
		data = line.strip().split('\t')
		label = int(data[2].strip())
		Y.append(label)
	f.close()
	return Y

train_victor_corpus = sys.argv[1]
test_victor_corpus = sys.argv[2].strip()
out_file = sys.argv[3].strip()

k = 'all'
Xtr, Xte = getFeatures()
Ytr = getLabels(train_victor_corpus)
feature_selector = SelectKBest(f_classif, k=k)
feature_selector.fit(Xtr, Ytr)
Xtr = feature_selector.transform(Xtr)
Xte = feature_selector.transform(Xte)

classifier = ensemble.GradientBoostingClassifier()
classifier.fit(Xtr, Ytr)
labels = classifier.predict(Xte)

o = open(out_file, 'w')
for label in labels:
	o.write(str(label) + '\t' + str(label) + '\n')
o.close()
