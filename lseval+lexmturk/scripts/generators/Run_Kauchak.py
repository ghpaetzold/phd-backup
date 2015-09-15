from lexenstein.generators import *
from lexenstein.morphadorner import *
from lexenstein.spelling import *
import sys, os

victor_corpus = sys.argv[1].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

nc = NorvigCorrector('/export/data/ghpaetzold/LEXenstein/corpora/wiki_simplewiki.txt')

file1 = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/all.fastalign.pos.txt'
file2 = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/all.fastalign.allalignments.txt'
file3 = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/stop_words.txt'
kg = KauchakGenerator(m, file1, file2, file3, nc)
subs = kg.getSubstitutions(victor_corpus)

os.system('mkdir ../../substitutions/kauchak/')
out = open('../../substitutions/kauchak/substitutions.txt', 'w')
for k in sorted(subs.keys()):
	newline = k + '\t' + k + '|||'
	if len(subs[k])>0:
		for c in subs[k]:
			newline += c + '|||'
		newline = newline[0:len(newline)-3]
		out.write(newline.strip() + '\n')
out.close()
		
