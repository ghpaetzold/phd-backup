from lexenstein.selectors import *
import sys

generator = sys.argv[1]
victor_corpus = sys.argv[2]
cooc_model = sys.argv[3]
common_distance = float(sys.argv[4])
candidate_distance = float(sys.argv[5])
out = sys.argv[6].strip()

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

biranselector = BiranSelector(cooc_model)
selected = biranselector.selectCandidates(subs, victor_corpus, common_distance, candidate_distance)

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
