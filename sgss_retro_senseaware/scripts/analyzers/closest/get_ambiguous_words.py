import urllib2, re, gensim
from nltk.corpus import wordnet as wn
import numpy as np
from sklearn.decomposition import PCA

exp = re.compile('<BR>([^<]*)<BR>')

conn = urllib2.urlopen('http://www.enchantedlearning.com/wordlist/nounandverb.shtml')
html = conn.read()

ocs = [oc.strip() for oc in exp.findall(html) if len(oc.strip().split(' '))==1]
ocmap = {}
synmap = {}
for word in ocs:
	syns = wn.synsets(word)
	ants = set([])
	for syn in syns:
		for lemma in syn.lemmas():
			ants.update(lemma.antonyms())
	ocmap[word] = len(ants)
	synmap[word] = len(syns)
words = sorted(ocmap.keys(), key=ocmap.__getitem__, reverse=True)

#for word in words:
#	print(word + ': ' + str(synmap[word]) + ', ' + str(ocmap[word]))

print('Loading...')
wvmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_100_cbow.bin'
wvrmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_100_cbow_retrofitted.bin'
pwvmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_generalized_100_cbow.bin'
pwvrmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_generalized_100_cbow_retrofitted.bin'
m = gensim.models.word2vec.Word2Vec.load_word2vec_format(wvmodel, binary=True)
pm = gensim.models.word2vec.Word2Vec.load_word2vec_format(pwvmodel, binary=True)
mr = gensim.models.word2vec.Word2Vec.load_word2vec_format(wvrmodel, binary=True)
pmr = gensim.models.word2vec.Word2Vec.load_word2vec_format(pwvrmodel, binary=True)


#Select words to calculate PCA of:
simmap = {}
simmapr = {}
selected = []
all = []
X = []
i = 0
words = ['stand']
while len(selected)<1 and i<len(words):
	word = words[i]
	print(str(word))

	nvec = pm[word+'|||N']
	vvec = pm[word+'|||V']
	TEMsim = m.most_similar(word, topn=10)
	SEMsimn = pm.most_similar(word+'|||N', topn=5)
	SEMsimv = pm.most_similar(word+'|||V', topn=5)
	REMsim = mr.most_similar(word, topn=10)	
	RSEMsimn = pmr.most_similar(word+'|||N', topn=5)
	RSEMsimv = pmr.most_similar(word+'|||V', topn=5)

	#Add it to the selected list:
	selected.append(word)

	#Add them to the similarity map:
	simmap[word] = TEMsim
	simmap[word+'|||N'] = SEMsimn
	simmap[word+'|||V'] = SEMsimv
	simmapr[word] = REMsim
	simmapr[word+'|||N'] = RSEMsimn
	simmapr[word+'|||V'] = RSEMsimv

	#Add them to list of words:
	all.append(word)
	all.append(word+'|||N')
	all.append(word+'|||V')
	temp = TEMsim + SEMsimn + SEMsimv
	for simw in temp:
		all.append(simw[0].strip())
	all.append(word)
        all.append(word+'|||N')
        all.append(word+'|||V')
	temp = REMsim + RSEMsimn + RSEMsimv
	for simw in temp:
		all.append(simw[0].strip())

	#Add them to X matrix:
	X.append(m[word])
	X.append(nvec)
	X.append(vvec)
	for simw in TEMsim:
		X.append(m[simw[0]])
	for simw in SEMsimn:
		X.append(pm[simw[0]])
	for simw in SEMsimv:
		X.append(pm[simw[0]])
	X.append(mr[word])
	X.append(pmr[word+'|||N'])
	X.append(pmr[word+'|||V'])
	for simw in REMsim:
		X.append(mr[simw[0]])
	for simw in RSEMsimn:
		X.append(pmr[simw[0]])
	for simw in RSEMsimv:
		X.append(pmr[simw[0]])
	i += 1

X = np.array(X)
print('X lines: ' + str(len(X)))
print('X columns: ' + str(len(X[0])))
print('All lines: ' + str(len(all)))

#Calculate PCA:
print('PCA...')
pca = PCA(n_components=2)
X = pca.fit_transform(X)

#Create vector map:
vecmap = {}
vecmapr = {}
for i in range(0, int(len(all)/2)):
	word = all[i]
	vec = X[i]
	vecmap[word] = vec
for i in range(int(len(all)/2), len(all)):
	word = all[i]
	vec = X[i]
	vecmapr[word] = vec

#Create files:
o1 = open('similar_map.txt', 'w')
o2 = open('vector_map.txt', 'w')

for word in simmap:
	line = word + '\t'
	for sim in simmap[word]:
		line += sim[0].strip() + '\t'
	o1.write(line.strip() + '\n')
o1.close()

for word in vecmap:
	line = word + '\t' + str(vecmap[word][0]) + '\t' + str(vecmap[word][1]) + '\n'
	o2.write(line)
o1.close()
o2.close()

o1 = open('similar_mapr.txt', 'w')
o2 = open('vector_mapr.txt', 'w')

for word in simmapr:
	line = word + '\t'
	for sim in simmapr[word]:
		line += sim[0].strip() + '\t'
	o1.write(line.strip() + '\n')
o1.close()

for word in vecmapr:
	line = word + '\t' + str(vecmapr[word][0]) + '\t' + str(vecmapr[word][1]) + '\n'
	o2.write(line)
o1.close()
o2.close()
