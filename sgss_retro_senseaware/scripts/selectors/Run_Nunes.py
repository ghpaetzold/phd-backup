from lexenstein.selectors import *
import sys

generator = sys.argv[1]
victor_corpus = sys.argv[2]
out = sys.argv[3].strip()

def getSubs(generator):
	result = {}
	f = open('../../substitutions/' + generator + '/substitutions.txt')
	for line in f:
		data = line.strip().split('\t')
		target = data[0].strip()
		candidates = data[1].strip().split('|||')
		result[target] = candidates
	f.close()
	return result

subs = getSubs(generator)

pos_model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
stanford_tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
condprob_model = '/export/data/ghpaetzold/LEXenstein/corpora/POS_condprob_model.bin'
java_path = '/usr/bin/java'

selector = NunesSelector(condprob_model, pos_model, stanford_tagger, java_path)
selected = selector.selectCandidates(subs, victor_corpus)

outf = open(out, 'w')
vicf = open(victor_corpus)
for cands in selected:
	data = vicf.readline().strip().split('\t')
	newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t'
	for cand in cands:
		newline += '0:'+cand + '\t'
	outf.write(newline.strip() + '\n')
outf.close()
vicf.close()
