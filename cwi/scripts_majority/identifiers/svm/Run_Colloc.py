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
fe.addCollocationalFeature('../../../../semeval/corpora/lm/subtleximdb/subtleximdb.5gram.unk.bin.txt', 2, 2, 'Complexity')

mli = MachineLearningIdentifier(fe)
mli.calculateTrainingFeatures(train_victor_corpus)
mli.calculateTestingFeatures(test_victor_corpus)
mli.selectKBestFeatures(k=k)
mli.trainSVM(C=C, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, class_weight='auto')
labels = mli.identifyComplexWords()

o = open(out_file, 'w')
for label in labels:
	o.write(str(label) + '\n')
o.close()
