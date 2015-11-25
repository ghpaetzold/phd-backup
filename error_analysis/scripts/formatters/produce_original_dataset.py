origmap = {}

f = open('../../corpora/lexmturk.txt')

for line in f:
	data = line.strip().split('\t')
	inst = (data[0].strip(), data[1].strip(), data[2].strip())
	origmap[inst] = line
f.close()

f = open('../../corpora/debelder.txt')

for line in f:
        data = line.strip().split('\t')
        inst = (data[0].strip(), data[1].strip(), data[2].strip())
        origmap[inst] = line
f.close()

print(str(len(origmap.keys())))

f = open('../../corpora/ls_dataset_benchmarking.txt')
o = open('../../corpora/ls_dataset_benchmarking_original.txt', 'w')
for line in f:
	data = line.strip().split('\t')
	inst = (data[0].strip(), data[1].strip(), data[2].strip())
	if inst not in origmap:
		print('Problem')
	else:
		o.write(origmap[inst])
f.close()
o.close()
