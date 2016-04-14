#  takes a vcf file, filtered rare exon variants and output to _rare.vcf

import os
from optparse import OptionParser
from utils import check_rare_exon

parser = OptionParser()
parser.add_option("-v", "--vcf", dest="VCFfile",help="input VCF folder", metavar="VCFfile")
(options, args) = parser.parse_args()

vcf_name = os.path.abspath(options.VCFfile)
rare_name = vcf_name.split('.vcf')[0] + '_rare.vcf'

ChrCount=0
with open(vcf_name, 'r') as f:
    fw = open(rare_name, 'w')
    for line in f: 
        if line[0]=='#': # get and write head
            fw.write(line)
        else: 
            data = line.strip().split('\t')

            # verbose  
            ChrPresent = data[0]
            if ChrCount != ChrPresent:
                print "Chromosome "+str(ChrPresent)
                ChrCount=ChrPresent
            
            INFOstring = data[7]
            if check_rare_exon(INFOstring):
                fw.write(line)
    fw.close()

            
