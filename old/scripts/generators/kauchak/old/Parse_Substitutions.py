import os
import nltk

f = open('../../corpora/substitutions/kauchak/all.substitutions.txt')

outs = open('../../corpora/parsed/source.sents.txt', 'w')
outt = open('../../corpora/parsed/target.sents.txt', 'w')

c = 0
for line in f:
	c += 1
	print(str(c))
        data = line.strip().split('\t')
        sources = data[0].strip()
        targets = data[1].strip()
        outt.write(sources + '\n')
        outs.write(targets + '\n')
f.close()
outs.close()
outt.close()
