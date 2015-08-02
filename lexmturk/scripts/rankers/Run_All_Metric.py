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

flabels = ['colloc00', 'senses', 'synonyms', 'hypernyms', 'hyponyms']
flabels = ['length']

generators = os.listdir('../../substitutions/')
#generators = ['merriam', 'wordnet', 'yamamoto']

testsets = []
#testsets.append('substitutions_svmrank_0.125_1_1_0.0001.txt')
#testsets.append('substitutions_boundaryCV_0.5.txt')
#testsets.append('substitutions_WSD_enhancedlesk.txt')
#testsets.append('substitutions_wordvector_0.125_HasStop_0_True_True_True.txt')
#testsets.append('substitutions_void.txt')
testsets.append('substitutions_biran_0.0_0.8.txt')
testsets.append('substitutions_WSD_first.txt')
testsets.append('substitutions_WSD_lesk.txt')
testsets.append('substitutions_WSD_path.txt')
testsets.append('substitutions_WSD_random.txt')
testsets.append('substitutions_clusters.txt')

for generator in generators:
        print(generator)
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
