from lexenstein.generators import *
from lexenstein.morphadorner import *
from lexenstein.spelling import *
import sys

victor_corpus = sys.argv[1].strip()

w2v = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_200_glove.bin'

kg = GlavasGenerator(w2v)
subs = kg.getSubstitutions(victor_corpus, 10)

out = open('../../substitutions/glavas/substitutions.txt', 'w')
for k in subs.keys():
	newline = k + '\t'
	if len(subs[k])>0:
		for c in subs[k]:
			newline += c + '|||'
		newline = newline[0:len(newline)-3]
		out.write(newline.strip() + '\n')
out.close()
		
