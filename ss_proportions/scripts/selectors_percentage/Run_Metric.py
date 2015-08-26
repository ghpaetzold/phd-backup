from lexenstein.rankers import *
from lexenstein.features import *
from lexenstein.morphadorner import *
import sys

test_victor_corpus = sys.argv[1].strip()
index = int(sys.argv[2].strip())
out = sys.argv[3].strip()

def getTaggedSents(corpus):
        result = []
        f = open(corpus)
        for line in f:
                tags = []
                tokens = line.strip().split(' ')
                for token in tokens:
                        tokendata = token.strip().split('|||')
                        tags.append((tokendata[0].strip(), tokendata[1].strip()))
                result.append(tags)
        return result

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

condprob_model = '/export/data/ghpaetzold/corpora/pos_tag_conditional_probabilities/simplewiki_condprob_model.bin'
model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
java = '/usr/bin/java'

fe = FeatureEstimator()
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 2, 2, 'Simplicity')

br = MetricRanker(fe)
tagged_sents = getTaggedSents('../../corpora/tagged_sents_lexmturk_test.txt')
br.fe.temp_resources['tagged_sents'] = tagged_sents
selected_raw = br.getRankings(test_victor_corpus, index)

#For each proportion, select and save:
proportions = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
for proportion in proportions:
	selected = []
	for inst in selected_raw:
		selected.append(inst[0:max(1, int(proportion*len(inst)))])
		print('Len: ' + str(len(inst[0:max(1, int(proportion*len(inst)))])))

        outf = open(out + '_' + str(proportion) + '.txt', 'w')
        vicf = open(test_victor_corpus)
        for cands in selected:
                data = vicf.readline().strip().split('\t')
                newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t'
                for cand in cands:
                        newline += '0:'+cand + '\t'
                outf.write(newline.strip() + '\n')
        outf.close()
        vicf.close()
