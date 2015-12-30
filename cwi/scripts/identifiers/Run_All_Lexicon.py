import os

trainset = '../../corpora/cwi_paetzold_training.txt'
testset = '../../corpora/cwi_paetzold_testing.txt'

lexicons = []
lexicons.append(('../../../lexmturk/corpora/wikisimple.vocab.txt', 'simple'))
lexicons.append(('../../../lexmturk/corpora/wiki.vocab.txt', 'complex'))
lexicons.append(('../../../lexmturk/corpora/stop_words.txt', 'simple'))
lexicons.append(('../../../lexmturk/corpora/basic_words.txt', 'simple'))
lexicons.append(('../../../lexmturk/corpora/subimdb.vocab.txt', 'simple'))

labels = []
labels.append('SimpleWikipedia')
labels.append('Wikipedia')
labels.append('Stop')
labels.append('Ogdens')
labels.append('SubIMDB')

for i in range(0, len(lexicons)):
	lexicon = lexicons[i]
	label = labels[i]
	os.system('mkdir ../../labels/lex_'+label)
	output = '../../labels/lex_'+label+'/labels.txt'
	comm = 'nohup python Run_Lexicon.py '+testset+' '+trainset+' '+lexicon[0]+' '+lexicon[1]+' '+output+' &'
	os.system(comm)
