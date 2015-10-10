from lexenstein.generators import *
from lexenstein.morphadorner import *
from lexenstein.spelling import *
import sys, os

size = sys.argv[1]

victor_corpus = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt'

w2v = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_generalized_'+size+'_cbow_retrofitted.bin'

folderExists = os.path.isdir('../../substitutions/paetzold_retrofitted'+size)

if not folderExists:
	os.system('mkdir ../../substitutions/paetzold_retrofitted'+size)

	m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

	nc = NorvigCorrector('/export/data/ghpaetzold/LEXenstein/corpora/norvig_model_wmt.bin', format='bin')

	pos_model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/wsj-0-18-left3words-distsim.tagger'
	stanford_tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
	
	kg = PaetzoldGenerator(w2v, nc, pos_model, stanford_tagger, '/usr/bin/java')
	subs = kg.getSubstitutions(victor_corpus, 10)
	
	out = open('../../substitutions/paetzold_retrofitted'+size+'/substitutions.txt', 'w')
	for k in subs.keys():
		newline = k + '\t'
		if len(subs[k])>0:
			for c in subs[k]:
				newline += c + '|||'
			newline = newline[0:len(newline)-3]
			out.write(newline.strip() + '\n')
	out.close()
		
else:
        print('Folder already exists!')
