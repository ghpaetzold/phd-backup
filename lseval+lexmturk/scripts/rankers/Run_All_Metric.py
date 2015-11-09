import os

flabels = []
flabels.append('devlin')
flabels.append('subimdb')

generators = os.listdir('../../substitutions/')
#generators = ['wordnet']

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
	#selectors = ['void']
        for selector in selectors:
		for i in range(0, len(flabels)):
			os.system('mkdir ../../rankings/'+flabels[i])
			output = '../../rankings/'+flabels[i]+'/ranks_'+generator+'_'+selector+'.txt'
			comm = 'nohup python Run_Metric.py ../../substitutions/'+generator+'/'+best_map[generator][selector]+' '+str(i)+' '+output+' &'
			os.system(comm)
