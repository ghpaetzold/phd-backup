from lexenstein.morphadorner import *
from lexenstein.identifiers import *
from lexenstein.features import *
import sys

m = MorphAdornerToolkit('/export/data/ghpaetzold/LEXenstein/morph/')

fe = FeatureEstimator(norm=False)
fe.addLengthFeature('Complexity')
fe.addSyllableFeature(m, 'Complexity')
fe.addNGramFrequencyFeature('/export/data/ghpaetzold/LEXenstein/corpora/ngram_dict_wmt_simplewiki_1billion_webbase.bin', 0, 0, 'Simplicity')
fe.addSenseCountFeature('Simplicity')
fe.addSynonymCountFeature('Simplicity')
fe.addHypernymCountFeature('Simplicity')
fe.addHyponymCountFeature('Simplicity')
fe.addMinDepthFeature('Complexity')
fe.addMaxDepthFeature('Complexity')

labels = ['length', 'syllables', 'frequency', 'senses', 'synonyms', 'hypernyms', 'hyponyms', 'mindepth', 'maxdepth']

map = {}
for label in labels:
	map[label] = {'0':{}, '1':{}}

print('Calculating...')
features = fe.calculateFeatures('../../corpora/cwi_paetzold_training.txt', format='cwictor')

complex = set([])
f = open('../../corpora/cwi_paetzold_training.txt')
for line in f:
	data = line.strip().split('\t')
	word = data[1].strip().lower()
	label = data[3].strip()
	if label=='1':
		complex.add(word)
f.close()

f = open('../../corpora/cwi_paetzold_training.txt')
c = -1
for line in f:
	c += 1
	data = line.strip().split('\t')
	word = data[1].strip().lower()
	label = '0'
	if word in complex:
		label = '1'
	values = features[c]
	for i in range(0, len(labels)):
		value = values[i]
		feature = labels[i]
		featmap = map[feature][label]
		if value not in featmap:
			featmap[value] = 0
		featmap[value] += 1
f.close()

for feature in map:
	o = open('./data/'+feature+'.txt', 'w')
	for value in map[feature]:
		newline = str(value)+'\t'
		for size in map[feature][value]:
			newline += str(size)+':'+str(map[feature][value][size])+'\t'
		o.write(newline.strip() + '\n')
	o.close()
		
