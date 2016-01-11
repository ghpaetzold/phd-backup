import os

flabels = ['paetzoldaaai']

generators = os.listdir('../../substitutions/')
#generators = ['biran', 'kauchak', 'wordnet', 'yamamoto', 'glavas', 'glavasretrofitted', 'paetzold', 'paetzoldretrofitted']
#generators = ['glavasretrofitted', 'paetzoldretrofitted']
generators = ['paetzoldretrofitted']

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
		os.system('mkdir ../../rankings/paetzoldaaai')
		output = '../../rankings/paetzoldaaai/ranks_'+generator+'_'+selector+'.txt'
		comm = 'nohup python Run_PaetzoldAAAI.py ../../substitutions/'+generator+'/'+best_map[generator][selector]+' '+output+' &'
		os.system(comm)
