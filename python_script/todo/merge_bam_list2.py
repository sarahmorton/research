gvcf = set()

import os 
import shutil

address = '/home/local/ARCS/hq2130/WES/pagc3_mergebam/merge_bam/'

def name(e):
    sample = e.split('.')[0].split('_')[0]
    if len(sample.split('-')) >= 3:
        if sample.split('-')[2] in {'01','02'}:
            sample = '-'.join(sample.split('-')[:3])
        else:
            sample = '-'.join(sample.split('-')[:2])
    return sample


merge = {}
for e in os.listdir(address):
    if e.endswith('bam'):
        sample_name = name(e)
        #print e,sample_name
	if sample_name in merge:
	    merge[sample_name].append(e)
        else:
            
	    merge[sample_name] = [e]
	
	
for sample, addr in merge.items():
    with open(address+sample+'.list','w') as f:
        if len(addr) < 2:
            print sample
        for e in addr:
            f.write(address+e+'\n')

