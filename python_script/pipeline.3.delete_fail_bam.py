#

#pipeline.3.delete_fail_bam.py -b bam/ -d
#
#

import os 
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-b", "--bN", dest="BAMfile",help="input BAM folder", metavar="BAMfile")
parser.set_defaults(delete=False)
parser.add_option("-d", "--delete", action='store_true', dest="delete", help="delete fail bams")

(options, args) = parser.parse_args()
bam_folder = options.BAMfile
deletebam=options.delete

def bamname(bam):
    sample = bam.split('.')[0]
    bam_name = sample+'.bwamem.mkdup.bam'
    bai_name = sample+'.bwamem.mkdup.bai'
    log_name = sample+'.FqB.log'
    return bam_name, bai_name, log_name


for filename in os.listdir(bam_folder):  
      
    if filename.endswith('.bam'):
        if filename.endswith('.bwamem.bam'):
            print filename, 'not finished, before sort'
            if deletebam:
                os.remove(bam_folder + '/' + filename)
        elif filename.endswith('.bwamem.sorted.bam'):
            print filename, 'not finished, before mkdup'
            if deletebam:
                os.remove(bam_folder + '/' + filename)
        else:
            bam_name, bai_name, log_name = bamname(filename) 

            # has bam
            if os.path.exists(bam_folder+'/'+bam_name):
                fewer, finish = False, False
                
                # check bam finish successfully 
                with open(bam_folder+'/'+filename) as f:
                    for line in f:
                        if 'file has fewer sequences' in line:
                            fewer = True
                        if '[main] CMD: bwa mem -M -t' in line:
                            finish = True
                # failed
                if fewer is True or finish is False:
                    print bam_name, fewer, finish
                    if deletebam:
                        os.remove( bam_folder + '/' + bam_name)
                        os.remove(bam_folder + '/' + bai_name)
                        os.remove(bam_folder + '/' + log_name)
        	    else:
            		print filename, 'good'
            else:
                print filename, 'something strange'
 
           
            
            
                        
                    
        
