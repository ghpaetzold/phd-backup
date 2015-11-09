import os

targets = set([])
f = open('/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt')
for line in f:
	targets.add(line.strip().split('\t')[1])
f.close()

methods = set(os.listdir('../../substitutions/'))
methods.remove('all')
methods = sorted(list(methods))
print(str(methods))

#Generating maps:
methodmap = {}
for method in methods:
	f = open('../../substitutions/' + method + '/substitutions.txt')
	submap = {}
	for line in f:
		data = line.strip().split('\t')
		target = data[0].strip()
		subs = set([sub.strip() for sub in data[1].strip().split('|||')])
		if target in targets:
			submap[target] = subs
	f.close()
	methodmap[method] = submap

#Creating combinations:
for i in range(0, len(methods)-1):
	for j in range(i+1, len(methods)):
		print('At: ' + str(i) + ', ' + str(j))
		m1 = methods[i]
		m2 = methods[j]
		path = '../../substitutions/'+m1+'+'+m2+'/'
		print(str(path))
		os.system('mkdir ' + path)

		#Build mixed dictionary:
		mixed = {}
		map1 = methodmap[m1]
		map2 = methodmap[m2]
		for key in map1:
			mixed[key] = map1[key]
		for key in map2:
			if key not in mixed:
				mixed[key] = map2[key]
			else:
				mixed[key].update(map2[key])		

		o = open(path + 'substitutions.txt', 'w')
		for key in mixed:
			newline = key + '\t'
			for sub in mixed[key]:
				newline += sub + '|||'
			newline = newline[0:len(newline)-3]
			o.write(newline.strip() + '\n')
		o.close()

#Creating combinations:
for i in range(0, len(methods)-2):
	for j in range(i+1, len(methods)-1):
		for k in range(j+1, len(methods)):
			print('At: ' + str(i) + ', ' + str(j))
			m1 = methods[i]
			m2 = methods[j]
			m3 = methods[k]
			path = '../../substitutions/'+m1+'+'+m2+'+'+m3+'/'
			print(str(path))
			os.system('mkdir ' + path)
	
			#Build mixed dictionary:
			mixed = {}
			map1 = methodmap[m1]
			map2 = methodmap[m2]
			map3 = methodmap[m3]
			for key in map1:
				mixed[key] = map1[key]
			for key in map2:
				if key not in mixed:
					mixed[key] = map2[key]
				else:
					mixed[key].update(map2[key])
			for key in map3:
				if key not in mixed:
					mixed[key] = map3[key]
				else:
					mixed[key].update(map3[key])
	
			o = open(path + 'substitutions.txt', 'w')
			for key in mixed:
				newline = key + '\t'
				for sub in mixed[key]:
					newline += sub + '|||'
				newline = newline[0:len(newline)-3]
				o.write(newline.strip() + '\n')
			o.close()
