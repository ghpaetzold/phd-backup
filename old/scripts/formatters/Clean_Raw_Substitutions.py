

folders = ['biran', 'merriam', 'wordnet', 'yamamoto']

path = '/export/data/ghpaetzold/substitutiongeneration/corpora/substitutions/'

for folder in folders:
	f = open(path + folder + '/substitutions.txt')
	o = open(path + folder + '/substitutions.clean.txt', 'w')

	for line in f:
		data = line.strip().split('\t')
		if len(data)>1:
			o.write(line.strip() + '\n')
	f.close()
	o.close()

