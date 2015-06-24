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
fe.addCollocationalFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/subtlex/lm/corpus.clean.5.bin.txt', 0, 0, 'Complexity')
fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/100415/corpus.5gram.bin.unk.txt', 0, 0, 'Complexity')
fe.addCollocationalFeature('../../../../wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 0, 0, 'Complexity')
fe.addCollocationalFeature('../../../../benchmarking/semeval/corpora/lm/simplewiki/simplewiki.5gram.bin.txt', 0, 0, 'Complexity')
fe.addCollocationalFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 2, 2, 'Complexity')
fe.addSentenceProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 'Complexity')
fe.addSenseCountFeature('Simplicity')
fe.addSynonymCountFeature('Simplicity')
fe.addHypernymCountFeature('Simplicity')
fe.addHyponymCountFeature('Simplicity')
fe.addMinDepthFeature('Complexity')
fe.addMaxDepthFeature('Complexity')

for ident in fe.identifiers:
	print(str(ident))

ti = ThresholdIdentifier(fe)
ti.calculateTrainingFeatures(train_corpus)
ti.calculateTestingFeatures(test_corpus)
ti.trainIdentifierBruteForce(index)
labels = ti.identifyComplexWords()
probabilities = ti.getConfidenceScores()

o = open(output_path, 'w')
for i in range(0, len(labels)):
        label = labels[i]
        prob = probabilities[i]
        o.write(str(label) + '\t' + str(prob) + '\n')
o.close()
