import urllib2 as urllib
from nltk.corpus import wordnet as wn

def cleanLemma(lem):
	result = ''
	aux = lem.strip().split('_')
	for word in aux:
		result += word + ' '
	return result.strip()

lex = open('../../../corpora/lexmturk/lexmturk.txt')
out = open('../../../corpora/substitutions/wordnet/substitutions.txt', 'w')
for line in lex:
	data = line.strip().split('\t')
	target = data[1].strip()
	syns = wn.synsets(target)
	newline = target + '\t'
	cands = set([])
	for syn in syns:
		for lem in syn.lemmas():
			candidate = cleanLemma(lem.name())
			if candidate!=target and candidate not in cands:
				cands.add(candidate)
				newline += candidate + '|||'
	if newline.endswith('|||'):
		newline = newline[0:len(newline)-3]
	out.write(newline.strip() + '\n')
lex.close()
out.close()
