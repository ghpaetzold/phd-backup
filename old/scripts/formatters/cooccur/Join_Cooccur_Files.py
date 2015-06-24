import os

def notNumber(text):
        try:
                num = float(text.strip())
                return False
        except ValueError:
                return True

stop_words = set([line.strip() for line in open('../../../corpora/stop_words/stop_words.txt')])

files = os.listdir('../../../corpora/cooccur_vectors/split/')

cooccurs = {}
c = 0
for file in files:
	c += 1
	print('At reading:' + str(float(c)/float(len(files))))
	f = open('../../../corpora/cooccur_vectors/split/'+file)
	for line in f:
		data = line.strip().split('\t')
		target = data[0]
		if target not in cooccurs.keys():
			cooccurs[target] = {}

		coocs = data[1:len(data)]
		for cooc in coocs:
			coocd = cooc.split(':')
			word = coocd[len(coocd)-2].strip()
			freq = int(coocd[len(coocd)-1].strip())
			if word not in stop_words:
				if word in cooccurs[target].keys():
					cooccurs[target][word] += freq
				else:
					cooccurs[target][word] = freq
	f.close()

final_cooccurs = {}
all_words = set([])
c = 0
for target in cooccurs.keys():
	c += 1
	print('At filtering:' + str(float(c)/float(len(cooccurs.keys()))))
	final_cooccurs[target] = {}
	for word in cooccurs[target].keys():
		w = None
		if notNumber(word.strip()):
			w = word.strip()
		else:
			w = '#NUMERAL#'
		all_words.add(w)
		if cooccurs[target][word]>2 or w=='#NUMERAL#':
			if w not in final_cooccurs[target].keys():
				final_cooccurs[target][w] = cooccurs[target][word]
			else:
				final_cooccurs[target][w] += cooccurs[target][word]

all_words = sorted(list(all_words))

out = open('../../../corpora/cooccur_vectors/vectors.txt', 'w')

acceptable = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890'

print('Writing...')
for target in sorted(list(final_cooccurs.keys())):
	if target[0] in acceptable and len(final_cooccurs[target].keys())>0:
		newline = target + '\t'
		for word in sorted(list(final_cooccurs[target].keys())):
			newline += word+':'+str(final_cooccurs[target][word]) + '\t'
		out.write(newline.strip() + '\n')
out.close()
print('Done!')
