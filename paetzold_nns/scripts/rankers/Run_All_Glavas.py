import os

generators = os.listdir('../../substitutions/')
generators = ['allvocab']

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

for gen in best_map:
        best_map[gen]['void'] = 'substitutions_void.txt'

os.system('mkdir ../../rankings/glavas')

for generator in generators:
	selectors = best_map[generator].keys()
        #selectors = ['void']
        for selector in selectors:
		trainset = 'placeholder'
		testset = '../../substitutions/'+generator+'/'+best_map[generator][selector]
		output = '../../rankings/glavas/ranks_'+generator+'_'+selector+'.txt'
		comm = 'nohup python Run_Glavas.py '+trainset+' '+testset+' '+output+' &'
		os.system(comm)
