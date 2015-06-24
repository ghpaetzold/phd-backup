import subprocess

def getInflections(verbstems):
	text1 = ''
	text2 = ''
	text3 = ''
	for verb in verbstems:
		text1 += verb.strip() + ' PAST_PERFECT_PARTICIPLE\n'
		text2 += verb.strip() + ' PAST_PARTICIPLE\n'
		text3 += verb.strip() + ' PRESENT_PARTICIPLE\n'
	text1 += '\n'
	text2 += '\n'
	text3 += '\n'
	args = ["java", "-jar", "/export/tools/adorner-tools/VerbConjugator.jar"]
	conj = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
	(out, err) = conj.communicate(text1)
	data1 = out.strip().split('\n')
	
	conj = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
	(out, err) = conj.communicate(text2)
	data2 = out.strip().split('\n')

	conj = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
	(out, err) = conj.communicate(text3)
	data3 = out.strip().split('\n')
	
	print('len: ' + str(len(verbstems)))
	print('1: ' + str(len(data1)))
	print('2: ' + str(len(data2)))
	print('3: ' + str(len(data3)))
	return data1, data2, data3

def getSingulars(plurstems):
	text = ''
	for stem in plurstems:
		if len(stem.strip())==0:
			print('Problem!')
		text += stem.strip() + ' 1\n'
	text += '\n'
	args = ["java", "-jar", "/export/tools/adorner-tools/NounPlurarizer.jar"]
	plur = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
	(out, err) = plur.communicate(text)
	data = out.strip().split('\n')
	print('Singularizer len stems: ' + str(len(plurstems)) + ', Len data: ' + str(len(data)))
	return data

def getPlurals(singstems):
	text = ''
	for stem in singstems:
		text += stem.strip() + ' 2\n'
	text += '\n'
	args = ["java", "-jar", "/export/tools/adorner-tools/NounPlurarizer.jar"]
	plur = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
	(out, err) = plur.communicate(text)
	data = out.strip().split('\n')
	print('Plurarizer len stems: ' + str(len(singstems)) + ', Len data: ' + str(len(data)))
	return data

def getStems(sings, plurs, verbs):
	text = ''
	for sing in sings:
		text += sing +'\n'
	for plur in plurs:
		text += plur +'\n'
	for verb in verbs:
		text += verb +'\n'
	text += '\n'
	args = ["java", "-jar", "/export/tools/adorner-tools/WordLemmatizer.jar"]
	lemm = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
	(out, err) = lemm.communicate(text)
	data = out.strip().split('\n')
	rsings = []
	rplurs = []
	rverbs = []
	c = -1
	for sing in sings:
		c += 1
		if len(data[c])>0:
			rsings.append(data[c])
		else:
			rsings.append(sing)
	for plur in plurs:
		c += 1
		if len(data[c])>0:
			rplurs.append(data[c])
		else:
			rplurs.append(plur)
	for verb in verbs:
		c += 1
		if len(data[c])>0:
			rverbs.append(data[c])
		else:
			rverbs.append(verb)
	print('Sings: ' + str(len(sings)) + ', ' + str(len(rsings)))
	print('Plurs: ' + str(len(plurs)) + ', ' + str(len(rplurs)))
	print('Verbs: ' + str(len(verbs)) + ', ' + str(len(rverbs)))
	return rsings, rplurs, rverbs

def getAlignments(forward, inverse):
	af = forward.strip().split(' ')
	ai = inverse.strip().split(' ')
	af.extend(ai)
	a = set(af)
	return a

#Read stop words:
stop_words = set([])
fstop = open('../../../corpora/stop_words/stop_words.txt')
for word in fstop:
	stop_words.add(word.lower().strip())
fstop.close()

#Open input files:
posdata = open('../../../corpora/parsed/all.fastalign.pos.txt')
forward = open('../../../corpora/parsed/all.fastalign.forward.txt')
inverse = open('../../../corpora/parsed/all.fastalign.inverse.txt')

#Get substitutions:
print('Getting substitutions...')
c = 0
result = {}
for line in posdata:
#for i in range(0, 40000):
#	line = posdata.readline()
	c += 1
	print(str(c))
	data = line.strip().split('\t')
	source = data[0].strip().split(' ')
	target = data[1].strip().split(' ')
	
	fline = forward.readline().strip()
	iline = inverse.readline().strip()

	alignments = getAlignments(fline, iline)

	for alignment in alignments:
		adata = alignment.strip().split('-')
		left = int(adata[0].strip())
		right = int(adata[1].strip())
		leftraw = source[left].strip()
		leftp = leftraw.split('|||')[1].strip()
		leftw = leftraw.split('|||')[0].strip()
		rightraw = target[right].strip()
		rightp = rightraw.split('|||')[1].strip()
		rightw = rightraw.split('|||')[0].strip()

		if len(leftw)>0 and len(rightw)>0 and leftp!='nnp' and rightp!='nnp' and rightp==leftp and leftw not in stop_words and rightw not in stop_words and leftw!=rightw:
			if leftraw in result.keys():
				result[leftraw].add(rightw)
			else:
				result[leftraw] = set([rightw])	
posdata.close()
forward.close()
inverse.close()
print('Substitutions read!')

#Instantiate final substitutions:
final_substitutions = {}

#Get inflections:
allkeys = sorted(list(result.keys()))

singulars = {}
plurals = {}
verbs = {}

singularsk = {}
pluralsk = {}
verbsk = {}

