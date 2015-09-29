import gensim, time

positives = ['synonyms']
negatives = ['antonyms']
test_size = 1000

def getVector(vec):
	result = ''
	for value in vec:
		result += str(value) + ' '
	return result.strip()

posw2vmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_500_cbow.bin'
model = gensim.models.word2vec.Word2Vec.load_word2vec_format(posw2vmodel, binary=True)
model.init_sims(replace=True)

suffix = '_'
for p in positives:
	suffix += p
suffix += '_'
for n in negatives:
	suffix += n
suffix += 'nonorm.txt'

#Produce instances:
pinsts = []
ninsts = []
start = time.time()
print('Reading positives...')
for p in positives:
	f = open('../../corpora/maps/'+p+'.txt')
	for line in f:
		data = line.strip().split('\t')
		target = data[0].strip()
		try:
			targetv = model[target]
			for cand in data[1:len(data)]:
				try:
					candv = model[cand]
					res = targetv-candv
					pinsts.append(res)
				except Exception:
					pass
		except Exception:
			pass
	f.close()

print('Reading negatives...')
for n in negatives:
	f = open('../../corpora/maps/'+n+'.txt')
	for line in f:
		data = line.strip().split('\t')
		target = data[0].strip()
		try:
			targetv = model[target]
			for cand in data[1:len(data)]:
				try:
					candv = model[cand]
					res = targetv-candv
					ninsts.append(res)
				except Exception:
					pass
		except Exception:
			pass
	f.close()
end = time.time()
print('Elapsed: ' + str(end-start))

print('Saving test file...')
o = open('../../corpora/datasets/testing'+suffix, 'w')
for i in range(0, test_size):
	pinst = getVector(pinsts[i])
	ninst = getVector(ninsts[i])
	o.write(pinst+'\t1\n')
	o.write(ninst+'\t-1\n')
o.close()

print('Saving training file...')
o = open('../../corpora/datasets/training'+suffix, 'w')
for i in range(test_size, len(pinsts)):
	pinst = getVector(pinsts[i])
	o.write(pinst+'\t1\n')

for i in range(test_size, len(ninsts)):
	ninst = getVector(ninsts[i])
	o.write(ninst+'\t-1\n')
o.close()
