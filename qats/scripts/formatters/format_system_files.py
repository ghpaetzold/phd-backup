import os

def produceFormattedFile(name, input, output):
	f = open(input)
	o = open(output, 'w')
	o.write('metric-name\tsentence-number\tclass-value\tscore-value\n')
	c = 0
	for line in f:
		c += 1
		data = line.strip().split('\t')
		l = toLabel(data[0])
		r = data[1]
		newline = name + '\t' + str(c) + '\t' + l + '\t' + r + '\n'
		o.write(newline)
	f.close()
	o.close()

def toLabel(value):
	label = None
	if value=='0':
		label = 'bad'
	elif value=='1':
		label = 'ok'
	elif value=='2':
		label = 'good'
	else:
		print('Problem!')
	return label

types = os.listdir('../../finallabels/')

names = {}
names['nn_adadelta_final'] = 'SimpleNets-RNN'
names['nn_mlp_final'] = 'SimpleNets-MLP'

for type in types:
	os.system('mkdir ../../finalsystemfiles/'+type)
	path = '../../finallabels/'+type
	for system in os.listdir(path):
		files = os.listdir(path+'/'+system)
		for file in files:
			if 'nn_mlp_final'==system:
				filename = '../../finalsystemfiles/'+type+'/SimpleNets-MLP.txt'
				produceFormattedFile(names[system], path+'/'+system+'/'+file, filename)
			else:
				ngram = file[len(file)-5]
				filename = '../../finalsystemfiles/'+type+'/SimpleNets-RNN'+ngram+'.txt'
				produceFormattedFile('SimpleNets-RNN'+ngram, path+'/'+system+'/'+file, filename)
