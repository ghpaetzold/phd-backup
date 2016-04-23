from keras.optimizers import *
from keras.models import *
from keras.layers.core import *
from keras.models import Sequential, slice_X
from keras.layers.core import Activation, TimeDistributedDense, RepeatVector
from keras.layers import recurrent
from keras.preprocessing.text import *
import sys
import numpy as np
from nltk.util import ngrams
import gensim

out_file = sys.argv[1].strip()
model_file = sys.argv[2].strip()
train_file = sys.argv[3].strip()

def getFeatures():
        Xtr = []
        f = open('../../classifiers/ml/features_final_testing.txt')
        for line in f:
                Xtr.append([float(v) for v in line.strip().split(' ')])
        f.close()
        return np.array(Xtr)

print('Calculating...')
Xte = getFeatures()

model = model_from_json(open(model_file+'.json').read())
model.load_weights(model_file+'.h5')
print('Loaded!')

print('Predicting...')
labels_raw = model.predict_classes(Xte, batch_size=Xte.shape[0])
labels = []
for label in labels_raw:
        labels.append(label)

f = open(train_file)
o = open(out_file, 'w')
for i in range(0, len(labels)):
	label = labels[i]
	data = f.readline().strip().split('\t')
	s1 = data[0]
	s2 = data[1]
#	if s1==s2:
#		if 'G_' in train_file or 'M_' in train_file or 'O_' in train_file:
#			o.write('2\t2\n')
#		else:
#			o.write('2\t2\n')
#	else:
        o.write(str(label) + '\t' + str(label) + '\n')
o.close()
f.close()
