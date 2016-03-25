gvcf = set()

import os 
import shutil

d2 = '/home/local/ARCS/hq2130/WES/fastq/bam/'
d2 = '/home/local/ARCS/hq2130/WES/sample1227/gvcf.splitfiles/'
d2 = '/home/local/ARCS/yshen/data/CDH/MGH_data/gVCF/'
d2 = '/home/local/ARCS/yshen/data/CDH/MGH_data/gVCF/gvcf2.splitfiles/'
fw = open(d2 + 'vcf.txt','w')
for filename in os.listdir(d2):
    if filename.endswith('vcf'):
	with open(d2 + filename) as f:
		fw.write( filename+'\n')
fw.close()

