from lexenstein.morphadorner import *
from lexenstein.identifiers import *
from lexenstein.features import *
import sys

train_victor_corpus = sys.argv[1]
k = sys.argv[2].strip()
if k!='all':
	k = int(sys.argv[2].strip())
n_estimators = int(sys.argv[3].strip())
criterion = sys.argv[4].strip()
classw = sys.argv[5].strip()
max_features = sys.argv[6].strip()
if max_features=='None':
	max_features = None
test_victor_corpus = sys.argv[7].strip()
out_file = sys.argv[8].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

fe = FeatureEstimator(norm=False)
fe.addLexiconFeature('../../../semeval/corpora/basic/basic_words.txt', 'Simplicity')
fe.addLengthFeature('Complexity')
fe.addCollocationalFeature('../../../../benchmarking/semeval/corpora/lm/simplewiki/simplewiki.5gram.bin.txt', 2, 2, 'Complexity')
fe.addSenseCountFeature('Simplicity')
fe.addSynonymCountFeature('Simplicity')
fe.addHypernymCountFeature('Simplicity')
fe.addHyponymCountFeature('Simplicity')

mli = MachineLearningIdentifier(fe)
mli.calculateTrainingFeatures(train_victor_corpus)
mli.calculateTestingFeatures(test_victor_corpus)
mli.selectKBestFeatures(k=k)
mli.trainExtraTreesClassifier(n_estimators=n_estimators, criterion=criterion, max_features=max_features)
labels = mli.identifyComplexWords()

o = open(out_file, 'w')
for label in labels:
	o.write(str(label) + '\n')
o.close()
