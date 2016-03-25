import os


def sample_id(filename):
	if 's1' in filename or 'fa' in filename or 'mo' in filename:
		all_name = filename.split('.')
		real_name = all_name[0]+all_name[1]
	else:
		real_name = filename.split('.')[0]
	return real_name

address = '/home/local/ARCS/hq2130/WES/gvcf_extra/'
address1 = '/home/local/ARCS/hq2130/WES/gvcf_renamed/'
address2 = '/home/local/ARCS/hq2130/WES/gvcf/'
address3 = '/home/local/ARCS/hq2130/WES/sample1227/'


samples = []
filename = []
sample_to_filename = {}


for e in os.listdir(address):
    
    if e.endswith('gz') and 'realigned' not in e: # samples using mkdup
        sample_name = sample_id(e)
        if sample_name not in samples:
            samples.append(sample_name)
            sample_to_filename[sample_name] = address+e

for e in os.listdir(address):
    if e.endswith('gz'): # samples using mkdup and realigned
        sample_name = sample_id(e)
        if sample_name not in samples:
            samples.append(sample_name)
            sample_to_filename[sample_name] = address+e

for e in os.listdir(address1):
    
    if e.endswith('gz') and 'realigned' not in e: # samples using mkdup
        sample_name = sample_id(e)
        if sample_name not in samples:
            samples.append(sample_name)
            sample_to_filename[sample_name] = address1+e

for e in os.listdir(address1):
    if e.endswith('gz'): # samples using mkdup and realigned
        sample_name = sample_id(e)
        if sample_name not in samples:
            samples.append(sample_name)
            sample_to_filename[sample_name] = address1+e


for e in os.listdir(address2):
    
    if e.endswith('gz') and 'realigned' not in e: # samples using mkdup
        sample_name = sample_id(e)
        if sample_name not in samples:
            samples.append(sample_name)
            sample_to_filename[sample_name] = address2+e

for e in os.listdir(address2):
    if e.endswith('gz'): # samples using mkdup and realigned
        sample_name = sample_id(e)
        if sample_name not in samples:
            samples.append(sample_name)
            sample_to_filename[sample_name] = address2+e


samples.sort()    
idx = 1
i = 0    
fw = open(address3+'cohort'+str(idx)+'.list','w')
for e in samples:
    #print e
    #print source[e]
    if i < 199:
        i += 1
        fw.write(sample_to_filename[e]+'\n')
    else:
        fw.write(sample_to_filename[e]+'\n')
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
