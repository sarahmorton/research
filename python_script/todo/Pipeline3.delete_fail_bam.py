import os 
import shutil
d = '/home/local/ARCS/hq2130/WES/fastq/bam/'
d = '/home/local/ARCS/hq2130/CHD_MedExomeKit/fastq/bam/'
for filename in os.listdir(d):
    
    if filename.endswith('.FqB.log'):
        bam_name = filename.split('.FqB.log')[0]+'.bwamem.mkdup.bam'
        bai_name = filename.split('.FqB.log')[0]+'.bwamem.mkdup.bai'
        if os.path.exists(d+bam_name):

            
            fewer, cmd = False, False
            with open(d+filename) as f:
                for line in f:
                    if 'file has fewer sequences' in line:
                        fewer = True
                    if '[main] CMD: bwa mem -M -t' in line:
                        cmd = True
            if fewer is True or cmd is False:
		print bam_name, fewer, cmd
                #os.remove( d + bam_name)
                #os.remove(d + filename)
                #os.remove(d + bai_name)
	    else:
		#continue
		print filename, 'good'
    if filename.endswith('.bwamem.bam'):
        os.remove(d + filename)
    if filename.endswith('.bwamem.sorted.bam'):
	os.remove(d + filename)            
            
            
                        
                    
        
