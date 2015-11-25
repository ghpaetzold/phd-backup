import os

#Parameters:
positive_ranges = ['1', '2', '3']
folds = ['10']
test_sizes = ['0.25']

generators = os.listdir('../../substitutions/')
#generators = ['all']

best_map = {}
f = open('../evaluators/best_ss.txt')
for line in f:
	data = line.strip().split('\t')
	gen = data[0].strip()
	sel = data[1].strip()
	file = data[2].strip()
	if gen not in best_map:
		best_map[gen] = {}
	best_map[gen][sel] = file
f.close()

datasets = {}
datasets['semeval'] = '../../../semeval/corpora/semeval/semeval_all.txt'
datasets['nnsimplex'] = '../../../sr_userstudy/corpora/NNSimpLex.txt'
datasets['lexmturk'] = '../../../lexmturk/corpora/lexmturk_all.txt'
datasets['debelder'] = '../../../../dataset_benchmarking/DeBelder_VICTOR_inflected.txt'

for generator in generators:
	selectors = best_map[generator].keys()
        selectors = ['void']
        for selector in selectors:
		for p in positive_ranges:
			for f in folds:
				for t in test_sizes:
					for dataset in datasets:
						os.system('mkdir ../../dt_rankings/'+dataset)
						os.system('mkdir ../../dt_rankings/'+dataset+'/boundaryCV')
						output = '../../dt_rankings/'+dataset+'/boundaryCV/ranks_'+generator+'_'+selector+'_'+p+'_'+f+'_'+t+'.txt'
						comm = 'nohup python Run_BoundaryCV.py '+datasets[dataset]+' '+p+' '+f+' '+t
						comm += ' ../../substitutions/'+generator+'/'+best_map[generator][selector]+' '+output+' &'
						os.system(comm)
