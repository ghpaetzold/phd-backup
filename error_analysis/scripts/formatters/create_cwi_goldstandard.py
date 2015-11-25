complex = set([line.strip() for line in open('../../corpora/complex_words.txt')])

f = open('../../corpora/ls_dataset_benchmarking.txt')
o = open('../../corpora/cwi_gold_standard.txt', 'w')
c = 0
for line in f:
	data = line.strip().split('\t')
	target = data[1].strip()
	if target in complex:
		c += 1
		o.write(data[0]+'\t'+data[1]+'\t'+data[2]+'\t1\n')
	else:
		o.write(data[0]+'\t'+data[1]+'\t'+data[2]+'\t0\n')
f.close()
o.close()

print(str(c))
