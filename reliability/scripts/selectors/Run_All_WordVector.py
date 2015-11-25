import os

generators = os.listdir('../../substitutions/')
victor_corpus = '../../corpora/paetzold_nns_dataset.txt'

#Run WordVec selector:
proportions = ['0.5']
stopwordsfiles = ['../../../lexmturk/corpora/stop_words.txt']
windows = ['2']
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
							out = '../../substitutions/'+generator+'/'
							out += 'substitutions_wordvector_'+proportion+'_'+hasstop+'_0_'+informative+'_'+target+'_'+one+'.txt'
							comm = 'nohup python Run_WordVector.py ' + generator + ' ' + victor_corpus + ' ' + proportion + ' '
							comm += stop + ' ' + window + ' ' + informative + ' ' + target + ' ' + one + ' ' + out + ' &'
							os.system(comm)
