import os

folders = os.listdir('../../substitutions/')

for folder in folders:
	lex = open('../../corpora/lexmturk_all.txt')
	fin = open('../../substitutions/'+folder+'/substitutions_enhancedlesk.txt')
	fout = open('../../substitutions/'+folder+'/substitutions_WSD_enhancedlesk.txt', 'w')

	for line in fin:
		lexl = lex.readline().strip().split('\t')
		data = line.strip().split('\t')
		target = data[0].strip()
		cands = []
		if len(data)>1:
			cands = data[1].strip().split('|||')
		
		newline = lexl[0].strip() + '\t' + lexl[1].strip() + '\t' + lexl[2].strip() + '\t'
		for cand in cands:
			newline += '0:' + cand + '\t'
		fout.write(newline.strip() + '\n')
	lex.close()
	fin.close()
	fout.close()
