import os
import gzip

#fastq/Sample_1-00270_002_002_R1.fastq.gz	@RG\tID:1-00270\tSM:1-00270\tLB:1-00270\tPL:ILLUMINA\tCN:COLUMBIA_YS_LAB	fastq/Sample_1-00270_002_002_R1.fastq.gz
directory = 'fastq/'
fw = open(directory+'fastq_head2.txt','w')

samples = {}
for e in os.listdir(directory):
    if e.startswith('PCGC'):
	ids = e.split('__')[1]
	if ids in samples:
		samples[ids].append(e)
	else:
		samples[ids] = [e]

for e in os.listdir(directory):
    if e[0] == 'P' and e.endswith('P1.fastq.gz'):# and len(e.split('_')) <= 5:
	print e
        # generate head and filepath 
        f = gzip.open(directory+ e, 'rb') 
        head = f.readline()
        f.close()
        #print e,head
        sample = e.split('__')[1]
        head = head.replace('#',' ').rstrip('/1\n') # since are split by space others by #
        PU,LB =  head.split()
        PU = ':'.join(PU[1:].split(':')[:2])
        LB = LB.split(':')[-1]
        #print PU,LB
        rg = '\\t'.join(['@RG','ID:'+sample,'PL:ILLUMINA','PU:'+PU,'LB:'+LB,'SM:'+sample,'CN:COLUMBIA_YS_LAB'])
        if e == samples[sample][0]:
		sample2 = samples[sample][1]
	else:
		sample2 = samples[sample][0]
	fw.write('\t'.join([e,rg, sample2])+'\n')
        
  
fw.close()
