import os

#Parameters:
losses = ['hinge', 'modified_huber']
penalties = ['l2', 'l1', 'elasticnet']
alphas = ['0.001', '0.01', '0.1']
l1ratios = ['0.01', '0.10', '0.15']
epsilons = ['0.0001', '0.001']

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
	for selector in best_map[generator]:
		for l in losses:
			for p in penalties:
				for a in alphas:
					for r in l1ratios:
						for e in epsilons:
							output = '../../rankings/boundary/ranks_'+generator+'_'+selector+'_'+l+'_'+p+'_'+a+'_'+r+'_'+e+'.txt'
							comm = 'nohup python Run_Boundary.py ../../corpora/lexmturk_all.txt 1 '+l+' '+p+' '+a+' '+r+' '+e
							comm += ' ../../substitutions/'+generator+'/'+best_map[generator][selector]+' '+output+' &'
							os.system(comm)
