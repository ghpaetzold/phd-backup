complex = set([line.strip() for line in open('../../corpora/complex_words.txt')])

f = open('../../corpora/ls_dataset_benchmarking.txt')
allcands = []
for line in f:
	data = line.strip().split('\t')
	cands = data[3:]
	allcands.extend(cands)
print(str(len(allcands)))
f.close()

f = open('../../corpora/ls_dataset_benchmarking_simple.txt')
simplecands = []
for line in f:
	data = line.strip().split('\t')
	target = data[1].strip()
	cands = data[3:]
	if len(cands)==0 and target not in complex:
		print('Problem')
	simplecands.extend(cands)
print(str(len(simplecands)))
f.close()
