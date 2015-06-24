def formatParse(line):
	result = ''
	tokens = line.split(' ')
	for token in tokens:
		tokend = token.strip().split('/')
		word = tokend[0].strip()
		pos = tokend[1].strip()
		result += word + '|||' + pos + ' '
	return result.strip()

fs = open('../../corpora/parsed/source.sents.parsedstanford.txt')
ft = open('../../corpora/parsed/target.sents.parsedstanford.txt')

os = open('../../corpora/parsed/source.sents.parsedstanford.formatted.txt', 'w')
ot = open('../../corpora/parsed/target.sents.parsedstanford.formatted.txt', 'w')

for line in fs:
	data = line.strip()
	if len(data)>0:
		data = formatParse(data)
		os.write(data.strip() + '\n')
fs.close()
os.close()

for line in ft:
	data = line.strip()
	if len(data)>0:
		data = formatParse(data)
		ot.write(data.strip() + '\n')
ft.close()
ot.close()
