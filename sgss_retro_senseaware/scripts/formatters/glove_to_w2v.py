import sys, gensim

glove = sys.argv[1]
temp = sys.argv[2]
size = int(sys.argv[3])
output = sys.argv[4]

print('Calculating number of instances...')
#words = set([])
#f = open(glove)
#for line in f:
#	words.add(line.strip().split(
#f.close()

print('Saving temporary file...')
#t = open(temp, 'w')
#t.write(str(c) + ' ' + str(size) + '\n')
#f = open(glove)
#for line in f:
#	t.write(line)
#f.close()
#t.close()

print('Loading temporary text model...')
m = gensim.models.word2vec.Word2Vec.load_word2vec_format(temp, binary=False)

print('Writing vectors...')
m.save_word2vec_format(output, fvocab=None, binary=True)
