from lexenstein.identifiers import *
from lexenstein.features import *
from lexenstein.morphadorner import *
import sys

test_corpus = sys.argv[1].strip()
train_corpus = sys.argv[2].strip()
index = int(sys.argv[3].strip())
output_path = sys.argv[4].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

fe = FeatureEstimator()
fe.addNGramFrequencyFeature('/export/data/ghpaetzold/benchmarking/subimdb/corpora/onegramshelves/simplewiki', 0, 0, 'Simplicity')

ti = ThresholdIdentifier(fe)
ti.calculateTrainingFeatures(train_corpus)
ti.calculateTestingFeatures(test_corpus)
ti.trainIdentifierBruteForce(index)
labels = ti.identifyComplexWords()

o = open(output_path, 'w')
for label in labels:
	o.write(str(label) + '\n')
o.close()
