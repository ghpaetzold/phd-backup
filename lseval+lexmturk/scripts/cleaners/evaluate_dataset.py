f = open('../../corpora/ls_dataset_benchmarking.txt')

counter = 0
for line in f:
	data = line.strip().split('\t')
	target = data[1].strip()
	cands = [c.strip().split(':')[1].strip() for c in data[3:]]
	for cand in cands:
		if cand==target:
			counter += 1
print(str(counter))

f.close()
