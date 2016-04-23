import sys

file = sys.argv[1]

c = 0
t = 0
f = open(file)
for line in f:
	t += 1
	data = line.strip().split('\t')
	label = data[3]
	if label=='1':
		c += 1
f.close()
print(str(c))
print(str(t))
