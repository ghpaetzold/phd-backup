from nltk.corpus import wordnet as wn

def addToDict(stem, word, map):
	if word not in map:
		if stem not in map:
			map[stem] = set([word])
		else:
			map[stem].add(word)
	else:
		map[word].add(stem)

def getSynonyms(stem, lemmas):
	synonyms = set([])
	for lemma in lemmas:
		name = lemma.name()
		if '_' not in name and name!=stem:
			synonyms.add(name.lower())
	return synonyms

def getHypernyms(stem, syn):
	hypernyms = set([])
	hypers = syn.hypernyms()
	for hyper in hypers:
		lemmas = hyper.lemmas()
		for lemma in lemmas:
			name = lemma.name()
			if '_' not in name and name!=stem:
				hypernyms.add(name.lower())
	return hypernyms

def getHyponyms(stem, syn):
        hyponyms = set([])
        hypos = syn.hyponyms()
        for hypo in hypos:
                lemmas = hypo.lemmas()
                for lemma in lemmas:
                        name = lemma.name()
                        if '_' not in name and name!=stem:
                                hyponyms.add(name.lower())
        return hyponyms

def getAntonyms(lemmas):
	antlemmas = set([])
	for lemma in lemmas:
		ants = lemma.antonyms()
		antsyns = set([])
		for ant in ants:
			antsyns.add(ant.synset())
		for antsyn in antsyns:
			antlemmas.update(antsyn.lemmas())
	antonyms = set([])
	for l in antlemmas:
		name = l.name()
		if '_' not in name:
			antonyms.add(name.lower())
	return antonyms

vocab = set([w.strip() for w in open('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/wiki.vocab.txt')])

synonyms = {}
hypernyms = {}
hyponyms = {}
antonyms = {}
c = 0
for word in vocab:
	c += 1
	print(str(c))
	stem = wn.morphy(word)
	if stem:
		syns = wn.synsets(stem)
		for syn in syns:
			lemmas = syn.lemmas()
			syns = getSynonyms(stem, lemmas)
			hypers = getHypernyms(stem, syn)
			hypos = getHyponyms(stem, syn)
			ants = getAntonyms(lemmas)
			if len(syns)>0 and len(ants)>0:
				for synonym in syns:
					addToDict(stem, synonym, synonyms)
				for antonym in ants:
					addToDict(stem, antonym, antonyms)
				for hypernym in hypers:
					addToDict(stem, hypernym, hypernyms)
				for hyponym in hypos:
					addToDict(stem, hyponym, hyponyms)

f = open('synonyms.txt', 'w')
for word in synonyms:
	newline = word + '\t'
	for syn in synonyms[word]:
		newline += syn + '\t'
	f.write(newline.strip() + '\n')
f.close()

f = open('antonyms.txt', 'w')
for word in antonyms:
        newline = word + '\t'
        for ant in antonyms[word]:
                newline += ant + '\t'
        f.write(newline.strip() + '\n')
f.close()

f = open('hypernyms.txt', 'w')
for word in hypernyms:
        newline = word + '\t'
        for ant in hypernyms[word]:
                newline += ant + '\t'
        f.write(newline.strip() + '\n')
f.close()

f = open('hyponyms.txt', 'w')
for word in hyponyms:
        newline = word + '\t'
        for ant in hyponyms[word]:
                newline += ant + '\t'
        f.write(newline.strip() + '\n')
f.close()
