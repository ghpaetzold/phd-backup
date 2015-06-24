import sys, os, nltk, pywsd

inpsubs = sys.argv[1]
outsubs = sys.argv[2]
temp = sys.argv[3]

def getSense(sentence, target):
	try:
		result = pywsd.similarity.max_similarity(sentence, target, option="lch", best=False)
		return result
	except IndexError:
		return None

def getCandidateSentence(sentence, candidate, head):
	tokens = sentence.strip().split(' ')
	result = ''
	for i in range(0, head):
		result += tokens[i] + ' '
	result += candidate + ' '
	for i in range(head+1, len(tokens)):
		result += tokens[i] + ' '
	return result.strip()

def getHead(sent, target):
        tokens = sent.strip().lower().split(' ')
        head = -1
        for i in range(0, len(tokens)):
                if target == tokens[i]:
                        head = i
        return head

substitutions = {}
inpf = open(inpsubs)
for line in inpf:
	data = line.strip().split('\t')
	target = data[0].strip()
	subs = sorted(data[1].strip().split('|||'))
	substitutions[target] = subs
inpf.close()

outf = open(outsubs, 'w')
lex = '../../corpora/lexmturk/lexmturk.txt'
lexf = open(lex)
c = 0
for line in lexf:
	c += 1
	print(str(c))
	data = line.strip().split('\t')
	sent = data[0].strip()
	target = data[1].strip()
	head = getHead(sent, target)
	
	target_sense = getSense(sent, target)

	candidates = []
	if target in substitutions.keys():
		candidates = substitutions[target]
	
	newline = target + '\t'
	for candidate in candidates:
		candidate_sense = None
		try:
			unic = unicode(candidate)
			candidate_sense = getSense(getCandidateSentence(sent, candidate, head), candidate)
		except UnicodeDecodeError:
			candidate_sense = None
		if target_sense or not candidate_sense:
			if not candidate_sense or candidate_sense==target_sense:
				newline += candidate + '|||'

	if newline.endswith('|||'):
		newline = newline[0:len(newline)-3]
	outf.write(newline.strip() + '\n')
lexf.close()
outf.close()
