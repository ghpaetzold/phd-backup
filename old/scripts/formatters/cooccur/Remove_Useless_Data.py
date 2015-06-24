stop_words = set([])

f = open('../../../corpora/cooccur_vectors/vectors.txt')
o = open('../../../corpora/cooccur_vectors/vectors.clean.txt', 'w')

acceptable = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890'

for line in f:
	data = line.strip().split('\t')
	target = data[0].strip()
	if target[0] in acceptable and len(data)>1:
		o.write(line)
f.close()
o.close()
