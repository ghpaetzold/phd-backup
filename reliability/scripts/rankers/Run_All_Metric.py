import os

flabels = []
flabels.append('length')
flabels.append('syllable')
flabels.append('subimdb00')
flabels.append('subtlex00')
flabels.append('simplewiki00')
flabels.append('wiki00')
flabels.append('brown00')
flabels.append('senses')
flabels.append('synonyms')
flabels.append('hypernyms')
flabels.append('hyponyms')
flabels.append('mindepth')
flabels.append('maxdepth')

generators = os.listdir('../../substitutions/')
generators = ['all']

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