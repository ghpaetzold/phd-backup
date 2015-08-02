f = open('../../corpora/lexmturk_nosupervision.txt')
o1 = open('../../corpora/lexmturk_nosupervision_train.txt', 'w')
o2 = open('../../corpora/lexmturk_nosupervision_test.txt', 'w')

for i in range(0, 250):
	line = f.readline()
	o1.write(line)

for i in range(0, 250):
	line = f.readline()
	o2.write(line)

o1.close()
o2.close()
