import os, sys

model = sys.argv[1]
pos_type = sys.argv[2]
retrofitted = sys.argv[3]

#Create prefix:
prefix = 'wv'
if pos_type=='none':
	if retrofitted=='1':
		prefix += 'REM'
	else:
		prefix += 'TEM'
elif pos_type=='paetzold':
	if retrofitted=='1':
		prefix += 'RSEM'
	else:
		prefix += 'SEM'

#Generators:
generators = os.listdir('../../substitutions/')
generators = ['glavas1300', 'glavas_retrofitted1300', 'paetzold1300', 'paetzold_retrofitted1300']

#Dataset:
victor_corpus = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt'

#Run WordVec selector:
proportions = ['0.75']
stopwordsfiles = ['../../../lexmturk/corpora/stop_words.txt']
windows = ['0']
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
							hasstop = 'HasStop'
							if stop == 'None':
								hasstop = 'NoStop'
							out = '../../substitutions/'+generator+'/substitutions_'+prefix
							out += '_'+proportion+'_'+hasstop+'_0_'+informative+'_'+target+'_'+one+'.txt'
							comm = 'nohup python Run_WordVector.py ' + generator + ' ' + victor_corpus + ' ' + proportion + ' '
							comm += stop + ' ' + window + ' ' + informative + ' ' + target + ' ' + one + ' ' + out + ' '
							comm += model + ' ' + pos_type + ' &'
							os.system(comm)
