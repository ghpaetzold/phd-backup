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

#Get parameters:
size = sys.argv[1]
senseaware = sys.argv[2]
if senseaware=='0':
        senseaware = False
elif senseaware=='1':
        senseaware = True
else:
        print('senseaware parameter not recognized!')

#Get text model:
textmodel = '../../corpora/wordvectors/word_vectors_all_'
if senseaware:
        textmodel += 'generalized_'
textmodel += size + '_cbow.txt'

#Get retrofitted file:
retrofitted = '../../corpora/wordvectors/retrofitted_wordnet'
if senseaware:
	retrofitted += 'parsed'
else:
	retrofitted += 'orig'
retrofitted += size+'_vectors.txt'

#Get temp file:
temp = '../../corpora/temp/'
if senseaware:
        temp += 'parsed'
else:
        temp += 'orig'
temp += size+'_cbow_temp.txt'

#Get output file:
output = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_'
if senseaware:
        output += 'generalized_'
output += size + '_cbow_retrofitted.bin'

#textmodel = sys.argv[1]
#retrofitted = sys.argv[2]
#temp = sys.argv[3]
#output = sys.argv[4]

print('Reading retrofitted entries...')
retromap = {}
f = open(retrofitted)
for line in f:
	data = line.strip().split(' ')
	word = data[0].strip()
	retromap[word] = line.strip()
f.close()

print('Creating temporary text model...')
f = open(textmodel)
t = open(temp, 'w')
t.write(f.readline().strip() + '\n')
for line in f:
	word = line.split(' ')[0].strip()
	if word in retromap:
		t.write(retromap[word] + '\n')
	else:
		t.write(line)
f.close()
t.close()

print('Loading temporary text model...')
m = gensim.models.word2vec.Word2Vec.load_word2vec_format(temp, binary=False)

print('Writing vectors...')
m.save_word2vec_format(output, fvocab=None, binary=True)
