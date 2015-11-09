complex = set([line.strip() for line in open('../../corpora/complex_words.txt')])

f = open('../../corpora/ls_dataset_benchmarking.txt')
o = open('../../corpora/ls_dataset_benchmarking_simple.txt', 'w')

for line in f:
	data = line.strip().split('\t')
	newline = data[0].strip() + '\t' + data[1].strip() + '\t' + data[2].strip() + '\t'
	cands = set([])
	for cand in data[3:]:
		c = cand.strip().split(':')[1].strip()
		if c not in complex:
			newline += cand + '\t'
	o.write(newline.strip() + '\n')
f.close()
o.close()
