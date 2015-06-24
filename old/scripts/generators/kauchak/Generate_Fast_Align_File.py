import os

def cleanPOS(posdata):
	result = ''
	result_pos = ''
	for token in posdata:
		tokend = token.split('|||')
		word = tokend[0].strip()
		pos = tokend[1].strip()
		if len(word.strip())>0:
			result += word.lower() + ' '
			result_pos += word.lower() + '|||' + pos + ' '
	return result.strip(), result_pos.strip()

f = open('../../../corpora/substitutions/kauchak/all.substitutions.txt')

post = open('../../../corpora/parsed/source.sents.parsedstanford.formatted.txt')
poss = open('../../../corpora/parsed/target.sents.parsedstanford.formatted.txt')

outt = open('../../../corpora/parsed/all.fastalign.txt', 'w')
outtp = open('../../../corpora/parsed/all.fastalign.pos.txt', 'w')

for line in f:
	data = line.strip().split('\t')
	sources = data[0].strip().split(' ')
	targets = data[1].strip().split(' ')

	posdatasr = poss.readline().strip()
	posdatas = posdatasr.split(' ')
	posdatatr = post.readline().strip()
	posdatat = posdatatr.split(' ')

	news, newsp = cleanPOS(posdatas)
	newt, newtp = cleanPOS(posdatat)

	if len(news.split(' '))!=len(newsp.split(' ')) or len(newt.split(' '))!=len(newtp.split(' ')):
		print('Problem :)')

	outt.write(news.lower().strip() + ' ||| ' + newt.lower().strip() + '\n')
	outtp.write(newsp.lower().strip() + '\t' + newtp.lower().strip() + '\n')
f.close()
poss.close()
post.close()
outt.close()
outtp.close()
