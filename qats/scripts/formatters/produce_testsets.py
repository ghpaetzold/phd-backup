import numpy as np

f = open('../../corpora/testset/test.shared-task.tsv')
s1s = open('../../corpora/testset/s1s.tok.txt')
s2s = open('../../corpora/testset/s2s.tok.txt')

types = ['G', 'S', 'M', 'O']

instances = []
for line in f:
	s1 = s1s.readline().strip()
	s2 = s2s.readline().strip()
	data = line.strip().split('\t')
	data[0] = s1
	data[1] = s2
	instances.append(data)
f.close()

for type in types:
	o = open('../../corpora/testset/'+type+'_all.txt', 'w')
	for instance in instances:
		o.write(instance[0] + '\t' + instance[1] + '\n')
	o.close()
