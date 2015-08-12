import os

methods = set(os.listdir('../../substitutions/'))
methods.remove('all')

result = {}
for method in methods:
	f = open('../../substitutions/' + method + '/substitutions.txt')
	for line in f:
		data = line.strip().split('\t')
		target = data[0].strip()
		subs = set([sub.strip() for sub in data[1].strip().split('|||')])
		if target in result:
			result[target] = result[target].union(subs)
		else:
			result[target] = subs
	f.close()

o = open('../../substitutions/all/substitutions.txt', 'w')
for key in sorted(result.keys()):
	newline = key + '\t'
	for sub in result[key]:
		newline += sub + '|||'
	newline = newline[0:len(newline)-3]
	o.write(newline.strip() + '\n')
o.close()
