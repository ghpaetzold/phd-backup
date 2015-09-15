from nltk.corpus import wordnet as wn

def transformPOS(pos):
	if pos=='r':
		return 'a'
	elif pos=='a' or pos=='s':
		return 'j'
	elif pos=='n' or pos=='v':
		return pos
	else:
		print('Problem: ' + pos)
		return pos

targets = set([])
f = open('../lexicons/wordnet-synonyms.txt')
for line in f:
	data = line.strip().split(' ')
	targets.update(data)

f.close()

o = open('../lexicons/parsed-wordnet-synonyms.txt', 'w')
for word in targets:
	wsyns = wn.synsets(word)

	synonym_map = {}
	for syn in wsyns:
		pos = transformPOS(syn.pos()).upper()
		key = word+'|||'+pos
		synonyms = set([l.name()+'|||'+pos for l in syn.lemmas()])
		if key in synonyms:
			synonyms.remove(key)
		if len(synonyms)>0:
			if key in synonym_map:
				synonym_map[key].update(synonyms)
			else:
				synonym_map[key] = synonyms

	for entry in synonym_map:
		newline = entry + ' '
		for synonym in synonym_map[entry]:
			newline += synonym + ' '
		o.write(newline.strip() + '\n')
o.close()