for i in range(0, len(allkeys)):
	key = allkeys[i]
	keydata = key.split('|||')
	leftw = keydata[0].strip()
	leftp = keydata[1].strip()

	if leftp.startswith('n'):
		if leftp=='nns':
			pluralsk[leftw] = set([])
			for subst in result[key]:
				plurals[subst] = set([])
		else:
			singularsk[leftw] = set([])
			for subst in result[key]:
				singulars[subst] = set([])
	elif leftp.startswith('v'):
		verbsk[leftw] = {}
		for subst in result[key]:
			verbs[subst] = {}

#------------------------------------------------------------------------------------------------

#Generate keys input:
singkeys = sorted(list(singularsk.keys()))
plurkeys = sorted(list(pluralsk.keys()))
verbkeys = sorted(list(verbsk.keys()))

#Get stems:
singstems, plurstems, verbstems = getStems(singkeys, plurkeys, verbkeys)

#Get plurals:
singres = getPlurals(singstems)

#Get singulars:
plurres = getSingulars(plurstems)

#Get verb inflections:
verbres1, verbres2, verbres3 = getInflections(verbstems)

#Add information to dictionaries:
for i in range(0, len(singkeys)):
	k = singkeys[i]
	singre = singres[i]
	singularsk[k] = singre
for i in range(0, len(plurkeys)):
	k = plurkeys[i]
	plurre = plurres[i]
	pluralsk[k] = plurre
for i in range(0, len(verbkeys)):
	k = verbkeys[i]
	verbre1 = verbres1[i]
	verbre2 = verbres2[i]
	verbre3 = verbres3[i]
	verbsk[k] = {'PAST_PERFECT_PARTICIPLE': verbre1, 'PAST_PARTICIPLE': verbre2, 'PRESENT_PARTICIPLE': verbre3}

#------------------------------------------------------------------------------------------------

#Generate substs input:
singkeys = sorted(list(singulars.keys()))
plurkeys = sorted(list(plurals.keys()))
verbkeys = sorted(list(verbs.keys()))

#Get stems:
singstems, plurstems, verbstems = getStems(singkeys, plurkeys, verbkeys)

#Get plurals:
singres = getPlurals(singstems)

#Get singulars:
plurres = getSingulars(plurstems)

#Get verb inflections:
verbres1, verbres2, verbres3 = getInflections(verbstems)

#Add information to dictionaries:
for i in range(0, len(singkeys)):
	k = singkeys[i]
	singre = singres[i]
	singulars[k] = singre
for i in range(0, len(plurkeys)):
	k = plurkeys[i]
	plurre = plurres[i]
	plurals[k] = plurre
for i in range(0, len(verbkeys)):
	k = verbkeys[i]
	verbre1 = verbres1[i]
	verbre2 = verbres2[i]
	verbre3 = verbres3[i]
	verbs[k] = {'PAST_PERFECT_PARTICIPLE': verbre1, 'PAST_PARTICIPLE': verbre2, 'PRESENT_PARTICIPLE': verbre3}

#------------------------------------------------------------------------------------------------

#Generate final substitution list:
for i in range(0, len(allkeys)):
	print(str(i) + ' of ' + str(len(allkeys)))
	key = allkeys[i]
	keydata = key.split('|||')
	leftw = keydata[0].strip()
	leftp = keydata[1].strip()

	#Add final version to candidates:
	if leftw not in final_substitutions.keys():
		final_substitutions[leftw] = result[key]
	else:
		final_substitutions[leftw] = final_substitutions[leftw].union(result[key])

	#If left is a noun:
	if leftp.startswith('n'):
		#If it is a plural:
		if leftp=='nns':
			plurl = pluralsk[leftw]
			newcands = set([])
			for candidate in result[key]:
				candplurl = plurals[candidate]
				newcands.add(candplurl)
			if plurl not in final_substitutions.keys():
				final_substitutions[plurl] = newcands
			else:
				final_substitutions[plurl] = final_substitutions[plurl].union(newcands)
		#If it is singular:
		else:
			singl = singularsk[leftw]
			newcands = set([])
			for candidate in result[key]:
				candsingl = singulars[candidate]
				newcands.add(candsingl)
			if singl not in final_substitutions.keys():
				final_substitutions[singl] = newcands
			else:
				final_substitutions[singl] = final_substitutions[singl].union(newcands)
	#If left is a verb:
	elif leftp.startswith('v'):
		for verb_tense in ['PAST_PERFECT_PARTICIPLE', 'PAST_PARTICIPLE', 'PRESENT_PARTICIPLE']:
			tensedl = verbsk[leftw][verb_tense]
			newcands = set([])
			for candidate in result[key]:
				candtensedl = verbs[candidate][verb_tense]
				newcands.add(candtensedl)
			if tensedl not in final_substitutions.keys():
				final_substitutions[tensedl] = newcands
			else:
				final_substitutions[tensedl] = final_substitutions[tensedl].union(newcands)				


out = open('../../../corpora/substitutions/kauchak/final_substitutions.txt', 'w')
allkeys = sorted(list(final_substitutions.keys()))
for i in range(0, len(allkeys)):
	print(str(i))
	key = allkeys[i]
	newline = key + '\t'
	for subst in final_substitutions[key]:
		newline += subst + '|||'
	if newline.endswith('|||'):
		newline = newline[0:len(newline)-3]
	out.write(newline.strip() + '\n')
out.close()

print('Reached the end!')
