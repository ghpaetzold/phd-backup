from keras.optimizers import *
from keras.models import *
from keras.layers.core import *
import sys
import numpy as np

train_victor_corpus = sys.argv[1]
hidden_size = int(sys.argv[2].strip())
lr = float(sys.argv[3].strip())
momentum = float(sys.argv[4].strip())
decay = float(sys.argv[5].strip())
nesterov = sys.argv[6].strip()
if nesterov=='1':
	nesterov = True
elif nesterov=='0':
	nesterov = False
else:
	print('Problem!')
layers = int(sys.argv[7].strip())
test_victor_corpus = sys.argv[8].strip()
out_file = sys.argv[9].strip()
model_file = sys.argv[10].strip()

def getFeatures():
        Xtr = []
        Xte = []
        f = open('../ml/features_training.txt')
        for line in f:
                Xtr.append([float(v) for v in line.strip().split(' ')])
        f.close()
        f = open('../ml/features_testing.txt')
        for line in f:
                Xte.append([float(v) for v in line.strip().split(' ')])
        f.close()
        return np.array(Xtr), np.array(Xte)

def getLabelVec(label):
        answer = np.zeros(3)
        answer[int(label)]=1.0
        return answer

def getLabels(corpus):
        Y = []
        f = open(corpus)
        for line in f:
                data = line.strip().split('\t')
                label = int(data[2].strip())
                Y.append(getLabelVec(label))
        f.close()
        return np.array(Y)


print('Calculating...')
Xtr, Xte = getFeatures()
Ytr = getLabels(train_victor_corpus)
print('X: ' + str(Xtr.shape))
print('Y: ' + str(Ytr.shape))

model = Sequential()
model.add(Dense(output_dim=hidden_size, input_dim=Xtr.shape[1], init="glorot_uniform"))
model.add(Activation("tanh"))
model.add(Dropout(0.25))
for i in range(0, layers):
	model.add(Dense(output_dim=hidden_size, init="glorot_uniform"))
	model.add(Activation("tanh"))
model.add(Dense(output_dim=3, init="glorot_uniform"))
model.add(Activation("sigmoid"))
sgd = SGD(lr=lr, decay=decay, momentum=momentum, nesterov=nesterov)
model.compile(loss='categorical_crossentropy', optimizer=sgd)

print('Training...')
model.fit(Xtr, Ytr, nb_epoch=10000, batch_size=Xtr.shape[0])
#model.fit(Xtr, Ytr, nb_epoch=5, batch_size=Xtr.shape[0])

print('Predicting...')
labels_raw = model.predict_classes(Xte, batch_size=Xte.shape[0])
labels = []
for label in labels_raw:
	labels.append(label)
#	if label>0:
#		labels.append(1)
#	else:
#		labels.append(0)

o = open(out_file, 'w')
for label in labels:
	o.write(str(label) + '\t' + str(label) + '\n')
o.close()
