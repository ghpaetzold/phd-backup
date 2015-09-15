import sys, os

size = sys.argv[1]

orig = '../../corpora/wordvectors/retrofitted_wordnetparsed'+size+'_vectors.txt'
fixed = '../../corpora/wordvectors/retrofitted_wordnetparsed'+size+'_vectors_fixed.txt'
f = open(orig)
o = open(fixed, 'w')

for line in f:
	data = line.strip().split(' ')
	lexeme = data[0]
	lexemed = lexeme.strip().split('|||')
	word = lexemed[0].strip()
	tag = lexemed[1].strip().upper()
	newline = word+'|||'+tag + ' '
	for value in data[1:]:
		newline += value + ' '
	o.write(newline.strip() + '\n')
f.close()
o.close()

#os.system('mv ' + fixed + ' ' + orig)
