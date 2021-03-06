import os

trainset = '../../corpora/ls_dataset_benchmarking.txt'
testset = '../../corpora/ls_dataset_benchmarking.txt'

generators = os.listdir('../../substitutions/')
#generators = ['biran']

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

os.system('mkdir ../../rankings/biran')

for generator in generators:
	selectors = best_map[generator].keys()
        #selectors = ['biran']
        for selector in selectors:
		testset = '../../substitutions/'+generator+'/'+best_map[generator][selector]		
		output = '../../rankings/biran/ranks_'+generator+'_'+selector+'.txt'
		clm = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/wiki.5gram.bin.txt'
		slm = '/export/data/ghpaetzold/benchmarking/lexmturk/corpora/simplewiki.5.bin.txt'
		comm = 'nohup python Run_Biran.py '+trainset+' '+clm+' '+slm+' '+testset+' '+output+' &'
		os.system(comm)
