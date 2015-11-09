f = open('../../corpora/analysis/SR.txt')

max = -999999999
comb = None
for line in f:
	data = line.strip().split('\t')
	identifier = data[0]
	generator = data[1]
	selector = data[2]
	ranker = data[3]
	map = {}
	for item in data[4:]:
		itemd = item.strip().split('=')
		map[itemd[0].strip()] = int(itemd[1].strip())
	ok = map['OK']
	sum = ok + map['4'] + map['5']
	print(str(sum))
	if ok>max:
		max = ok
		comb = line.strip()

f.close()

print(str(comb))
