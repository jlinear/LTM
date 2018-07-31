import sys, random


def generate_tables(in_file):
	fr = open(in_file)
	rawdb = {} # entity--attribute--source
	F_set = set()
	for line in fr:
		item = line.strip('\r\n').split('\t')
		e,a,s = item[0], item[1], item[2]
		f = (e,a)

		if not e in rawdb:
			rawdb[e] = {}
		if not a in rawdb[e]:
			rawdb[e][a] = []
		rawdb[e][a].append(s)

		F_set.add(f)
	fr.close()

	F = sorted(F_set) # fid--entity(e_f)--attribute(a_f)

	C = {} #fid--source--observation(T/F)
	for i, f in enumerate(F):
		(e_f, a_f) = f
		C[i] = {}
		e_src = []
		for [attr, src] in sorted(rawdb[e_f].items(), key=lambda x:x[0]):
			e_src += src
		for s in e_src:
			if s in rawdb[e_f][a_f]:
				C[i][int(s)] = True
			else:
				C[i][int(s)] = False

	return F, C

def LTM(F, C, beta, alpha0, alpha1, burnin, maxit, sample_size):


	#### Initialization
	for f in F:
		dhj = 1

	#### Sampling

		#### Sample t_f from conditional distribution

		#### Calculate expectation of t_f


if __name__ == '__main__':
	F, C =  generate_tables(sys.argv[1])
	print F[0]
	print len(C[0])