f = open('../../corpora/lexmturk/lexmturk_all.txt')
o1 = open('../../corpora/lexmturk/lexmturk_train.txt', 'w')
o2 = open('../../corpora/lexmturk/lexmturk_test.txt', 'w')

for i in range(0, 450):
	o1.write(f.readline().strip() + '\n')
for i in range(0, 50):
	o2.write(f.readline().strip() + '\n')

f.close()
o1.close()
o2.close()
