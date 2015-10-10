f = open('../../corpora/NNSimpLex.txt')
tr = open('../../corpora/NNSimpLex_train.txt', 'w')
te = open('../../corpora/NNSimpLex_test.txt', 'w')

for i in range(0, 450):
	tr.write(f.readline())
for i in range(0, 451):
	te.write(f.readline())

f.close()
tr.close()
te.close()
