from lexenstein.generators import *
from lexenstein.morphadorner import *
import sys

victor_corpus = sys.argv[1]

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

kg = WordnetGenerator(m)
subs = kg.getSubstitutions(victor_corpus)

out = open('../../substitutions/wordnet/substitutions.txt', 'w')
for k in subs.keys():
	newline = k + '\t'
	if len(subs[k])>0:
		for c in subs[k]:
			newline += c + '|||'
		newline = newline[0:len(newline)-3]
		out.write(newline.strip() + '\n')
out.close()
		
