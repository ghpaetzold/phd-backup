import gensim, sys

def toString(vector):
	result = ''
	for value in vector:
		result += str(value) + ' '
	return result.strip()

def writeVectors(lexicon, model, path):
	words = set([])
	f = open(lexicon)
	for line in f:
		data = line.strip().split(' ')
		words.update(data)
	f.close()
	
	o = open(path, 'w')
	for word in words:
		try:
			vec = model[word]
			o.write(word + ' ' + toString(vec) + '\n')
		except Exception:
			pass
	o.close()	

size = sys.argv[1]
senseaware = sys.argv[2]
if senseaware=='0':
	senseaware = False
elif senseaware=='1':
	senseaware = True
else:
	print('senseaware parameter not recognized!')
arch = sys.argv[3]

path = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_'
if senseaware:
	path += 'generalized_'
path += size + '_'+arch+'.bin'

#Load binary model:
m = gensim.models.word2vec.Word2Vec.load_word2vec_format(path, binary=True)

#Create lexicon path:
wnlexicon = '../../lexicons/wordnet-synonyms.txt'
if senseaware:
	wnlexicon = '../../lexicons/parsed-wordnet-synonyms.txt'

#Create common vectors path:
vectors = '../../corpora/wordvectors/wordnet'
if senseaware:
	vectors += 'parsed'
else:
	vectors += 'orig'
vectors += size+'_vectors_'+arch+'.txt'

#Create output path:
outpath = '../../corpora/wordvectors/word_vectors_all_'
if senseaware:
	outpath += 'generalized_'
outpath += size + '_'+arch+'.txt'

#Write vectors:
print('Writing vectors...')
writeVectors(wnlexicon, m, vectors)
m.save_word2vec_format(outpath, fvocab=None, binary=False)

