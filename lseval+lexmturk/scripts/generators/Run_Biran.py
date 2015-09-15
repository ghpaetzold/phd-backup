from lexenstein.generators import *
from lexenstein.morphadorner import *
from lexenstein.spelling import *
import sys, os

victor_corpus = sys.argv[1].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

nc = NorvigCorrector('/export/data/ghpaetzold/LEXenstein/corpora/norvig_model_wmt.bin', format='bin')

pos_model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
stanford_tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
complexvocab = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/wiki.vocab.txt'
simplevocab = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/wikisimple.vocab.txt'
complexlm = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/wiki.5gram.bin.txt'
simplelm = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/simplewiki.5.bin.txt'

kg = BiranGenerator(m, complexvocab, simplevocab, complexlm, simplelm, nc, pos_model, stanford_tagger, '/usr/bin/java')
subs = kg.getSubstitutions(victor_corpus)

os.system('mkdir ../../substitutions/biran/')
out = open('../../substitutions/biran/substitutions.txt', 'w')
for k in subs.keys():
	newline = k + '\t'
	if len(subs[k])>0:
		for c in subs[k]:
			newline += c + '|||'
		newline = newline[0:len(newline)-3]
		out.write(newline.strip() + '\n')
out.close()
		
