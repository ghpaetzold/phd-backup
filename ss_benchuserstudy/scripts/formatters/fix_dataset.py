import nltk, math

def getNewHead(sent, target, head):
	indexes = set([])
	tokens = sent.strip().split(' ')
	for i in range(0, len(tokens)):
		if target.lower()==tokens[i].lower():
			indexes.add(i)
	mindist = 9999999
	minindex = -1
	for index in indexes:
		dist = math.fabs(index-head)
		if dist<mindist:
			mindist = dist
			minindex = index
	return minindex

f = open('../../corpora/ss_dataset_userstudy.txt')
t = open('../../corpora/tagged_sents_dataset.txt')
o = open('../../corpora/ss_dataset_userstudy_final.txt', 'w')

for line in f:
	data = line.strip().split('\t')
	tags = t.readline().strip().split(' ')
	target = data[1].strip()

	sent = ''
	for tag in tags:
		token = tag.strip().split('|||')[0]
		sent += token + ' '

	newhead = getNewHead(sent, data[1].strip(), int(data[2].strip()))
	if sent.strip().split(' ')[newhead].lower()!=target:
		print('Problem!')

	newline = sent.strip() + '\t' + data[1].strip() + '\t' + str(newhead) + '\t'
	for item in data[3:]:
		itemd = item.strip().split(':')
		if itemd[0].strip()=='1':
			newline += item + '\t'
	o.write(newline.strip() +  '\n')
	
f.close()
o.close()
