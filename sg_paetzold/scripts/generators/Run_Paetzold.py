from lexenstein.generators import *
from lexenstein.morphadorner import *
from lexenstein.spelling import *
import sys
import os

victor_corpus = sys.argv[1].strip()
w2vmodel = sys.argv[2].strip()
output = sys.argv[3].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

nc = NorvigCorrector('/export/data/ghpaetzold/LEXenstein/corpora/norvig_model_wmt.bin', format='bin')
	
pos_model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/wsj-0-18-left3words-distsim.tagger'
stanford_tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
	
kg = PaetzoldGenerator(w2vmodel, nc, pos_model, stanford_tagger, '/usr/bin/java')
	
amounts = ['5', '10', '15', '20', '25']
for amount in amounts:
	if not os.path.isfile(output+'_'+amount):
		subs = kg.getSubstitutions(victor_corpus, int(amount))
	
		out = open(output+'_'+amount, 'w')
		for k in subs.keys():
			newline = k + '\t'
			if len(subs[k])>0:
				for c in subs[k]:
					newline += c + '|||'
				newline = newline[0:len(newline)-3]
				out.write(newline.strip() + '\n')
		out.close()
		
