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

def getFeatures():
        Xtr = []
        f = open('../../classifiers/ml/features_testing.txt')
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

o = open(out_file, 'w')
for label in labels:
        o.write(str(label) + '\t' + str(label) + '\n')
o.close()
