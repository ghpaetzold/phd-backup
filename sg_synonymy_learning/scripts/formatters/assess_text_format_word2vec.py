f = open('../corpora/glovetemp.txt')

line = f.readline().strip()
print(str(line.split(' ')))
#line = f.readline().strip()
#print(str(line.split(' ')))

line = ''
c = 0
for l in f:
	c += 1
	line = l.strip()
print(str(line))
print(str(c))
f.close()
