import os

#Features: 21
flabels = []
#flabels.append('lexicon_basic')
#flabels.append('lexicon_wikisimple')
flabels.append('length')
#flabels.append('syllable')
#flabels.append('colloc00')
#flabels.append('colloc01')
#flabels.append('colloc02')
#flabels.append('colloc10')
flabels.append('colloc11')
flabels.append('colloc12')
flabels.append('colloc20')
flabels.append('colloc21')
flabels.append('colloc22')
flabels.append('sent_prob')
flabels.append('senses')
flabels.append('synonyms')
flabels.append('hypernyms')
flabels.append('hyponyms')
flabels.append('mindepth')
flabels.append('maxdepth')

flabels = ['length', 'brownfreq', 'senses', 'synonyms', 'hypernyms', 'hyponyms']

generators = os.listdir('../../substitutions/')
#generators = ['biran', 'kauchak', 'wordnet', 'yamamoto', 'glavas', 'glavasretrofitted', 'paetzold', 'paetzoldretrofitted']
#generators = ['glavasretrofitted', 'paetzoldretrofitted']
generators = ['wordnet']

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
		for i in range(0, len(flabels)):
			os.system('mkdir ../../rankings/'+flabels[i])
			output = '../../rankings/'+flabels[i]+'/ranks_'+generator+'_'+selector+'.txt'
			comm = 'nohup python Run_Metric.py ../../substitutions/'+generator+'/'+best_map[generator][selector]+' '+str(i)+' '+output+' &'
			os.system(comm)
