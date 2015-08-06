import os

generators = ['all']
#generators = os.listdir('/export/data/ghpaetzold/benchmarking/ss_userstudy/substitutions/')
#generators.remove('all')

#Features: 21
flabels = []
flabels.append('colloc00')
flabels.append('colloc01')
flabels.append('colloc10')
flabels.append('colloc11')
flabels.append('colloc00tb')
flabels.append('colloc01tb')
flabels.append('colloc10tb')
flabels.append('colloc11tb')
flabels.append('colloc00pa')
flabels.append('colloc01pa')
flabels.append('colloc10pa')
flabels.append('colloc11pa')
flabels.append('postagprob')

for i in range(0, len(flabels)):
	for j in range(1, 6):
		for generator in generators:
			trainset = '/export/data/ghpaetzold/benchmarking/ss_userstudy/corpora/grammaticality_victor_training_'
			trainset += str(j) + '.txt'
			testset = '/export/data/ghpaetzold/benchmarking/ss_userstudy/substitutions/'
			testset += generator + '/substitutions_void.txt'
			output = '/export/data/ghpaetzold/benchmarking/ss_userstudy/substitutions/' + generator + '/'
			output += 'substitutions_'+flabels[i]+'Grammaticality_'+str(j)+'.txt'
			comm = 'nohup python Run_Threshold.py '+trainset+' '+testset+' '+str(i)+' '+output+' &'
			os.system(comm)
