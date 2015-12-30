from sklearn import linear_model
import sys, numpy, pickle
from sklearn.preprocessing import normalize
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
from sklearn import tree

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
k = sys.argv[2].strip()
if k!='all':
	k = int(sys.argv[2].strip())
max_features = None
try:
	max_features = float(sys.argv[3].strip())
except ValueError:
	max_features = sys.argv[3].strip()
max_depth = None
try:
	max_depth = float(sys.argv[4].strip())
except ValueError:
	max_depth = None
test_victor_corpus = sys.argv[5].strip()
out_file = sys.argv[6].strip()

Xtr, Xte = getFeatures()
Ytr = getLabels(train_victor_corpus)
feature_selector = SelectKBest(f_classif, k=k)
feature_selector.fit(Xtr, Ytr)
Xtr = feature_selector.transform(Xtr)
Xte = feature_selector.transform(Xte)

classifier = tree.DecisionTreeClassifier(criterion='gini', splitter='best', max_features=max_features, max_depth=max_depth)
classifier.fit(Xtr, Ytr)
labels = classifier.predict(Xte)

o = open(out_file, 'w')
for label in labels:
	o.write(str(label) + '\t' + str(label) + '\n')
o.close()
