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
fe.addLengthFeature('Complexity')
fe.addSyllableFeature(m, 'Complexity')
fe.addCollocationalFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/subtlex/lm/corpus.clean.5.bin.txt', 0, 0, 'Simplicity')
fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subimdb.5gram.unk.bin.txt', 0, 0, 'Simplicity')
fe.addCollocationalFeature('../../../../wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 0, 0, 'Simplicity')
fe.addCollocationalFeature('../../../../benchmarking/semeval/corpora/lm/simplewiki/simplewiki.5gram.bin.txt', 0, 0, 'Simplicity')
fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 0, 0, 'Simplicity')
fe.addSenseCountFeature('Simplicity')
fe.addSynonymCountFeature('Simplicity')
fe.addHypernymCountFeature('Simplicity')
fe.addHyponymCountFeature('Simplicity')
fe.addMinDepthFeature('Complexity')
fe.addMaxDepthFeature('Complexity')

ti = ThresholdIdentifier(fe)
ti.calculateTrainingFeatures(train_corpus)
ti.calculateTestingFeatures(test_corpus)
ti.trainIdentifierBruteForce(index)
labels = ti.identifyComplexWords()

o = open(output_path, 'w')
for label in labels:
	o.write(str(label) + '\n')
o.close()
