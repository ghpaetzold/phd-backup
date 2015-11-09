f = open('../../../corpora/wcefiles/cwictor_corpus.txt')
c = 0
for line in f:
	c += 1
f.close()
print(str(c))
