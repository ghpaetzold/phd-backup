import os

trainset = '../../corpora/paetzold_nns_dataset.txt'
testset = '../../corpora/paetzold_nns_dataset.txt'

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

#Parameters:
alphas = ['1']

for gen in best_map:
        best_map[gen]['void'] = 'substitutions_void.txt'

for generator in generators:
        selectors = best_map[generator].keys()
        #selectors = ['void']
        for selector in selectors:
		testset = '../../substitutions/'+generator+'/'+best_map[generator][selector]
		for a1 in alphas:
			for a2 in alphas:
				output = '../../rankings/bott/ranks_'+generator+'_'+selector+'_'+a1+'_'+a2+'.txt'
				lm = '/export/data/ghpaetzold/machinelearningranking/corpora/lm/simplewiki.5gram.bin.txt'
				comm = 'nohup python Run_Bott.py '+trainset+' '+lm+' '+a1+' '+a2+' '+testset+' '+output+' &'
				os.system(comm)
