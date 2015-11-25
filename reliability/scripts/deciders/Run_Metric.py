from lexenstein.rankers import *
from lexenstein.features import *
from lexenstein.morphadorner import *
import sys

test_victor_corpus = sys.argv[1].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

fe = FeatureEstimator()
fe.addLengthFeature('Complexity')
#fe.addSyllableFeature(m, 'Complexity')
fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 0, 0, 'Simplicity')
fe.addCollocationalFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/subtlex/lm/corpus.clean.5.bin.txt', 0, 0, 'Complexity')
fe.addCollocationalFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/simplewiki.5.bin.txt', 0, 0, 'Complexity')
fe.addCollocationalFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 0, 0, 'Simplicity')
fe.addCollocationalFeature('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/brown.5gram.bin.txt', 0, 0, 'Simplicity')

fe.addNGramProbabilityFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 1, 0, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 0, 1, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 1, 1, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 2, 0, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 2, 1, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 0, 2, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 1, 2, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/wordnetlmranking/corpora/corpus/wiki/lm/corpus.clean.5.bin.txt', 2, 2, 'Simplicity')

fe.addSenseCountFeature('Simplicity')
fe.addSynonymCountFeature('Simplicity')
fe.addHypernymCountFeature('Simplicity')
fe.addHyponymCountFeature('Simplicity')
fe.addMinDepthFeature('Complexity')
fe.addMaxDepthFeature('Complexity')

flabels = []
flabels.append('length')
#flabels.append('syllable')
flabels.append('subimdb00')
flabels.append('subtlex00')
flabels.append('simplewiki00')
flabels.append('wiki00')
flabels.append('brown00')
flabels.append('wiki10')
flabels.append('wiki01')
flabels.append('wiki11')
flabels.append('wiki20')
flabels.append('wiki21')
flabels.append('wiki02')
flabels.append('wiki12')
flabels.append('wiki22')
flabels.append('senses')
flabels.append('synonyms')
flabels.append('hypernyms')
flabels.append('hyponyms')
flabels.append('mindepth')
flabels.append('maxdepth')

br = MetricRanker(fe)

for i in range(0, len(flabels)):
	decider = flabels[i]
	data = test_victor_corpus[:len(test_victor_corpus)-4].split('_')
	generator = data[0]
	selector = data[1]
	ranker = data[2]

        ranks = br.getRankings('../../problems/'+test_victor_corpus, i)

        output_path = '../../decisions/'+generator+'_'+selector+'_'+ranker+'_'+decider+'.txt'

        o = open(output_path, 'w')
        for rank in ranks:
                newline = ''
                for r in rank:
                        newline += r + '\t'
                o.write(newline.strip() + '\n')
        o.close()
