f1 = open('NNSimpLex_test.txt')
f2 = open('tagged_sents_NNSimpLex_test.txt')

for line in f1:
	data = line.strip().split('\t')
	tokens = data[0].strip().split(' ')
	tags = f2.readline().strip().split(' ')
	if len(tokens)!=len(tags):
		print('Problem')
f1.close()
f2.close()
