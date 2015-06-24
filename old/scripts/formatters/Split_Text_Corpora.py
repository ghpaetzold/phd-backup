
f = open('../../corpora/text/all.txt')

n_files = 20
out = []
for i in range(0, n_files):
	out.append(open('../../corpora/text/split/all.' + str(i) + '.txt', 'w', encoding='utf-8'))

c = 0
index = 0
for line in f:
	c += 1
	print(str(c))
	o = out[index]
	o.write(line)
	index += 1
	if index == n_files:
		index = 0
f.close()

for o in out:
	o.close()
