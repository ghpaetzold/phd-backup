import sys, gensim, os

def getSimilarity(m, type, word1, word2):
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
		maxsim = -99999999
		for tag1 in tags:
			for tag2 in tags:
				try:
					similarity = m.similarity(word1+'|||'+tag1, word2+'|||'+tag2)
					if similarity>maxsim:
						maxsim = similarity
				except Exception:
					try:
						similarity = m.similarity(word1.lower()+'|||'+tag1, word2.lower()+'|||'+tag2)
						if similarity>maxsim:
							maxsim = similarity
					except Exception:
						pass
		similarity = maxsim
		if similarity==-99999999:
			similarity = 0.0
	return similarity


#Get dataset, type of model and vector size:
dataset = sys.argv[1]
type = sys.argv[2]
size = sys.argv[3]
arch = sys.argv[4]

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
dpath = '../../corpora/wordsimilarity/'+dataset+'.txt'
f = open(dpath)

#Create folders:
os.system('mkdir ../../similarities/' + dataset)
os.system('mkdir ../../similarities/' + dataset +'/'+ type)
os.system('mkdir ../../similarities/' + dataset +'/'+ type + '/' + arch)

#Write distances:
opath = '../../similarities/' + dataset +'/'+ type + '/' + arch + '/' + size
o = open(opath, 'w')
for line in f:
	data = line.strip().split('\t')
	word1 = data[0].strip()
	word2 = data[1].strip()
	similarity = getSimilarity(m, type, word1, word2)
	o.write(str(similarity) + '\n')
f.close()
o.close()
	
