from lexenstein.selectors import *
import sys

generator = sys.argv[1]
victor_corpus = sys.argv[2]
out = sys.argv[3].strip()

def getSubs(generator):
	result = {}
	f = open('../../corpora/lexmturk_gold_test.txt')
	for line in f:
		data = line.strip().split('\t')
		target = data[1].strip()
		candidates = set([cand.split(':')[1] for cand in data[3:len(data)]])
		print(str(candidates))
		if target in result.keys():
			result[target].update(candidates)
		else:
			result[target] = candidates
	f.close()
	return result

subs = getSubs(generator)

voidselector = VoidSelector()
selected = voidselector.selectCandidates(subs, victor_corpus)

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
