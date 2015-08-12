from lexenstein.generators import *
from lexenstein.morphadorner import *
from lexenstein.spelling import *
import sys

victor_corpus = sys.argv[1].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

nc = NorvigCorrector('/export/data/ghpaetzold/LEXenstein/corpora/norvig_model_wmt.bin', format='bin')

pos_model = '../evaluators/stanford-postagger-full-2015-04-20/models/wsj-0-18-left3words-distsim.tagger'
stanford_tagger = '../evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
#w2vpm = '/export/data/ghpaetzold/word2vecvectors/corpora/word_vectors_all_generalized_500.bin'
w2vpm = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_generalized_500_cbow.bin'

kg = PaetzoldGenerator(w2vpm, nc, pos_model, stanford_tagger, '/usr/bin/java')
subs = kg.getSubstitutions(victor_corpus, 10)

out = open('../../substitutions/paetzold/substitutions.txt', 'w')
for k in subs.keys():
	newline = k + '\t'
	if len(subs[k])>0:
		for c in subs[k]:
			newline += c + '|||'
		newline = newline[0:len(newline)-3]
		out.write(newline.strip() + '\n')
out.close()
		
