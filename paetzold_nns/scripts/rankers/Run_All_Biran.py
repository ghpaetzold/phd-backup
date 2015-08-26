import os

trainset = '../../corpora/paetzold_nns_dataset.txt'
testset = '../../corpora/paetzold_nns_dataset.txt'

generators = os.listdir('../../substitutions/')
generators = ['biran']

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
		testset = '../../substitutions/'+generator+'/'+best_map[generator][selector]		
		output = '../../rankings/biran/ranks_'+generator+'_'+selector+'.txt'
		clm = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/wiki.5gram.bin.txt'
		slm = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/simplewiki.5.bin.txt'
		comm = 'nohup python Run_Biran.py '+trainset+' '+clm+' '+slm+' '+testset+' '+output+' &'
		os.system(comm)
