import urllib.request as urllib
import xml.etree.ElementTree as ET
import nltk

def getPOS(target, sent):
	result = ''
	data = nltk.pos_tag(sent.lower().strip().split(' '))
	for token in data:
		if token[0].strip()==target:
			result = token[1].strip()
	return result

basicf = open('../../../corpora/basic/basic_words.txt')
basic_words = set([])
for line in basicf:
	basic_words.add(line.strip())
basicf.close()

lex = open('../../../corpora/lexmturk/lexmturk.txt')
out = open('../../../corpora/substitutions/yamamoto/substitutions.txt', 'w', encoding='utf-8')
c = -1
for line in lex:
	c += 1
	print(str(c))

	data = line.strip().split('\t')
	target = data[1].strip()
	targetp = getPOS(target, data[0].strip())

	url = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/' + target + '?key=65f439df-0149-4294-bd7f-2d317b3bd00e'
	conn = urllib.urlopen(url)
	root = ET.fromstring(conn.read())

	newline = target + '\t'
	candidates = set([])

	for definition in root.iter('dt'):
		if definition.text!=None:
			text = definition.text.strip()
			text = text[1:len(text)]
			tokens = nltk.word_tokenize(text)
			postags = nltk.pos_tag(tokens)
			for p in postags:
				postag = p[1].strip()
				cand = p[0].strip()
				if postag==targetp:
					candidates.add(cand)
	for candidate in candidates:
		newline += candidate + '|||'
	if newline.endswith('|||'):
		newline = newline[0:len(newline)-3]
	out.write(newline.strip() + '\n')
lex.close()
out.close()
