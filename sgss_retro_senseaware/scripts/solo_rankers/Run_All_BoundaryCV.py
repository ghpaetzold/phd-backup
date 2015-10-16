import os

#Parameters:
positive_ranges = ['3']
folds = ['5']
test_sizes = ['0.25']
types = ['TEM', 'REM', 'SEM', 'RSEM']
#sizes = ['500']
#sizes = ['700', '900', '1100', '1300', '1500']
sizes = ['2300', '2500']
#archs = ['cbow', 'skip']
archs = ['cbow']

for p in positive_ranges:
	for f in folds:
		for t in test_sizes:
			for type in types:
				for arch in archs:
					for size in sizes:
						os.system('mkdir ../../solo_rankings/boundary/')
						os.system('mkdir ../../solo_rankings/boundary/' + type)
						os.system('mkdir ../../solo_rankings/boundary/' + type + '/' + arch)
						os.system('mkdir ../../solo_rankings/boundary/' + type + '/' + arch + '/' + size)
						output = '../../solo_rankings/boundary/' + type + '/' + arch + '/' + size + '/ranks_'+p+'_'+f+'_'+t+'.txt'
						comm = 'nohup python Run_BoundaryCV.py /export/data/ghpaetzold/benchmarking/semeval/corpora/semeval/semeval_train_clean.txt '
						comm += p+' '+f+' '+t+ ' /export/data/ghpaetzold/benchmarking/semeval/corpora/semeval/semeval_test_clean.txt '+output+' '
						comm += type + ' ' + size + ' ' + arch + ' &'
						os.system(comm)
