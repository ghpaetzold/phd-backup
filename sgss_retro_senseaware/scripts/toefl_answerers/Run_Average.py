import sys, gensim, os

def getAnswer(m, type, word1, cands):
	maxcand = None
	maxsim = -999999
	for word2 in cands:
		similarity = 0.0
		if 'S' not in type:
			try:
				similarity = m.similarity(word1, word2)
			except Exception:
				try:
					similarity = m.similarity(word1.lower(), word2.lower())
				except Exception:
					pass
		else:
			tags = ['N', 'V', 'J', 'A', 'P']
			counter = 0
			avgsim = 0.0
			for tag1 in tags:
				for tag2 in tags:
					try:
						similarity = m.similarity(word1+'|||'+tag1, word2+'|||'+tag2)
						avgsim += similarity
						counter += 1
					except Exception:
						try:
							similarity = m.similarity(word1.lower()+'|||'+tag1, word2.lower()+'|||'+tag2)
							avgsim += similarity
							counter += 1
						except Exception:
							pass
			if counter>0:
				similarity = avgsim/float(counter)
			else:
				similarity = 0.0
		if similarity>maxsim:
			maxsim = similarity
			maxcand = word2
	if not maxcand:
		print('Null candidate')
	return maxcand


#Get dataset, type of model and vector size:
type = sys.argv[1]
size = sys.argv[2]
arch = sys.argv[3]

#Open model:
mpath = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_'
if 'S' in type:
	mpath += 'generalized_'
mpath += size + '_' + arch
if 'R' in type:
	mpath += '_retrofitted'
mpath += '.bin'
m = gensim.models.word2vec.Word2Vec.load_word2vec_format(mpath, binary=True)

#Open dataset:
dpath = '../../corpora/toefl/toefl_training.txt'
f = open(dpath)

#Create folders:
os.system('mkdir ../../toefl_answers/'+ type)
os.system('mkdir ../../toefl_answers/'+ type + '/' + arch)

#Write distances:
opath = '../../toefl_answers/'+ type + '/' + arch + '/' + size
o = open(opath, 'w')
for line in f:
	data = line.strip().split('\t')
	word = data[0].strip()
	cands = data[1:]
	answer = getAnswer(m, type, word, cands)
	o.write(str(answer) + '\n')
f.close()
o.close()
	
