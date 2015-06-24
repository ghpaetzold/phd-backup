import sys

cwictor = sys.argv[1]
predicted = sys.argv[2]

f1 = open(cwictor)
f2 = open(predicted)

falsec = 0
falses = 0
for line in f1:
	data = line.strip().split('\t')
	sentence = data[0].strip()
	target = data[1].strip()
	head = int(data[2].strip())
	glabel = int(data[3].strip())

	plabel = int(f2.readline().strip())

	if glabel!=plabel:
		print('Word \"' + target + '\" is ' + str(glabel) + ', predicted as ' + str(plabel))
		if plabel==1:
			falsec += 1
		elif plabel==0:
			falses += 1
print('Predicted complex, but simple: ' + str(falsec))
print('Predicted simple, but complex: ' + str(falses))
f1.close()
f2.close() 
