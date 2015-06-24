from lexenstein.morphadorner import MorphAdornerToolkit
from lexenstein.generators import *
from lexenstein.evaluators import *
from lexenstein.selectors import *
from lexenstein.features import *
from lexenstein.rankers import *
from lexenstein.identifiers import *
import sys

test_corpus = '../../corpora/cwi_paetzold_testing_majority.txt'
out_file = '../../labels_majority/none/labels_None.txt'

sai = SimplifyNoneIdentifier()
labels = sai.identifyComplexWords(test_corpus)

o = open(out_file, 'w')
for label in labels:
	o.write(str(label) + '\n')
o.close()
