from lexenstein.generators import *
from lexenstein.morphadorner import *
from lexenstein.spelling import *
import sys
import os

victor_corpus = sys.argv[1].strip()
w2vmodel = sys.argv[2].strip()
amount = int(sys.argv[3].strip())
output = sys.argv[4].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

nc = NorvigCorrector('/export/data/ghpaetzold/LEXenstein/corpora/norvig_model_wmt.bin', format='bin')

kg = PaetzoldGenerator(w2vmodel, nc)
subs = kg.getSubstitutions(victor_corpus, amount)

out = open(output, 'w')
for k in subs.keys():
	newline = k + '\t'
	if len(subs[k])>0:
		for c in subs[k]:
			newline += c + '|||'
		newline = newline[0:len(newline)-3]
		out.write(newline.strip() + '\n')
out.close()
		
