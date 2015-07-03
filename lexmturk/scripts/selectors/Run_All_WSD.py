import os

generators = os.listdir('../../substitutions/')
#generators = ['kauchak']
#generators = ['biran']
#generators = ['merriam']
#generators = ['wordnet']
#generators = ['yamamoto']
generators = ['all']
#generators = ['paetzold']
victor_corpus = '../../corpora/lexmturk_all.txt'

#Run WSD selector:
methods = ['lesk', 'leacho', 'path', 'wupalmer', 'random', 'first']
for generator in generators:
	for method in methods:
		out = '../../substitutions/'+generator+'/'
		out += 'substitutions_WSD_'+method+'.txt'
		comm = 'nohup python Run_WSD.py '+generator+' '+victor_corpus+' '+method+' '+out+' &'
		os.system(comm)
