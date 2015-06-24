def reverseSubs(subs):
	result = []
	for sub in subs:
		aux = sub.strip().split('|||')
		indext = aux[0].strip()
		indexs = aux[2].strip()
		wordt = aux[1].strip()
		words = aux[3].strip()
		result.append(indexs+'|||'+words+'|||'+indext+'|||'+wordt)
	return result

fst = open('../../corpora/substitutions/source_target.substitutions.txt')
fts = open('../../corpora/substitutions/target_source.substitutions.txt')

out = open('../../corpora/substitutions/all.substitutions.txt', 'w')

for line in fst:
	datast = line.strip().split('\t')
	source = datast[0].strip()
	target = datast[1].strip()
	subsst = []
	if len(datast)>2:
		subsst = datast[2:len(datast)]
	datats = fts.readline().strip().split('\t')
	substs = []
	if len(datats)>2:
		substs = datats[2:len(datats)]
		substs = reverseSubs(substs)
	subsst.extend(substs)
	allsubs = set(subsst)
	if len(allsubs)>0:
		newline = source + '\t' + target + '\t'
		for sub in allsubs:
			newline += sub + '\t'
		out.write(newline.strip() + '\n')
out.close()
fst.close()
fts.close()
