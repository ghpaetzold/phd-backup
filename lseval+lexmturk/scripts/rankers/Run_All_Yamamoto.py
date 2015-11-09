import os

#Parameters:
alphas = ['1']

trainset = '../../corpora/ls_dataset_benchmarking.txt'
testset = '../../corpora/ls_dataset_benchmarking.txt'

generators = os.listdir('../../substitutions/')
#generators = ['yamamoto']

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
#        selectors = ['void']
        for selector in selectors:
		testset = '../../substitutions/'+generator+'/'+best_map[generator][selector]
		output = '../../rankings/yamamoto/ranks_'+generator+'_'+selector+'_1_1_1_1_1.txt'
		lm = '/export/data/ghpaetzold/machinelearningranking/corpora/lm/simplewiki.5gram.bin.txt'
		cooc = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/vectors.clean.txt'
		comm = 'nohup python Run_Yamamoto.py '+trainset+' '+lm+' '+cooc+' 1 1 1 1 1 '+testset+' '+output+' &'
		os.system(comm)
