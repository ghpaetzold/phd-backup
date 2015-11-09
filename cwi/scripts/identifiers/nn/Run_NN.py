from keras.optimizers import *
from keras.models import *
from keras.layers.core import *
from lexenstein.morphadorner import *
from lexenstein.identifiers import *
from lexenstein.features import *
import sys
import numpy as np

train_victor_corpus = sys.argv[1]
hidden_size = int(sys.argv[2].strip())
final_loss = sys.argv[3].strip()
final_optimizer = sys.argv[4].strip()
test_victor_corpus = sys.argv[5].strip()
out_file = sys.argv[6].strip()

def getLabels(corpus):
	result = []
	f = open(corpus)
	for line in f:
		data = line.strip().split('\t')
		label = float(data[3].strip())
		result.append(label)
	f.close()
	return np.array(result)

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

fe = FeatureEstimator(norm=False)
fe.addLexiconFeature('../../../../semeval/corpora/basic/basic_words.txt', 'Simplicity')
fe.addLexiconFeature('../../../../semeval/corpora/vocabularies/wikisimple.vocab.txt', 'Simplicity')
fe.addLengthFeature('Complexity')
fe.addSyllableFeature(m, 'Complexity')
fe.addCollocationalFeature('../../../../../benchmarking/semeval/corpora/lm/simplewiki/simplewiki.5gram.bin.txt', 2, 2, 'Complexity')
fe.addSentenceProbabilityFeature('../../../../../benchmarking/semeval/corpora/lm/simplewiki/simplewiki.5gram.bin.txt', 'Complexity')
fe.addCollocationalFeature('../../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 2, 2, 'Complexity')
fe.addSentenceProbabilityFeature('../../../../lexmturk/corpora/subtleximdb.5gram.bin.unk.txt', 'Complexity')
fe.addSenseCountFeature('Simplicity')
fe.addSynonymCountFeature('Simplicity')
fe.addHypernymCountFeature('Simplicity')
fe.addHyponymCountFeature('Simplicity')
fe.addMinDepthFeature('Complexity')
fe.addMaxDepthFeature('Complexity')
#fe.addWordVectorValues('/export/data/ghpaetzold/LEXenstein/corpora/word_vectors_all.bin', 300, 'Complexity')

Xtr = np.array(fe.calculateFeatures(train_victor_corpus, format='cwictor'))
Ytr = getLabels(train_victor_corpus)
Xte = np.array(fe.calculateFeatures(test_victor_corpus, format='cwictor'))

model = Sequential()
model.add(Dense(output_dim=hidden_size, input_dim=Xtr.shape[1], init="glorot_uniform"))
model.add(Activation("tanh"))
model.add(Dense(output_dim=1, init="glorot_uniform"))
model.add(Activation("sigmoid"))
model.compile(loss=final_loss, optimizer=final_optimizer)

print('Training...')
model.fit(Xtr, Ytr, nb_epoch=100, batch_size=Xtr.shape[0], verbose=0)

print('Predicting...')
labels_raw = model.predict_classes(Xte, batch_size=Xte.shape[0])
labels = []
for label in labels_raw:
	if label>0:
		labels.append(1)
	else:
		labels.append(0)

o = open(out_file, 'w')
for label in labels:
	o.write(str(label) + '\n')
o.close()
