from lexenstein.rankers import *
from lexenstein.features import *
from lexenstein.morphadorner import *
import sys

test_victor_corpus = sys.argv[1].strip()
index = int(sys.argv[2].strip())
out = sys.argv[3].strip()
proportion = int(sys.argv[4].strip())

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

fe = FeatureEstimator()
fe.addNGramProbabilityFeature('/export/data/ghpaetzold/subtitlesimdb/corpora/160715/subtleximdb.5gram.unk.bin.txt', 2, 2, 'Simplicity')

br = MetricRanker(fe)
selected_raw = br.getRankings(test_victor_corpus, index)

#For each proportion, select and save:
selected = []
for inst in selected_raw:
	selected.append(inst[0:min(proportion, len(inst))])
	outf = open(out, 'w')
	vicf = open(test_victor_corpus)
	for cands in selected:
		data = vicf.readline().strip().split('\t')
		newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t'
		for cand in cands:
			newline += '0:'+cand + '\t'
		outf.write(newline.strip() + '\n')
	outf.close()
	vicf.close()
