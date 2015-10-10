f = open('toefl.qst')
o = open('toefl_training.txt', 'w')

candlist = []
for i in range(0, 80):
	target = f.readline().strip().split('\t')[1].strip()
	newline = target + '\t'
	cands = []
	for i in range(0, 4):
		cand = f.readline().strip().split('\t')[1].strip()
		cands.append(cand)
		newline += cand + '\t'
	f.readline()
	o.write(newline.strip() + '\n')
	candlist.append(cands)
f.close()
o.close()

f = open('toefl.ans')
o = open('toefl_testing.txt', 'w')
c = -1
for line in f:
	if len(line.strip())>0:
		c += 1
		cands = candlist[c]
		answer = line.strip().split('\t')[3].strip()
		if answer=='a':
			o.write(cands[0] + '\n')
		elif answer=='b':
			o.write(cands[1] + '\n')
		elif answer=='c':
			o.write(cands[2] + '\n')
		elif answer=='d':
			o.write(cands[3] + '\n')
		else:
			print('Problem: ' + answer)
f.close()
o.close()
