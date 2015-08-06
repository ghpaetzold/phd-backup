from nltk.tag.stanford import StanfordPOSTagger
import os, sys

input = sys.argv[1]
output = sys.argv[2]

model = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/models/english-bidirectional-distsim.tagger'
tagger = '/export/data/ghpaetzold/benchmarking/lexmturk/scripts/evaluators/stanford-postagger-full-2015-04-20/stanford-postagger.jar'
java = '/usr/bin/java'

os.environ['JAVAHOME'] = java
tagger = StanfordPOSTagger(model, tagger)

f = open(input)
sentences = []
for line in f:
	sentences.append(line.strip().split('\t')[0].strip().split(' '))
f.close()

print('Tagging...')
tagged_sents = tagger.tag_sents(sentences)
print('Tagged!')

o = open(output, 'w')
for line in tagged_sents:
	l = ''
	for token in line:
		l += token[0].strip() + '|||' + token[1].strip() + ' '
	o.write(l.strip() + '\n')
o.close()
