import os

valids = ['ssuserstudy', 'lexmturk', 'nnseval', 'all']
#valids = ['ssuserstudy']

for valid in valids:
	os.system('mkdir ../../../rankings/rnnlm'+valid+'/')
	comm = 'nohup python run_rnnlm.py '+valid+' &'
	os.system(comm)
