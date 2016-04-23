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
	labelg = data[2]
	labels = data[3]
	labelm = data[4]
	labelo = data[5]
	instances.append(s1 + '\t' + s2 + '\t' + labelg + '\t' + labels + '\t' + labelm + '\t' + labelo)
f.close()

trains = []
f1 = open('../../corpora/G_train.txt')
f2 = open('../../corpora/S_train.txt')
f3 = open('../../corpora/M_train.txt')
f4 = open('../../corpora/O_train.txt')
map = {'0':'bad', '1':'ok', '2':'good'}
invmap = {'bad':'0', 'ok':'1', 'good':'2'}
for line in f1:
	data = line.strip().split('\t')
	S = map[f2.readline().strip().split('\t')[2].strip()]
	M = map[f3.readline().strip().split('\t')[2].strip()]
	O = map[f4.readline().strip().split('\t')[2].strip()]
	trains.append(data[0].strip() + '\t' + data[1].strip() + '\t' + map[data[2].strip()] + '\t' + S + '\t' + M + '\t' + O)
f1.close()
f2.close()
f3.close()
f4.close()

print(str(len(instances)))
print(str(len(trains)))

for train in trains:
	instances.remove(train)
print(str(len(instances)))

f1 = open('../../corpora/G_test.txt','w')
f2 = open('../../corpora/S_test.txt','w')
f3 = open('../../corpora/M_test.txt','w')
f4 = open('../../corpora/O_test.txt','w')
for instance in instances:
	data = instance.split('\t')
	s1 = data[0]
	s2 = data[1]
	G = data[2]
	S = data[3]
	M = data[4]
	O = data[5]
	f1.write(s1 + '\t' + s2 + '\t' + invmap[G] + '\n')
	f2.write(s1 + '\t' + s2 + '\t' + invmap[S] + '\n')
	f3.write(s1 + '\t' + s2 + '\t' + invmap[M] + '\n')
	f4.write(s1 + '\t' + s2 + '\t' + invmap[O] + '\n')
f1.close()
f2.close()
f3.close()
f4.close()
