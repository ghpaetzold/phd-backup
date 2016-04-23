f = open('../../corpora/vocab_rnnlm_20.txt')
c = 0
for line in f:
	c += 1
	print(str(c))
f.close()
