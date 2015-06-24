import os

def getPrefixes():
	files = os.listdir('../../corpora/substitutions/biran/')
	result = set([])
	for file in files:
		if file.startswith('substitutions'):
			if len(file.split('.'))>2:
				prefix = file.split('.')[1].strip()
				result.add(prefix)
	return result

methods = ['biran', 'kauchak', 'merriam', 'wordnet', 'yamamoto']

root = '../../corpora/substitutions/'

fout = open(root + 'all/substitutions.txt', 'w')
substs = {}
for method in methods:
	fin = open(root + method + '/substitutions.txt')
	for line in fin:
		data = line.strip().split('\t')
		if len(data)>1:
			target = data[0].strip()
			subs = set(data[1].strip().split('|||'))
			if target not in substs.keys():
				substs[target] = subs
			else:
				substs[target] = substs[target].union(subs)
	fin.close()

for target in substs:
	newline = target + '\t'
	for cand in substs[target]:
		newline += cand.strip() + '|||'
	if newline.endswith('|||'):
		newline = newline[0:len(newline)-3]
	fout.write(newline.strip() + '\n')
fout.close()

prefixes = getPrefixes()
print(str(prefixes))

for prefix in prefixes:
	fout = open(root + 'all/substitutions.' + prefix + '.txt', 'w')
	outdata = []
	for method in methods:
		fin = open(root + method + '/substitutions.' + prefix + '.txt')
		for i in range(0, 500):
			line = fin.readline()
			data = line.strip().split('\t')
			target = data[0].strip()
			if len(outdata)<i+1:
				outdata.append({target:set([])})
			if len(data)>1:
				if target not in outdata[i]:
					outdata[i][target] = set([]) 
				outdata[i][target] = outdata[i][target].union(set(data[1].strip().split('|||')))
		fin.close()
	for i in range(0,500):
		for k in outdata[i].keys():
			newline = k + '\t'
			for cand in outdata[i][k]:
				newline += cand + '|||'
			if newline.endswith('|||'):
				newline = newline[0:len(newline)-3]
			fout.write(newline.strip() + '\n')
	fout.close()				
