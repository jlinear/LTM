import random


def generate_tables(in_file):
	#0RANKPATTERN	1PATTERN	2ENTITYPOS	3VALUEPOS	4RANKENTITYVALUETM	5ENTITY	6VALUE	7TM	8COUNT
	fr = open(in_file,'r')
	fr.readline()
	rawdb = {} # entity--attribute--source
	fact_table = set() # fid--entity(e_f)--attribute(a_f)
	for line in fr:
		item = line.strip('\r\n').split('\t')
		entity, attr, src = item[5], item[6] + '+' + item[7], item[0]
		fact = entity + '\t' + attr

		#rawdb
		if not entity in rawdb:
			rawdb[entity] = {}
		if not attr in rawdb[entity]:
			rawdb[entity][attr] = []
		rawdb[entity][attr].append(src)

		#generate fact table
		# fact_table.add(fact)

	fr.close()

	claim_table = {} #fid--source--observation
	#C_f: claim_table[i]
	#S_f: e_src
	# for i,f in enumerate(sorted(fact_table)):
	# 	[e_f, a_f] = f.split('\t')
	# 	claim_table[i] = {}
	# 	e_src = []
	# 	for [attr, src] in sorted(rawdb[e_f].items(), key=lambda x:x[0]):
	# 		e_src += src
	# 	for s in e_src:
	# 		if s in rawdb[e_f][a_f]:
	# 			claim_table[i][int(s)] = True
	# 		else:
	# 			claim_table[i][int(s)] = False


	#printing (for debugging usage)
	rawdb_name = '_rawdb.txt'
	f_table_name = '_fact_table.txt'
	c_table_name = '_claim_table.txt'
	fw1 = open(rawdb_name,'w')
	for [entity, attr2src] in sorted(rawdb.items(), key=lambda x:x[0]):
		for [attr, src] in sorted(attr2src.items(), key=lambda x:x[0]):
			for s in src:
				fw1.write(entity + '\t' + attr + '\t' + s + '\n')
	fw1.close()

	# fw2 = open(f_table_name,'w')
	# for i, f in enumerate(sorted(fact_table)):
	# 	fw2.write(str(i) + '\t' + f + '\n')
	# fw2.close()

	# fw3 = open(c_table_name,'w')
	# for [i, s2o] in sorted(claim_table.items(), key=lambda x:x[0]):
	# 	for [s, o] in sorted(s2o.items(), key=lambda x:x[0]):
	# 		fw3.write(str(i) + '\t' + str(s) + '\t' + str(o) + '\n')
	# fw3.close()

	F = sorted(fact_table)
	return rawdb, F, claim_table

def LTM(F, C, beta, alpha0, alpha1, burnin, maxit, sample_size):
	#### Initialization
	for f in F:
		dhj = 1

	#### Sampling

		#### Sample t_f from conditional distribution

		#### Calculate expectation of t_f


if __name__ == '__main__':
	rawdb, F, C =  generate_tables("../data/data_text_CP.txt")