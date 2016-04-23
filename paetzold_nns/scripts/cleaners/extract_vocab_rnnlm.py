import os

files = os.listdir('/export/data/ghpaetzold/word2vecvectors/corpora/wiki_simplewiki_subtlex/split_tagged/')
vocab = {}
for file in files:
	print(str(file))
	f = open('/export/data/ghpaetzold/word2vecvectors/corpora/wiki_simplewiki_subtlex/split_tagged/'+file)
	for line in f:
		tokens = line.strip().split(' ')
		for token in tokens:
			if token not in vocab:
				vocab[token] = 0
			vocab[token] += 1
	f.close()

o = open('../../corpora/vocab_rnnlm.txt', 'w')
for word in vocab:
	o.write(word + '\t' + str(vocab[word]) + '\n')
o.close()
