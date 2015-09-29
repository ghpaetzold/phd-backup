import gensim

posw2vmodel = '/export/data/ghpaetzold/word2vecvectors/models/word_vectors_all_500_cbow_retrofitted.bin'
model = gensim.models.word2vec.Word2Vec.load_word2vec_format(posw2vmodel, binary=True)

words = ['good', 'large', 'thin', 'short', 'blonde']

for word in words:
	most_sim = model.most_similar(positive=[word], topn=5)
	newline = word + ' & ' + most_sim[0][0]
	for word in most_sim[1:]:
		newline += ', ' + word[0]
	print(newline.strip() + r' \\')
