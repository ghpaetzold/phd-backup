import os

files = os.listdir('/export/data/ghpaetzold/substitutiongeneration/corpora/substitutions/kauchak/')

for file in files:
	data = file.strip().split('.')
	if len(data)>2:
		f = open('/export/data/ghpaetzold/substitutiongeneration/corpora/substitutions/kauchak/' + file)
		c = 0
		for line in f:
			c += 1
		if c != 500:
			print('Problem at: ' + file)
		f.close()
