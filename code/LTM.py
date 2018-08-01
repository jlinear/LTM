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
				C[i][int(s)] = 1 #True
			else:
				C[i][int(s)] = 0 #False

	return F, C

def LTM(F, C, alpha0, alpha1, beta, burnin, maxit, sample_size):

	# F is in the form an ordered list (index as fid)
	# C is a dict: fid 2 source : observation
	# alpha0 = (alpha01, alpha00) prior false positive count, prior true negative count  per source
	# alpha1 = (alpha11, alpha10) prior true positive count, prior false negative count  per source
	# beta = (beta1, beta0) prior true count, prior false count  per fact

	alpha = {}
	alpha[0] = alpha0
	alpha[1] = alpha1

	#### Initialization
	T = [] # The truth table of all facts
	n_sto = {}
	p_true = []
	for fid, f in enumerate(F):
		ran = random.uniform(0,1)
		if ran < 0.5:
			t_f = 0
		else:
			t_f = 1
		T.append(t_f)

		n_sto[fid] = {}
		for s_c in C[fid].keys():
			if not s_c in n_sto[fid]:
				n_sto[fid][s_c] = {}
			if not t_f in n_sto[fid][s_c]:
				n_sto[fid][s_c][t_f] = {}
				n_sto[fid][s_c][1-t_f] = {}
			if not C[fid][s_c] in n_sto[fid][s_c][t_f]: # C[fid][s_c] -> o_c
				n_sto[fid][s_c][t_f][C[fid][s_c]] = 0
				n_sto[fid][s_c][t_f][1-C[fid][s_c]] = 0
				n_sto[fid][s_c][1-t_f][C[fid][s_c]] = 0
				n_sto[fid][s_c][1-t_f][1-C[fid][s_c]] = 0

			n_sto[fid][s_c][t_f][C[fid][s_c]] += 1 

		p_true.append(0)

	#### Sampling
	i = 0
	p = {}
	while i < maxit:
		i += 1
	
		for fid, f in enumerate(F):
			if not fid in p:
				p[fid] = {}
			t_f = T[fid]
			p[fid][t_f] = beta[t_f]
			p[fid][1-t_f] = beta[1-t_f]

			for s_c in C[fid].keys():
				o_c = C[fid][s_c]
				p[fid][t_f] = 1.0 * p[fid][t_f] * (n_sto[fid][s_c][t_f][o_c] - 1 + alpha[t_f][o_c]) /  \
							(n_sto[fid][s_c][t_f][1] + n_sto[fid][s_c][t_f][0] - 1 + alpha[t_f][1] + alpha[t_f][0])
				p[fid][1-t_f] = 1.0 * p[fid][1-t_f] * (n_sto[fid][s_c][1-t_f][o_c] - 1 + alpha[1-t_f][o_c]) /  \
							(n_sto[fid][s_c][1-t_f][1] + n_sto[fid][s_c][1-t_f][0] - 1 + alpha[1-t_f][1] + alpha[1-t_f][0])

		#### Sample t_f from conditional distribution
			ran = random.uniform(0,1)
			if (p[fid][t_f] + p[fid][1-t_f]) == 0: #May have some issues here!!!
				temp = float('inf')
			else:
				temp = 1.0 * p[fid][1-t_f] / (p[fid][t_f] + p[fid][1-t_f])
			if ran < temp:
				t_f = 1 -t_f
				T[fid] = t_f # update truth table
				for s_c in C[fid].keys():
					o_c = C[fid][s_c]
					n_sto[fid][s_c][1-t_f][o_c] -= 1
					n_sto[fid][s_c][t_f][o_c] += 1

		#### Calculate expectation of t_f
			if i > burnin and i % sample_size == 0:
				p_true[fid] += 1.0 * t_f / sample_size

	# for fid, f in enumerate(F):
	# 	if p_true[fid] > 0.1:
	# 		T[fid] = 1
	# 	else:
	# 		T[fid] = 0

	# return T

	res = []
	for fid, f in enumerate(F):
		res.append(p_true[fid])

	return res


if __name__ == '__main__':
	F, C =  generate_tables(sys.argv[1])
	
	alpha0 = (10, 1000)
	alpha1 = (50, 50)
	beta = (10, 10)

	T = LTM(F, C, alpha0, alpha1, beta, 2, 5, 2)

	outf_name = sys.argv[2] + '_out.txt'
	fw = open(outf_name,'w')
	for fid, f in enumerate(F):
		fw.write(str(fid) + '\t' + f[0] + '\t' + f[1] + '\t' + str(T[fid]) + '\n')
	fw.close()





