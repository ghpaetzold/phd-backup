import re

f = open('../../corpora/alignments/source_target.alignments.txt')

o = open('../../corpora/substitutions/source_target.substitutions.txt', 'w')

substitutions = {}

line = f.readline().strip()
line = f.readline().strip()
while line != ']':
	source_sent = f.readline().strip()
	firstsent = source_sent.lower().split(' ')
	line = f.readline().strip()
	if line.startswith('NULL'):
		res = re.findall('([^\s]+) \(\{([^\}]+)\}\)', line.strip())
		secondsent = ''
		for i in range(1, len(res)):
			data = res[i]
			secondsent += data[0].strip() + ' '
		target_sent = secondsent.strip()

		newline = source_sent + '\t' + target_sent + '\t'

		total_substitutions = 0		
		for i in range(1, len(res)):
			data = res[i]
			target_word = data[0].strip().lower()
			aux = data[1].strip().split('/')[0].strip()
			if len(aux)>0:
				indexes = aux.split(' ')
				for index in indexes:
					source_word = firstsent[int(index)-1]
					if target_word!=source_word:
						total_substitutions += 1
						newline += str(int(index)-1)+'|||'+source_word+'|||'+str(i-1)+'|||'+target_word+'\t'
		o.write(newline.strip() + '\n')
	line = f.readline().strip()
o.close()
f.close()
