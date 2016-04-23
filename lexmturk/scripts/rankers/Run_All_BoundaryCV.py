import os

#Parameters:
positive_ranges = ['1', '2', '3']
folds = ['5', '10']
test_sizes = ['0.25', '0.5', '0.75']

generators = os.listdir('../../substitutions/')
generators = ['paetzold']

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
#	for selector in best_map[generator]:
	for selector in ['boundaryUnsupervisedCV']:
		for p in positive_ranges:
			for f in folds:
				for t in test_sizes:
					output = '../../rankings/boundaryCV/ranks_'+generator+'_'+selector+'_'+p+'_'+f+'_'+t+'.txt'
					comm = 'nohup python Run_BoundaryCV.py ../../corpora/lexmturk_all.txt '+p+' '+f+' '+t
					comm += ' ../../substitutions/'+generator+'/'+best_map[generator][selector]+' '+output+' &'
					os.system(comm)
