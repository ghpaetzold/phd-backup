f1 = open('toefl_training.txt')
f2 = open('toefl_testing.txt')

for line in f1:
	answer = f2.readline().strip()
	cands = set(line.strip().split('\t')[1:])
	if answer not in cands:
		print('Problem!')

f1.close()
f2.close()

