f = open('../../corpora/cwi_training_multitask.txt')
o = open('../../corpora/cwi_training_multitask_decomposed.txt', 'w')

for line in f:
	data = line.strip().split('\t')
	anns = data[3:]
	map = {0:set([]), 1:set([])}
	for ann in anns:
		annd = ann[1:len(ann)-1].split(', ')
		label = int(annd[4])
		map[label].add(ann)
	for label in map:
		if len(map[label])>0:
			newline = data[0] + '\t' + data[1] + '\t' + data[2] + '\t' + str(label)
			for ann in map[label]:
				newline += '\t' + ann
			o.write(newline + '\n')

f.close()
o.close()
