from lexenstein.rankers import *
from lexenstein.features import *
from lexenstein.morphadorner import *
import sys

test_victor_corpus = sys.argv[1].strip()
index = int(sys.argv[2].strip())
output_path = sys.argv[3].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

fe = FeatureEstimator()
#fe.addLexiconFeature('../../../semeval/corpora/basic/basic_words.txt', 'Simplicity')
#fe.addLexiconFeature('../../../semeval/corpora/vocabularies/wikisimple.vocab.txt', 'Simplicity')
#fe.addLengthFeature('Complexity')
#fe.addSyllableFeature(m, 'Complexity')
#fe.addCollocationalFeature('../../corpora/subtleximdb.5gram.bin.unk.txt', 2, 2, 'Complexity')
fe.addCollocationalFeature('../../corpora/subtleximdb.5gram.bin.unk.txt', 0, 0, 'Complexity')
#fe.addSentenceProbabilityFeature('../../corpora/subtleximdb.5gram.bin.unk.txt', 'Complexity')
#fe.addSenseCountFeature('Simplicity')
#fe.addSynonymCountFeature('Simplicity')
#fe.addHypernymCountFeature('Simplicity')
#fe.addHyponymCountFeature('Simplicity')
#fe.addMinDepthFeature('Complexity')
#fe.addMaxDepthFeature('Complexity')

br = MetricRanker(fe)
print('estimated for: ' + output_path)

ranks = br.getRankings(test_victor_corpus, index)

o = open(output_path, 'w')
for rank in ranks:
	newline = ''
	for r in rank:
		newline += r + '\t'
	o.write(newline.strip() + '\n')
o.close()
