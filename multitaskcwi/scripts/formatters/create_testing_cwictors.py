f = open('../../corpora/cwi_testing_multitask.txt')
o = open('../../corpora/cwi_testing_multitask_decomposed.txt', 'w')

for line in f:
	data = line.strip().split('\t')
	anns = data[3:]
	map = {0:set([]), 1:set([])}
	for ann in anns:
		annd = ann[1:len(ann)-1].split(', ')
		label = int(annd[4])
		map[label].add(ann)
	if len(map[1])>0:
		newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t' + str(label)
		newline += '\t' + list(map[1])[0]
		o.write(newline + '\n')
	else:
		newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t' + str(label)
                newline += '\t' + list(map[0])[0]
                o.write(newline + '\n')
f.close()
o.close()
