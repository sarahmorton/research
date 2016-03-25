gvcf = set()

import os 
import shutil
d = "/home/local/ARCS/hq2130/WES/fastq_yale3/"
fw = open(d+'fastq_dir.txt','w')
for filename in os.listdir(d):
    #print 'xxx',filename
    move = True
    if os.path.isdir(d +filename):
        for fastq_name in os.listdir(d +filename ):
            if '_002' in fastq_name:
                move = False
        if  move :
            for fastq_name in os.listdir(d +filename ):
                adddress1 =  d +filename + '/'+fastq_name
                adddress2 = '/home/local/ARCS/hq2130/WES/fastq_upload'
                #print adddress1
                #shutil.move(adddress1, adddress2)
                
            #break
        else:
            adddress1 =  d +filename #+ '/'+fastq_name
            print adddress1
	    fw.write(adddress1 + '\n')

        #    print filename
            
                
fw.close()

