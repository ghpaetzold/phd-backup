import os

#Parameters:
positive_ranges = ['3']
folds = ['10']
test_sizes = ['0.75']
ks = ['all']

generators = os.listdir('../../substitutions/')
#generators = ['paetzold']

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

for generator in generators:
	selectors = best_map[generator].keys()
        #selectors = ['wordvector']
        for selector in selectors:
		for p in positive_ranges:
			for f in folds:
				for t in test_sizes:
					for k in ks:
						output = '../../rankings/boundaryCV/ranks_'+generator+'_'+selector+'_'+p+'_'+f+'_'+t+'_'+k+'.txt'
						comm = 'nohup python Run_BoundaryCV.py ../../corpora/ls_dataset_benchmarking.txt '+p+' '+f+' '+t
						comm += ' ../../substitutions/'+generator+'/'+best_map[generator][selector]+' '+output+' '+k+' &'
						os.system(comm)
