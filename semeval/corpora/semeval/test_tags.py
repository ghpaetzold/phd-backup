f1 = open('semeval_test_clean.txt')
f2 = open('tagged_sents_semeval_test.txt')

c = 0
for line1 in f1:
	line2 = f2.readline()
	tokens = line1.strip().split('\t')[0].strip().split(' ')
	tags = line2.strip().split(' ')
	if len(tokens)!=len(tags):
		print('Tokens: ' + str(tokens))
		print('Tags: ' + str(tags))
		print('')
		c += 1
f1.close()
f2.close()
print(str(c))
