f = open('../../corpora/analysis/SG.txt')

max = -999999999
comb = None
for line in f:
	data = line.strip().split('\t')
	identifier = data[0]
	generator = data[1]
	selector = data[2]
	map = {}
	for item in data[3:]:
		itemd = item.strip().split('=')
		map[itemd[0].strip()] = int(itemd[1].strip())
	ok = map['OK']
	sum = ok + map['3A'] + map['3B']
	print(str(sum))
	if ok>max:
		max = ok
		comb = line.strip()

f.close()

print(str(comb))
