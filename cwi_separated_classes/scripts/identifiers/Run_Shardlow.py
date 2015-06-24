from lexenstein.morphadorner import *
from lexenstein.identifiers import *
from lexenstein.features import *
import sys

train_victor_corpus = sys.argv[1]
k = None
try:
	k = int(sys.argv[2].strip())
except ValueError:
	k = 'all'
C = float(sys.argv[3].strip())
kernel = sys.argv[4].strip()
degree = float(sys.argv[5].strip())
gamma = float(sys.argv[6].strip())
coef0 = float(sys.argv[7].strip())
test_victor_corpus = sys.argv[8].strip()
out_file = sys.argv[9].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

fe = FeatureEstimator()
fe.addLengthFeature('Complexity')
fe.addSyllableFeature(m, 'Complexity')
fe.addCollocationalFeature('../../../../machinelearningranking/corpora/lm/subtlex.5gram.bin.txt', 0, 0, 'Complexity')
fe.addCollocationalFeature('../../../../machinelearningranking/corpora/lm/oneperdoc.subimdb.2.bin.txt', 0, 0, 'Complexity')
fe.addSenseCountFeature('Simplicity')
fe.addSynonymCountFeature('Simplicity')

classes = ['N', 'V', 'J', 'A', 'O']
predicted = {}
for c in classes:
	train_corpus = train_victor_corpus + '_' + c + '.txt'
	test_corpus = test_victor_corpus + '_' + c + '.txt'

	mli = MachineLearningIdentifier(fe)
	mli.calculateTrainingFeatures(train_corpus)
	mli.calculateTestingFeatures(test_corpus)
	mli.selectKBestFeatures(k=k)
	mli.trainSVM(C=C, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, class_weight='auto')
	labels = mli.identifyComplexWords()

	o = open(out_file+'_'+str(c)+'.txt', 'w')
	for label in labels:
		o.write(str(label) + '\n')
	o.close()
