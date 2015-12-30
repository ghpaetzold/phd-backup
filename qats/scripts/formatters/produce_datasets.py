import numpy as np

f = open('../../corpora/original.txt')
s1s = open('../../corpora/s1s.tok.txt')
s2s = open('../../corpora/s2s.tok.txt')

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

np.random.shuffle(instances)

trains = []
tests = []
for type in types:
	trains.append(open('../../corpora/'+type+'_train.txt', 'w'))
	tests.append(open('../../corpora/'+type+'_test.txt', 'w'))

map = {'bad':'0', 'ok':'1', 'good':'2'}

for i in range(0, 300):
	instance = instances[i]
	s1 = instance[0]
	s2 = instance[1]
	values = instance[2:]
	for j in range(0, len(types)):
		trains[j].write(s1 + '\t' + s2 + '\t' + map[values[j]] + '\n')

for i in range(300, len(instances)):
	instance = instances[i]
        s1 = instance[0]
        s2 = instance[1]
        values = instance[2:]
        for j in range(0, len(types)):
                tests[j].write(s1 + '\t' + s2 + '\t' + map[values[j]] + '\n')

for train in trains:
	train.close()
for test in tests:
	test.close()
