from lexenstein.rankers import *
from lexenstein.features import *
from lexenstein.morphadorner import *
import sys

test_victor_corpus = sys.argv[1].strip()
index = int(sys.argv[2].strip())
out = sys.argv[3].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

fe = FeatureEstimator()
fe.addWordVectorSimilarityFeature('../../../lexmturk/corpora/word_vectors_all.bin', 'Simplicity')
fe.addNGramFrequencyFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 1, 0, 'Complexity')
fe.addNGramFrequencyFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 0, 1, 'Complexity')
fe.addNGramFrequencyFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 1, 1, 'Complexity')
fe.addNGramFrequencyFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 2, 0, 'Complexity')
fe.addNGramFrequencyFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 0, 2, 'Complexity')
fe.addNGramFrequencyFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 2, 1, 'Complexity')
fe.addNGramFrequencyFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 1, 2, 'Complexity')
fe.addNGramFrequencyFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 2, 2, 'Complexity')
fe.addTranslationProbabilityFeature('/export/data/ghpaetzold/LEXenstein/corpora/translation_probabilities_lexmturkall.txt', 'Simplicity')

br = MetricRanker(fe)
selected = br.getRankings(test_victor_corpus, index)

outf = open(out, 'w')
vicf = open(test_victor_corpus)
for cands in selected:
        data = vicf.readline().strip().split('\t')
	ocands = data[3:len(data)]
        newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t'
        for cand in cands:
                newline += '0:'+cand + '\t'
        outf.write(newline.strip() + '\n')
outf.close()
vicf.close()
