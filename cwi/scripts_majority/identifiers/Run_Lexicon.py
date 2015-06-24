from lexenstein.identifiers import *
from lexenstein.features import *
from lexenstein.morphadorner import *
import sys

test_corpus = sys.argv[1].strip()
train_corpus = sys.argv[2].strip()
lexicon = sys.argv[3].strip()
type = sys.argv[4].strip()
output_path = sys.argv[5].strip()

ti = LexiconIdentifier(lexicon, type)
labels = ti.identifyComplexWords(test_corpus)

o = open(output_path, 'w')
for label in labels:
	o.write(str(label) + '\n')
o.close()
