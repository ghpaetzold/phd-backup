import sys, gensim, os

def getSimilarity(m, type, word1, word2):
	similarity = 0.0
	word1d = word1.strip().split('|||')
	word2d = word2.strip().split('|||')
	actualWord1 = word1d[0].strip()
	actualWord2 = word2d[0].strip()
	tag1 = word1d[1].strip()
	tag2 = word2d[1].strip()
	if 'S' not in type:
		try:
			similarity = m.similarity(word1, word2)
		except Exception:
			try:
				similarity = m.similarity(actualWord1.lower(), actualWord2.lower())
			except Exception:
				pass
	else:
		try:
			similarity = m.similarity(word1, word2)
		except Exception:
			try:
				similarity = m.similarity(actualWord1+'|||'+tag1, actualWord2.lower()+'|||'+tag2)
			except Exception:
				pass
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
dpath = '../../corpora/wordsimilarity/'+dataset+'-tagged.txt'
f = open(dpath)

#Create folders:
os.system('mkdir ../../similarities/' + dataset+'-TAGGED')
os.system('mkdir ../../similarities/' + dataset+'-TAGGED' +'/'+ type)
os.system('mkdir ../../similarities/' + dataset+'-TAGGED' +'/'+ type + '/' + arch)

#Write distances:
opath = '../../similarities/' + dataset+'-TAGGED/'+ type + '/' + arch + '/' + size
o = open(opath, 'w')
for line in f:
	data = line.strip().split('\t')
	word1 = data[0].strip()
	word2 = data[1].strip()
	similarity = getSimilarity(m, type, word1, word2)
	o.write(str(similarity) + '\n')
f.close()
o.close()
	
