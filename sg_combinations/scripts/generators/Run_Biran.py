from lexenstein.generators import *
from lexenstein.morphadorner import *
from lexenstein.spelling import *
import sys

victor_corpus = sys.argv[1].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

nc = NorvigCorrector('/export/data/ghpaetzold/LEXenstein/corpora/wiki_simplewiki.txt')

pos_model = '../evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
stanford_tagger = '../evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
kg = BiranGenerator(m, '../../corpora/wiki.vocab.txt', '../../corpora/wikisimple.vocab.txt', '../../corpora/wiki.5gram.bin.txt', '../../corpora/simplewiki.5.bin.txt', nc, '../evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger', '../evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar')
subs = kg.getSubstitutions(victor_corpus)

out = open('../../substitutions/biran/substitutions.txt', 'w')
for k in subs.keys():
	newline = k + '\t'
	if len(subs[k])>0:
		for c in subs[k]:
			newline += c + '|||'
		newline = newline[0:len(newline)-3]
		out.write(newline.strip() + '\n')
out.close()
		
