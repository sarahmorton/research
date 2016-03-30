#!/usr/bin/env python
#pipeline.2.fastq_head
#
#

import os 
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--fastq", dest="fastq",help="input fastq folder", metavar="fastqfolder")


(options, args) = parser.parse_args()
fastq_folder = options.fastq

head_file = os.path.join(fastq_folder, 'fastq_head.txt')
fw = open(directory+'fastq_head.txt','w')
for e in os.listdir(directory):
    if e[0] == '1' and e.endswith('1.fastq.gz'):
        # generate head and filepath 
        f = gzip.open(directory+ e, 'rb') 
        head = f.readline()
        f.close()
        #print e,head
        sample = e.split('_')[0]
        head = head.replace('#',' ').rstrip('/1\n') # since are split by space others by #
        PU,LB =  head.split()
        PU = ':'.join(PU[1:].split(':')[:2])
        LB = LB.split(':')[-1]
        #print PU,LB
        rg = '\\t'.join(['@RG','ID:'+sample,'PL:ILLUMINA','PU:'+PU,'LB:'+LB,'SM:'+sample,'CN:COLUMBIA_YS_LAB'])
        fw.write('\t'.join([e,rg, e.split('1.fastq.gz')[0]+'2.fastq.gz'])+'\n')
fw.close()
