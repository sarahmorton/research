gvcf = set()

import os 
import shutil

address = '/home/local/ARCS/hq2130/WES/fastq/merge/'
address = '/home/local/ARCS/hq2130/WES/fastq/merge_bam/'
merge = {}
for e in os.listdir(address):
    if e.endswith('bam'):
	sample = e.split('_')[0]
	if sample in merge:
	    merge[sample].append(e)
        else:
            
	    merge[sample] = [e]
	
	
for sample, addr in merge.items():
    with open(address+sample+'.list','w') as f:
        for e in addr:
            f.write(address+e+'\n')


