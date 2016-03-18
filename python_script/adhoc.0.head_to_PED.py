'''
script takes vcf head and format to ped
'''
dirs = '/home/local/ARCS/hq2130/CHD_MedExomeKit/vcf_0223/'
vcf_head = 'head.txt'
ped_name = 'CHD_MedExomeKit.ped'
with open(dirs+vcf_head) as f:
	cases = set()
	all_case = set()
	lst = f.readline().strip().split()
	i = 0
	for e in lst:
		i += 1
		if e[0] == '1' and not e.endswith('-01' )and not e.endswith('-02' ):
			cases.add(e) 
		if e[0] == '1' :
			all_case.add(e[:7]) 

	print 'non completed trio:'
	print all_case - cases
	print 'total trios: %s' %(len(cases))
	cases = list(cases)
	cases.sort()
	fw = open(dirs+ped_name,'w')
	fw.write('\t'.join(['FAMILY',	'PERSON',	'FATHER',	'MOTHER',	'SEX(1 for male)',	'Affected(2 for affected)',	'comment', '\n']))
	for e in cases:
		fw.write('\t'.join([e , e , e +'-01', e +'-02', 'x', 'x', 'x', '\n']))
	fw.close()