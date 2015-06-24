import sys

file = sys.argv[1]

f = open(file)
s = 0
for line in f:
	data = line.strip().split('\t')
	s += len(data[3:len(data)])
f.close()
print(str(s))	
