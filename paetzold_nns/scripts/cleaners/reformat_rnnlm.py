import os

types = ['all', 'lexmturk', 'nnseval', 'ssuserstudy']

for type in types:
	os.system('mkdir ../../rankings/rnnlm'+type)

files = os.listdir('../../rankings/rnnlm/')
for file in files:
	data = file[0:len(file)-4].split('_')
	newfile = data[0]+'_'+data[1]+'_'+data[2]+'.txt'
	comm = 'mv ../../rankings/rnnlm/'+file + ' ../../rankings/rnnlm'+data[3]+'/'+newfile
	print(str(comm))
	os.system(comm)
