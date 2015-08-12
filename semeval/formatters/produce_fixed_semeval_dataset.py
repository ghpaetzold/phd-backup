import sys, math

inp = sys.argv[1]
tags = sys.argv[2]
out = sys.argv[3]

f1 = open(inp)
f2 = open(tags)
o = open(out, 'w')

for line in f1:
	data = line.strip().split('\t')
	target = data[1].strip()
	head = int(data[2].strip())
	tags = f2.readline().strip().split(' ')

	tgtindexes = []

	sent = ''
	for i in range(0, len(tags)):
		tag = tags[i]
		tagd = tag.split('|||')
		sent += tagd[0].strip() + ' '
		if tagd[0].strip()==target:
			tgtindexes.append(i)

	
	newline = sent.strip() + '\t' + target + '\t'

	newhead = -1
	mindiff = 999999
	for index in tgtindexes:
		diff = math.fabs(index-head)
		if diff<mindiff:
			mindiff = diff
			newhead = index
	if len(tgtindexes)>1:
		print('\nOriginal head: ' + str(head))
		print('Selected head: ' + str(newhead))
		print('Options: ' + str(tgtindexes))
		print('Sentence: ' + str(sent))

	if newhead > -1:
		newline += str(newhead) + '\t'
	else:
		print('Big error!')

	for i in range(3, len(data)):
		newline += data[i] + '\t'
	o.write(newline.strip() + '\n')

f1.close()
f2.close()
o.close()
		
