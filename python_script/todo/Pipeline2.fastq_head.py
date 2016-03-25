import os
import gzip

#fastq/Sample_1-00270_002_002_R1.fastq.gz	@RG\tID:1-00270\tSM:1-00270\tLB:1-00270\tPL:ILLUMINA\tCN:COLUMBIA_YS_LAB	fastq/Sample_1-00270_002_002_R1.fastq.gz
directory = 'fastq/'
directory = '/home/local/ARCS/hq2130/CHD_MedExomeKit/fastq/'
directory = '/home/local/ARCS/hq2130/WES/fastq/'
fw = open(directory+'fastq_head2.txt','w')

processed = set()
for e in os.listdir(directory):
    if e.endswith('.align'):
	processed.add( e.split('.')[1])
'''
with open(directory+'fastq_head.txt') as f:
	for line in f:
		e = line.split()[0]
		processed.add(e.split('_')[0])
'''

for e in os.listdir(directory):
    if e[0] == '1' and e.endswith('P1.fastq.gz') and len(e.split('_')) <= 2:

        # generate head and filepath 
        f = gzip.open(directory+ e, 'rb') 
        head = f.readline()
        f.close()
        #print e,head
        sample = e.split('_')[0]
	if sample in processed: continue
        head = head.replace('#',' ').rstrip('/1\n') # since are split by space others by #
        PU,LB =  head.split()
        PU = ':'.join(PU[1:].split(':')[:2])
        LB = LB.split(':')[-1]
        #print PU,LB
        rg = '\\t'.join(['@RG','ID:'+sample,'PL:ILLUMINA','PU:'+PU,'LB:'+LB,'SM:'+sample,'CN:COLUMBIA_YS_LAB'])
        fw.write('\t'.join([e,rg, e.split('1.fastq.gz')[0]+'2.fastq.gz'])+'\n')
        
  
fw.close()
