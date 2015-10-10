f = open('/export/data/ghpaetzold/generalpurpose/glove/mymodel/final_model_glove.txt')
o = open('/export/data/ghpaetzold/generalpurpose/glove/mymodel/final_model_glove_w2v.txt', 'w')
#f = open('../../corpora/wordvectors/word_vectors_all_300_cbow.txt')

#Get data:
line = f.readline().strip()
vecsize = len(line.split(' '))-1
entries = 1
for line in f:
	entries += 1
f.close()

#Write first line:
print(str(entries) + ' ' + str(vecsize))
o.write(str(entries) + ' ' + str(vecsize) + '\n')

#Write rest of file:
f = open('/export/data/ghpaetzold/generalpurpose/glove/mymodel/final_model_glove.txt')
c = 1
problems = 0
for line in f:
	c += 1
	if c%500000==0:
		print(str(c))
	#word = line.split(' ')[0].strip()
	#if len(word)==0:
	#	print('Problem: ' + line.strip())
	#if isinstance(line, unicode):
	#	problems += 1
	o.write(line)
f.close()
o.close()

#print('Unicode entries: ' + str(problems))
#print('Lines: ' + str(c))
