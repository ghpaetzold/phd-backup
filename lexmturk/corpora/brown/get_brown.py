import os

files = os.listdir('./brown/')
out = open('brown.txt', 'w')
for file in files:
	f = open('./brown/'+file)
	for line in f:
		data = line.strip().split(' ')
		if len(data)>0:
			sent = ''
			for token in data:
				sent += token.strip().split('/')[0].strip() + ' '
			if len(sent.strip())>0:
				out.write(sent.strip() + '\n')
	f.close()
out.close()
