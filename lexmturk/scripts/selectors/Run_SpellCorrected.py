from lexenstein.selectors import *
from lexenstein.spelling import *
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

selected = []
sc = NorvigCorrector('/export/data/ghpaetzold/LEXenstein/corpora/wiki_simplewiki.txt')
f = open(victor_corpus)
for line in f:
	data = line.strip().split('\t')
	target = data[1].strip()
	if target in subs.keys():
		fixed = set([])
		for cand in subs[target]:
			if len(cand)>1:
				fixed.add(sc.correct(cand))
		selected.append(fixed)
	else:
		selected.append(set([]))

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
