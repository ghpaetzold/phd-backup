from lexenstein.generators import *
from lexenstein.morphadorner import *
from lexenstein.spelling import *
import sys

victor_corpus = sys.argv[1].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

nc = NorvigCorrector('/export/data/ghpaetzold/LEXenstein/corpora/norvig_model_wmt.bin', format='bin')

kg = MerriamGenerator(m, 'c21550b0-418e-4a52-b85c-76587b8fdc2f', nc)
subs = kg.getSubstitutions(victor_corpus)

out = open('../../substitutions/merriam/substitutions.txt', 'w')
for k in subs.keys():
	newline = k + '\t'
	if len(subs[k])>0:
		for c in subs[k]:
			newline += c + '|||'
		newline = newline[0:len(newline)-3]
		out.write(newline.strip() + '\n')
out.close()
		