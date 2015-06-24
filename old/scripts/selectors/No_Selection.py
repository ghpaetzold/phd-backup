import sys, os, nltk

inpsubs = sys.argv[1]
outsubs = sys.argv[2]
temp = sys.argv[3]

lexf = open('../../corpora/lexmturk/lexmturk.txt')
subsf = open(inpsubs)
outf = open(outsubs, 'w')

#Get substitutions:
subs = {}
for line in subsf:
	data = line.strip().split('\t')
	target = data[0].strip()
	if len(data)>1:
		subs[target] = data[1].strip()
subsf.close()

for line in lexf:
	data = line.strip().split('\t')
	target = data[1].strip()
	if target in subs.keys():
		outf.write(target + '\t' + subs[target] + '\n')
	else:
		outf.write(target + '\n')
lexf.close()
outf.close()

