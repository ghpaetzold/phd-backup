import sys, os, nltk

inpsubs = sys.argv[1]
outsubs = sys.argv[2]
temp = sys.argv[3]

def getSubSenseFromData(sensedata, head):
        line = sensedata[head]
        data = line.strip().split('\t')
        word = data[0].strip()
        sense = data[3].strip().split('/')[0].strip()
        return word, sense

def getSenseFromData(sensedata, target):
	final_sense = None
	head = -1
	for i in range(0, len(sensedata)):
		line = sensedata[i]
		data = line.strip().split('\t')
		word = data[0].strip()
		sense = data[3].strip().split('/')[0].strip()
		if target == word:
			final_sense = sense
			head = i
	return final_sense, head

def getPOSAndStem(sent, target, subs):
	result = []

	stemmer = nltk.stem.porter.PorterStemmer()

	#Get head:
	head = -1
	tokens = sent.strip().lower().split(' ')
	for i in range(0, len(tokens)):
		token = tokens[i]
		if token==target:
			head = i
	
	#Get POS data of original sentence:
	pos_data = nltk.pos_tag(tokens)
	
	#Get stems of original sentence:
	stem_data = getStems(tokens, stemmer)

	#Add data to result:
	inst = []
	for i in range(0, len(pos_data)):
		inst.append((tokens[i], fromTBtoWN(pos_data[i][1]), stem_data[i]))
	result.append(inst)

	#Get POS/stems for each substitution:
	for sub in subs:
		sub_pos = getSubPOS(tokens, head, sub)
		sub_stem = stemmer.stem(sub)
		inst = []
		for i in range(0, head):
			inst.append((tokens[i], fromTBtoWN(pos_data[i][1]), stem_data[i]))
		inst.append((sub, sub_pos, sub_stem))
		for i in range(head+1, len(tokens)):
			inst.append((tokens[i], fromTBtoWN(pos_data[i][1]), stem_data[i]))
		result.append(inst)
	if sent.find('termites')>-1:
		print(str(result))
	return result

def getSubPOS(tokens, head, sub):
	sent = tokens
	sent[head] = sub
	pos_d = nltk.pos_tag(sent)
	pos = pos_d[head][1]
	pos = fromTBtoWN(pos)
	return pos

def fromTBtoWN(pos):
	if pos.startswith('N'):
		return 'n'
	elif pos.startswith('J'):
		return 'j'
	elif pos.startswith('RB'):
		return 'r'
	elif pos.startswith('V'):
		return 'v'
	else:
		return pos[0].lower()	

def getStems(tokens, stemmer):
	result = []
	for token in tokens:
		stem = stemmer.stem(token)
		result.append(stem)
	return result

lexf = open('../../corpora/lexmturk/lexmturk.txt')
subsf = open(inpsubs)

#Get substitutions:
subs = {}
for line in subsf:
	data = line.strip().split('\t')
	left = data[0].strip()
	if len(data)>1:
		rights = set(data[1].strip().split('|||'))
		subs[left] = rights
subsf.close()

#Disambiguate:
tempf = open(temp+'temp_input.txt', 'w')
lex = []
c = -1
#for i in range(0, 4):
#	line = lexf.readline()
for line in lexf:
	c += 1
	print(str(c))
	data = line.strip().split('\t')
	sent = data[0].strip()
	target = data[1].strip()
	if target in subs.keys():
		sub_data = getPOSAndStem(sent, target, subs[target])
		lex.append((sent, target))
		for instance in sub_data:
			for wordd in instance:
				word = wordd[0]
				pos = wordd[1]
				stem = wordd[2]
				tempf.write(word + '\t' + pos + '\t' + stem + '\n')
			tempf.write('\n')
tempf.close()
lexf.close()

lesk_path = '/export/data/ghpaetzold/wsdcorpus/enhancedlesk/lesk-wsd-dsm-master/'
dsm_path = '/export/data/ghpaetzold/wsdcorpus/enhancedlesk/termvectors_en.bin'
folder_path = '/export/data/ghpaetzold/substitutiongeneration/scripts/selectors/'

os.chdir(lesk_path)
comm = './run.sh -i ' + temp + 'temp_input.txt -o ' + temp + 'temp_output.txt -cm sent -f plain -dsm ' + dsm_path
comm += ' -lang en -sc ' + lesk_path + 'resources/sense/en/ -sdType prob -sf wn -c max -of plain -stem true'
os.system(comm)
os.chdir(folder_path)

#Get sense data:
sensef = open(temp+'temp_output.txt')
sensedata = []
currdata = []
for line in sensef:
	if len(line.strip())>0:
		currdata.append(line.strip())
	else:
		sensedata.append(currdata)
		currdata = []



#Get senses of candidates:
index = 0
out = open(outsubs, 'w')
for inst in lex:
	sent = inst[0]
	target = inst[1]
	target_sense, head = getSenseFromData(sensedata[index], target)
	index += 1

	datasize = len(sensedata[index])

	final_subs = set([])
	for sub in subs[target]:
		sub_word, sub_sense = getSubSenseFromData(sensedata[index], head)
		index += 1
		if target_sense==sub_sense:
			final_subs.add(sub_word)
	newline = target + '\t'
	for final_sub in final_subs:
		newline += final_sub + '|||'
	if newline.endswith('|||'):
		newline = newline[0:len(newline)-3]
	out.write(newline.strip() + '\n')
out.close()
