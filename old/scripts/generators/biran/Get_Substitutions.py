import urllib2 as urllib
from nltk.corpus import wordnet as wn
import subprocess
import nltk
import kenlm

def getComplexity(word, clm, slm):
	C = (clm.score(word, bos=False, eos=False))/(slm.score(word, bos=False, eos=False))
	L = float(len(word))
	return C*L

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

	result = {}
        for i in range(0, len(verbstems)):
                result[verbstems[i]] = {'PAST_PERFECT_PARTICIPLE': data1[i], 'PAST_PARTICIPLE': data2[i], 'PRESENT_PARTICIPLE': data3[i]}
        return result

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
	result = {}
	for i in range(0, len(plurstems)):
		result[plurstems[i]] = data[i]
        return result

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
	result = {}
        for i in range(0, len(singstems)):
                result[singstems[i]] = data[i]
        return result

def getStems(sings):
        text = ''
        for sing in sings:
                text += sing +'\n'
        text += '\n'
        args = ["java", "-jar", "/export/tools/adorner-tools/WordLemmatizer.jar"]
        lemm = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        (out, err) = lemm.communicate(text)
        data = out.strip().split('\n')
	result = {}
	for i in range(0, len(data)):
		stem = data[i]
		sing = sings[i]
		if len(stem.strip())>0:
			result[sing] = stem.strip()
		else:
			result[sing] = sing
        return result

def cleanLemma(lem):
	result = ''
	aux = lem.strip().split('_')
	for word in aux:
		result += word + ' '
	return result.strip()

def getPOSMap(path):
	result = {}
	lex = open(path)
	for line in lex:
		data = line.strip().split('\t')
		sent = data[0].strip().lower().split(' ')

		target = data[1].strip().lower()
		posd = nltk.pos_tag(sent)
		for token in posd:
			if token[0].lower()==target:
				if target in result.keys():
					result[target] = 'v'
				else:
					result[target] = token[1].lower().strip()
	print('len: ' + str(len(result.keys())))
	lex.close()
	return result

def getVocab(path):
	return set([line.strip() for line in open(path)])

#Open input:
lex = open('../../../corpora/lexmturk/lexmturk.txt')
out = open('../../../corpora/substitutions/biran/substitutions.txt', 'w')

target_pos = getPOSMap('../../../corpora/lexmturk/lexmturk.txt')

vocabc = getVocab('../../../corpora/vocab/wiki.vocab.txt')
vocabs = getVocab('../../../corpora/vocab/wikisimple.vocab.txt')

#Get initial set of substitutions:
substitutions_initial = {}
for line in lex:
	data = line.strip().split('\t')
	target = data[1].strip()
	if target in vocabc:
		syns = wn.synsets(target)
		newline = target + '\t'
		cands = set([])
		for syn in syns:
			for lem in syn.lemmas():
				candidate = cleanLemma(lem.name())
				if len(candidate.split(' '))==1 and candidate in vocabs:
					cands.add(candidate)
			for hyp in syn.hypernyms():
				for lem in hyp.lemmas():
					candidate = cleanLemma(lem.name())
					if len(candidate.split(' '))==1 and candidate in vocabs:
						cands.add(candidate)
		substitutions_initial[target] = cands
lex.close()

#Create second set of filtered substitutions:
substitutions_stemmed = {}

keys = sorted(list(substitutions_initial.keys()))
nounverbs = []
cands = set([])
for key in keys:
	if target_pos[key].startswith('v') or target_pos[key].startswith('n'):
		nounverbs.append(key)
		for cand in substitutions_initial[key]:
			cands.add(cand)
cands = sorted(list(cands))

stemk = getStems(nounverbs)
stemc = getStems(cands)

#Create third set of filtered substitutions:
substitutions_inflected = {}

singularsk = []
pluralsk = []
verbsk = []

singulars = []
plurals = []
verbs = []

for key in keys:
	poskey = target_pos[key]
	if poskey.startswith('n'):
		singularsk.append(stemk[key])
		for cand in substitutions_initial[key]:
			singulars.append(stemc[cand])
		pluralsk.append(stemk[key])
		for cand in substitutions_initial[key]:
			plurals.append(stemc[cand])
	elif poskey.startswith('v'):
		verbsk.append(stemk[key])
		for candn in substitutions_initial[key]:
			verbs.append(stemc[candn])

singularskr = getPlurals(singularsk)
pluralskr = getSingulars(pluralsk)
verbskr = getInflections(verbsk)

singularsr = getPlurals(singulars)
pluralsr = getSingulars(plurals)
verbsr = getInflections(verbs)

for key in keys:
        poskey = target_pos[key]
        if poskey.startswith('n'):
		substitutions_inflected[singularskr[stemk[key]]] = set([])
		substitutions_inflected[pluralskr[stemk[key]]] = set([])
                for cand in substitutions_initial[key]:
			substitutions_inflected[singularskr[stemk[key]]].add(singularsr[stemc[cand]])
                        substitutions_inflected[pluralskr[stemk[key]]].add(pluralsr[stemc[cand]])
        elif poskey.startswith('v'):
                substitutions_inflected[verbskr[stemk[key]]['PAST_PERFECT_PARTICIPLE']] = set([])
		substitutions_inflected[verbskr[stemk[key]]['PAST_PARTICIPLE']] = set([])
		substitutions_inflected[verbskr[stemk[key]]['PRESENT_PARTICIPLE']] = set([])
                for candn in substitutions_initial[key]:
                        substitutions_inflected[verbskr[stemk[key]]['PAST_PERFECT_PARTICIPLE']].add(verbsr[stemc[candn]]['PAST_PERFECT_PARTICIPLE'])
			substitutions_inflected[verbskr[stemk[key]]['PAST_PARTICIPLE']].add(verbsr[stemc[candn]]['PAST_PARTICIPLE'])
			substitutions_inflected[verbskr[stemk[key]]['PRESENT_PARTICIPLE']].add(verbsr[stemc[candn]]['PRESENT_PARTICIPLE'])

#Remove simple->complex substitutions:
substitutions_final = {}

clm = kenlm.LanguageModel('../../../corpora/lm/wiki.5.bin.txt')
slm = kenlm.LanguageModel('../../../corpora/lm/simplewiki.5.bin.txt')

for key in substitutions_inflected.keys():
	substitutions_final[key] = set([])
	key_score = getComplexity(key, clm, slm)
	for cand in substitutions_inflected[key]:
		cand_score = getComplexity(cand, clm, slm)
		if key_score>=cand_score:
			substitutions_final[key].add(cand)

#Save final substitutions:
for key in substitutions_final.keys():
	if len(substitutions_final[key])>0:
		newline = key + '\t'
		for cand in substitutions_final[key]:
			newline += cand + '|||'
		if newline.endswith('|||'):
			newline = newline[0:len(newline)-3]
		out.write(newline.strip() + '\n')
out.close()
