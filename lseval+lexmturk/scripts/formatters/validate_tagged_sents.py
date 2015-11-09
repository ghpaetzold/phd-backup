f = open('../evaluators/best_ss.txt')

for line in f:
	data = line.strip().split('\t')
	generator = data[0].strip()
	file = data[2].strip()

	f1 = open('../../substitutions/'+generator+'/'+file)
	f2 = open('../../corpora/tagged_sents_ls_dataset_benchmarking.txt')
	for line in f1:
		tokens = line.strip().split('\t')[0].strip().split(' ')
		tags = f2.readline().strip().split(' ')
		if len(tokens)!=len(tags):
			print('File: ' + '../../substitutions/'+generator+'/'+file)
	f1.close()
	f2.close()
f.close()

