from lexenstein.rankers import *
from lexenstein.features import *
import sys

victor_corpus = sys.argv[1]
test_victor_corpus = sys.argv[2].strip()
output_path = sys.argv[3].strip()

model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
java = '/usr/bin/java'

fe = FeatureEstimator()
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 1, 0, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 0, 1, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 1, 1, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 2, 0, 'Simplicity')
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 0, 2, 'Simplicity')
#fe.addCollocationalFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 1, 1, 'Simplicity')
w2vmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_200_glove.bin'
fe.addWordVectorSimilarityFeature(w2vmodel, 'Simplicity')
fe.addWordVectorContextSimilarityFeature(w2vmodel, model, tagger, java, 'Simplicity')

br = GlavasRanker(fe)
ranks = br.getRankings(test_victor_corpus)

lm = kenlm.LanguageModel('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt')

o = open(output_path, 'w')
f = open(test_victor_corpus)
for rank in ranks:
        target = f.readline().strip().split('\t')[1].strip()
        targetp = lm.score(target)
        newline = ''
        if len(rank)>0:
                candp = lm.score(rank[0])
                if targetp>=candp:
                        newline = target + '\t'
                else:
                        newline = ''
                for r in rank:
                        newline += r + '\t'
        else:
                newline = target
        o.write(newline.strip() + '\n')
o.close()
