import os

valids = ['ssuserstudy', 'lexmturk', 'nnseval', 'all']
for valid in valids:
	comm = 'nohup /export/tools/rnnlm/rnnlm -train ../../../corpora/rnnlm_training_corpus.txt '
	comm += '-valid ../../../corpora/'+valid+'_valid.txt '
	comm += '-rnnlm ../../../corpora/rnnlm_models/5kk_'+valid+'_model.txt -hidden 50 -rand-seed 1 -debug 2 -bptt 3 -class 200 &'
	os.system(comm)
