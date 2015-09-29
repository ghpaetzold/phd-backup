f1 = open('../../corpora/ls_dataset_benchmarking.txt')
#f2 = open('../../corpora/tagged_sents_ls_dataset_benchmarking.txt')

tuples = []
for line1 in f1:
#	line2 = f2.readline()
	tuple = line1.strip()
	tuples.append(tuple)
f1.close()
#f2.close()

tuples = set(tuples)
tuples = list(tuples)

f1 = open('../../corpora/ls_dataset_benchmarking_train.txt', 'w')
f2 = open('../../corpora/ls_dataset_benchmarking_test.txt', 'w')
#f3 = open('../../corpora/tagged_sents_ls_dataset_benchmarking_train.txt', 'w')
#f4 = open('../../corpora/tagged_sents_ls_dataset_benchmarking_test.txt', 'w')
for i in range(0, 465):
	tuple = tuples[i]
	f1.write(tuple + '\n')

for i in range(0, 464):
	tuple = tuples[i]
	f2.write(tuple + '\n')
f1.close()
f2.close()
