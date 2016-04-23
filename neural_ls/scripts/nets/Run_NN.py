import os

sizes = ['100', '300', '500']
#sizes = ['500', '700']
archs = ['cbow']
retros = ['0']
corpora = ['subimdbfiltered']
#lines = ['10000']
lines = ['10000']
epochs = ['10', '100']
hiddens = ['50']

for size in sizes:
	for arch in archs:
		for retro in retros:
			for corpus in corpora:
				for line in lines:
					for epoch in epochs:
						for hidden in hiddens:
							comm = 'nohup python Train_NN.py '+size+' '+arch+' '+retro+' '+corpus+' '+line+' '+epoch+' '+hidden+' &'
							print(comm)
							os.system(comm)
