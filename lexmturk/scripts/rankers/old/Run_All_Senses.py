import os

trainset = '../../substitutions/all/substitutions_wordvector_0.125_HasStop_0_True_True_True.txt'
trainset = '../../substitutions/all/substitutions_void.txt'
#trainset = '../../substitutions/all/substitutions_biran_0.0_0.8.txt'
output = '../../rankings/senses/ranks_void.txt'
comm = 'nohup python Run_Senses.py '+trainset+' '+output+' &'
os.system(comm)
