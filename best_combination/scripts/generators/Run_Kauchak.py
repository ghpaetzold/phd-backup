from lexenstein.generators import *
from lexenstein.morphadorner import *
from lexenstein.spelling import *
import sys

victor_corpus = sys.argv[1].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

nc = NorvigCorrector('/export/data/ghpaetzold/LEXenstein/corpora/wiki_simplewiki.txt')

kg = KauchakGenerator(m, '../../corpora/all.fastalign.pos.txt', '../../corpora/all.fastalign.allalignments.txt', '../../corpora/stop_words.txt', nc)
subs = kg.getSubstitutions(victor_corpus)

out = open('../../substitutions/kauchak/substitutions.txt', 'w')
for k in sorted(subs.keys()):
	newline = k + '\t'
	if len(subs[k])>0:
		for c in subs[k]:
			newline += c + '|||'
		newline = newline[0:len(newline)-3]
		out.write(newline.strip() + '\n')
out.close()
		
