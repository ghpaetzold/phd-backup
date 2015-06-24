import os

generators = os.listdir('../../substitutions/')
victor_corpus = '../../corpora/lexmturk_gold.txt'

#Run Biran selector:
commonds = ['0.0', '0.1']
candidateds = ['0.8', '0.9']
for generator in generators:
	for commond in commonds:
		for candidated in candidateds:
			out = '../../substitutions/'+generator+'/'
			out += 'substitutions_biran_'+commond+'_'+candidated+'.txt'
			cooc_model = '../../../lexmturk/corpora/vectors.clean.txt'
			comm = 'nohup python Run_Biran.py '+generator+' '+victor_corpus+' '+cooc_model+' '+commond+' '+candidated+' '+out+' &'
			os.system(comm)
