from lexenstein.generators import *
from lexenstein.morphadorner import *
from lexenstein.spelling import *
import sys

victor_corpus = sys.argv[1]

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

nc = NorvigCorrector('/export/data/ghpaetzold/LEXenstein/corpora/norvig_model_wmt.bin', format='bin')

pos_model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
stanford_tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'

kg = WordnetGenerator(m, nc, pos_model, stanford_tagger, '/usr/bin/java')
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
