from lexenstein.rankers import *
from lexenstein.features import *
from lexenstein.morphadorner import *
import sys

test_victor_corpus = sys.argv[1].strip()
index = int(sys.argv[2].strip())
output_path = sys.argv[3].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

fe = FeatureEstimator()
fe.addLengthFeature('Complexity')
fe.addSyllableFeature(m, 'Complexity')
fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 0, 0, 'Simplicity')
fe.addCollocationalFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/subtlex/lm/corpus.clean.5.bin.txt', 0, 0, 'Complexity')
fe.addCollocationalFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/simplewiki.5.bin.txt', 0, 0, 'Complexity')
fe.addCollocationalFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 0, 0, 'Simplicity')
fe.addCollocationalFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/brown.5gram.bin.txt', 0, 0, 'Simplicity')

fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 2, 2, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/subtlex/lm/corpus.clean.5.bin.txt', 2, 2, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/simplewiki.5.bin.txt', 2, 2, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 2, 2, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/brown.5gram.bin.txt', 2, 2, 'Simplicity')
#fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 1, 0, 'Simplicity')
#fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 0, 1, 'Simplicity')
#fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 1, 1, 'Simplicity')
#fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 2, 0, 'Simplicity')
#fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 2, 1, 'Simplicity')
#fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 0, 2, 'Simplicity')
#fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 1, 2, 'Simplicity')
#fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 2, 2, 'Simplicity')

fe.addSenseCountFeature('Simplicity')
fe.addSynonymCountFeature('Simplicity')
fe.addHypernymCountFeature('Simplicity')
fe.addHyponymCountFeature('Simplicity')
fe.addMinDepthFeature('Complexity')
fe.addMaxDepthFeature('Complexity')

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
