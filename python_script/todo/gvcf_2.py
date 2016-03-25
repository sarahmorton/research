import os


def sample_id(filename):
	if 's1' in filename or 'fa' in filename or 'mo' in filename:
		all_name = filename.split('.')
		real_name = all_name[0]+all_name[1]
	else:
		real_name = filename.split('.')[0]
	return real_name

address = '/home/local/ARCS/hq2130/WES/Breast_gvcf/'
address3 = '/home/local/ARCS/hq2130/WES/Breast_gvcf_comb/'

samples = []


for e in os.listdir(address):
    
    if e.endswith('gz'): # samples using mkdup
        samples.append(address+e)



samples.sort()    
idx = 45
i = 0    
fw = open(address3+'cohort'+str(idx)+'.list','w')
for e in samples:
    #print e
    #print source[e]
    if i < 199:
        i += 1
        fw.write(e+'\n')
    else:
        fw.write(e+'\n')
        fw.close()
        idx += 1
        i = 0
        fw = open(address3+'cohort'+str(idx)+'.list','w')
fw.close()
        
fw = open(address3+'bam.txt','w')
for e in os.listdir(address3):
    if e.endswith('list'): # samples using mkdup and realigned
        fw.write(e+'\n')
fw.close()
