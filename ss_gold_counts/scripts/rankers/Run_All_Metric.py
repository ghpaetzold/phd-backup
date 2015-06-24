import os

#Features: 21
flabels = []
flabels.append('lexicon_basic')
flabels.append('lexicon_wikisimple')
flabels.append('length')
flabels.append('syllable')
flabels.append('colloc00')
flabels.append('colloc01')
flabels.append('colloc02')
flabels.append('colloc10')
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

generators = os.listdir('../../substitutions/')

testsetmap = {}
f = open('../evaluators/best_ss.txt')
for line in f:
        data = line.strip().split('\t')
        generator = data[0].strip()
        testsets = data[1:len(data)]
        testsetmap[generator] = testsets
f.close()

for generator in generators:
        print(generator)
	testsets = testsetmap[generator]
        for testset in testsets:
                testsetd = testset.strip().split('_')
                selector = testsetd[1].strip()
                if selector == 'WSD':
                        selector = testsetd[2].strip()
		for i in range(0, len(flabels)):
			os.system('mkdir ../../rankings/'+flabels[i])
			output = '../../rankings/'+flabels[i]+'/ranks_'+generator+'_'+selector+'.txt'
			comm = 'nohup python Run_Metric.py ../../substitutions/'+generator+'/'+testset+' '+str(i)+' '+output+' &'
			os.system(comm)
