import os

trainset = '../../corpora/cwi_paetzold_training_majority.txt'
testset = '../../corpora/cwi_paetzold_testing.txt'

lexicons = []
lexicons.append(('../../../lexmturk/corpora/wikisimple.vocab.txt', 'simple'))
lexicons.append(('../../../lexmturk/corpora/wiki.vocab.txt', 'complex'))
lexicons.append(('../../../lexmturk/corpora/stop_words.txt', 'simple'))
lexicons.append(('../../../lexmturk/corpora/basic_words.txt', 'simple'))
lexicons.append(('../../../lexmturk/corpora/subimdb.vocab.txt', 'simple'))

labels = []
labels.append('Lex:Simple_Wikipedia')
labels.append('Lex:Wikipedia')
labels.append('Lex:Stop_Words')
labels.append('Lex:Ogdens_Words')
labels.append('Lex:SubIMDB')

for i in range(0, len(lexicons)):
	lexicon = lexicons[i]
	label = labels[i]
	output = '../../labels_majority/lexicon/labels_'+label+'.txt'
	comm = 'nohup python Run_Lexicon.py '+testset+' '+trainset+' '+lexicon[0]+' '+lexicon[1]+' '+output+' &'
	os.system(comm)
