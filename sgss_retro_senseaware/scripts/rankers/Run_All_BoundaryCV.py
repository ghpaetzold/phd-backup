import os

#Parameters:
positive_ranges = ['2', '3']
folds = ['5']
test_sizes = ['0.25']
types = ['TEM', 'REM', 'SEM', 'RSEM']
size = '500'
archs = ['cbow']
foldermap = {}
foldermap['TEM'] = 'glavas1300'
foldermap['REM'] = 'glavas_retrofitted1300'
foldermap['SEM'] = 'paetzold1300'
foldermap['RSEM'] = 'paetzold_retrofitted1300'
for p in positive_ranges:
	for f in folds:
		for t in test_sizes:
			for type in types:
				for arch in archs:
					os.system('mkdir ../../rankings/boundary/')
					os.system('mkdir ../../rankings/boundary/' + type)
					#os.system('mkdir ../../rankings/boundary/' + type + '/' + arch)
					#os.system('mkdir ../../rankings/boundary/' + type + '/' + arch + '/' + size)
					output = '../../rankings/boundary/' + type + '/ranks_'+p+'_'+f+'_'+t+'.txt'
					comm = 'nohup python Run_BoundaryCV.py /export/data/ghpaetzold/benchmarking/lexmturk/corpora/lexmturk_all.txt '
					comm += p+' '+f+' '+t
					comm += ' ../../substitutions/'+foldermap[type]+'/substitutions_wv'+type+'_0.75_HasStop_0_True_True_True.txt '
					comm += output+' '
					comm += type + ' ' + size + ' ' + arch + ' &'
					os.system(comm)
