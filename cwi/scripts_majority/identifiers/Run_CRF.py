from lexenstein.morphadorner import *
from lexenstein.identifiers import *
from lexenstein.features import *
import sys
from pystruct.learners import *
from pystruct.models import *
import numpy as np


train_victor_corpus = sys.argv[1]
test_victor_corpus = sys.argv[2].strip()
learner = eval(sys.argv[3].strip())
model = eval(sys.argv[4].strip())
out_file = sys.argv[5].strip()

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

fe = FeatureEstimator(norm=False)
fe.addLexiconFeature('../../../semeval/corpora/basic/basic_words.txt', 'Simplicity')
fe.addLexiconFeature('../../../semeval/corpora/vocabularies/wikisimple.vocab.txt', 'Simplicity')
fe.addLengthFeature('Complexity')
fe.addSyllableFeature(m, 'Complexity')
fe.addCollocationalFeature('../../../../benchmarking/semeval/corpora/lm/simplewiki/simplewiki.5gram.bin.txt', 2, 2, 'Complexity')
fe.addSentenceProbabilityFeature('../../../../benchmarking/semeval/corpora/lm/simplewiki/simplewiki.5gram.bin.txt', 'Complexity')
fe.addCollocationalFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 2, 2, 'Complexity')
fe.addSentenceProbabilityFeature('../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 'Complexity')
fe.addSenseCountFeature('Simplicity')
fe.addSynonymCountFeature('Simplicity')
fe.addHypernymCountFeature('Simplicity')
fe.addHyponymCountFeature('Simplicity')
fe.addMinDepthFeature('Complexity')
fe.addMaxDepthFeature('Complexity')
#fe.addWordVectorValues('/export/data/ghpaetzold/LEXenstein/corpora/word_vectors_all.bin', 300, 'Complexity')

Xtr = np.array(fe.calculateFeatures(train_victor_corpus, format='cwictor'))
Ytr = np.array([int(x.strip().split('\t')[3].strip()) for x in open(train_victor_corpus)])
Xte = np.array(fe.calculateFeatures(test_victor_corpus, format='cwictor'))

print('XTR: ' + str(Xtr.shape))
print('XTE: ' + str(Xte.shape))
print('YTR: ' + str(Ytr.shape))

clf = learner(model())
clf.fit(Xtr, Ytr)
labels = clf.predict(Xte)

o = open(out_file, 'w')
for label in labels:
	o.write(str(label) + '\n')
o.close()
