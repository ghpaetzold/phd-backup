import os

sents = []
f = open('/export/data/ghpaetzold/benchmarking/qats/corpora/testset/G_all.txt')
for line in f:
	sents.append(line.strip())
f.close()

labels = {}
types = ['O', 'G', 'M', 'S']
for type in types:
	labels[type] = []

f = open('/export/data/ghpaetzold/benchmarking/qats/corpora/gold/labels.txt')
f.readline()
for line in f:
	data = line.strip().split('\t')
	for i in range(0, len(types)):
		type = types[i]
		label = data[i]
		labels[type].append(label)
f.close()

map = {}
map['bad'] = 0
map['ok'] = 1
map['good'] = 2

files = {}
for type in types:
	files[type] = open('/export/data/ghpaetzold/benchmarking/qats/corpora/testset/'+type+'_all_with_labels.txt', 'w')

for type in types:
	typelabels = labels[type]
	file = files[type]
	for i in range(0, len(sents)):
		file.write(sents[i] + '\t' + str(map[typelabels[i]]) + '\n')

for type in files:
	files[type].close()
