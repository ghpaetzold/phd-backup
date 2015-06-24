import os

generators = os.listdir('../../substitutions/')
#generators = ['kauchak']
#generators = ['biran']
#generators = ['merriam']
#generators = ['wordnet']
#generators = ['yamamoto']
generators = ['all']
victor_corpus = '../../corpora/lexmturk_all.txt'

stopWordVec = False
stopBiran = False


#Run WordVec selector:
proportions = ['0.125', '0.5']
stopwordsfiles = ['../../corpora/stop_words.txt']
windows = ['1', '0']
informatives = ['True']
targets = ['True']
ones = ['True']
for generator in generators:
	for proportion in proportions:
		for stop in stopwordsfiles:
			for window in windows:
				for informative in informatives:
					for target in targets:
						for one in ones:
							if not stopWordVec:
								hasstop = 'HasStop'
								if stop == 'None':
									hasstop = 'NoStop'
								out = '../../substitutions/'+generator+'/'
								out += 'substitutions_wordvector_'+proportion+'_'+hasstop+'_'+window+'_'+informative+'_'+target+'_'+one+'.txt'
								comm = 'nohup python Run_WordVector.py ' + generator + ' ' + victor_corpus + ' ' + proportion + ' '
								comm += stop + ' ' + window + ' ' + informative + ' ' + target + ' ' + one + ' ' + out + ' &'
								os.system(comm)
								#print(comm)

#Run Biran selector:
commonds = ['0.0', '0.1']
candidateds = ['0.8', '0.9']
for generator in generators:
	for commond in commonds:
		for candidated in candidateds:
			if not stopBiran:
				out = '../../substitutions/'+generator+'/'
				out += 'substitutions_biran_'+commond+'_'+candidated+'.txt'
				cooc_model = '../../corpora/vectors.clean.txt'
				comm = 'nohup python Run_Biran.py '+generator+' '+victor_corpus+' '+cooc_model+' '+commond+' '+candidated+' '+out+' &'
				os.system(comm)

#Run WSD selector:
methods = ['lesk', 'leacho', 'path', 'wupalmer', 'random', 'first']
for generator in generators:
	for method in methods:
		out = '../../substitutions/'+generator+'/'
		out += 'substitutions_WSD_'+method+'.txt'
		comm = 'nohup python Run_WSD.py '+generator+' '+victor_corpus+' '+method+' '+out+' &'
		os.system(comm)
