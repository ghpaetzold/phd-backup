import os
from nltk.tag.stanford import POSTagger
import nltk

def getClass(tag):
	result = None
	if tag.startswith('N'):
		result = 'N'
	elif tag.startswith('V'):
		result = 'V'
	elif tag.startswith('RB'):
		result = 'A'
	elif tag.startswith('J'):
		result = 'J'
	else:
		result = 'O'
	return result

os.environ['JAVAHOME'] = '/usr/bin/java'
pos_model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/wsj-0-18-left3words-distsim.tagger'
stanford_tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
tagger = POSTagger(pos_model, stanford_tagger)

f = open('../../corpora/cwi_paetzold_training.txt')
sents = set([])
for line in f:
	data = line.strip().split('\t')
	sent = data[0].strip()
	sents.add(sent)
f.close()
f = open('../../corpora/cwi_paetzold_testing.txt')
for line in f:
        data = line.strip().split('\t')
        sent = data[0].strip()
        sents.add(sent)
f.close()

sents = list(sents)
tagged_sents = []
for i in range(0, len(sents)):
	sent = sents[i].split(' ')
	tokens = nltk.pos_tag(sent)
	tagged_sents.append(tokens)

f = open('../../corpora/tagged_sents.txt', 'w')
for i in range(0, len(sents)):
	if len(sents[i].split(' '))!=len(tagged_sents[i]):
		print('BIG PROBLEM')
	newline = sents[i].strip() + '\t'
	for token in tagged_sents[i]:
		newline += token[1].strip() + ' '
	f.write(newline.strip() + '\n')
f.close()

tagged_sents = {}
f = open('../../corpora/tagged_sents.txt')
for line in f:
	data = line.strip().split('\t')
	sent = data[0].strip()
	tags = data[1].strip()
	tagged_sents[sent] = tags.split(' ')
f.close()


sets = ['training', 'testing']
for s in sets:
	f1 = open('../../corpora/cwi_paetzold_'+s+'.txt')

	classes = ['N', 'V', 'J', 'A', 'O']
	writers = {}
	for c in classes:
		writers[c] = open('../../corpora/cwi_paetzold_'+s+'_'+c+'.txt', 'w')
	
	for instance in f1:
		data = instance.split('\t')
		sent = data[0].strip()
		head = int(data[2].strip())
		tokens = tagged_sents[sent]
		tag = getClass(tokens[head])
		writers[tag].write(instance)

	for w in writers.keys():
		writers[w].close()
		
