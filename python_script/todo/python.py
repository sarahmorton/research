gvcf = set()

import os 
import shutil
d = "/home/local/ARCS/hq2130/WES/gvcf/"
d1 = "/home/local/ARCS/hq2130/WES/gvcf_renamed/"
d2 = "/home/local/ARCS/hq2130/WES/gvcf_extra/"

d3 = "/home/local/ARCS/hq2130/WES/PCGC_2000trios/combind_gvcf/"
#d1 = '/home/local/ARCS/hq2130/WES/Merge_BAM/merger_vcf/'
d3 = '/home/local/ARCS/hq2130/WES/pagc3_mergebam/merge_bam/BAM/'
processed = set()
for filename in os.listdir(d):
	if '.gz' in filename:
		#print filename
		processed.add(filename.split('.')[0])
for filename in os.listdir(d1):
	if '.gz' in filename:
		#print filename
		processed.add(filename.split('.')[0])
for filename in os.listdir(d2):
	if '.gz' in filename:
		#print filename
		processed.add(filename.split('.')[0])		
		
fw = open(d3+'bam2.txt','w')
for filename in os.listdir(d3):    
    if filename.endswith('1-04867-01.merged.mkdup.bam'):
        #if filename.split('.')[0] in processed: continue
	fw.write(filename + '\n')
fw.close()