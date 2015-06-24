from lexenstein.morphadorner import *
from lexenstein.identifiers import *
from lexenstein.features import *
import sys

train_victor_corpus = sys.argv[1]
k = sys.argv[2].strip()
if k!='all':
	k = int(sys.argv[2].strip())
criterion = sys.argv[3].strip()
splitter = sys.argv[4].strip()
max_features = None
try:
	max_features = float(sys.argv[5].strip())
except ValueError:
	max_features = sys.argv[5].strip()
max_depth = None
try:
	max_depth = float(sys.argv[6].strip())
except ValueError:
	max_depth = None
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

classes = ['N', 'V', 'J', 'A', 'O']
predicted = {}
for c in classes:
	train_corpus = train_victor_corpus + '_' + c + '.txt'
	test_corpus = test_victor_corpus + '_' + c + '.txt'

	mli = MachineLearningIdentifier(fe)
	mli.calculateTrainingFeatures(train_corpus)
	mli.calculateTestingFeatures(test_corpus)
	mli.selectKBestFeatures(k=k)
	mli.trainDecisionTreeClassifier(criterion=criterion, splitter=splitter, max_features=max_features, max_depth=max_depth)
	labels = mli.identifyComplexWords()
	
	o = open(out_file+'_'+str(c)+'.txt', 'w')
	for label in labels:
		o.write(str(label) + '\n')
	o.close()