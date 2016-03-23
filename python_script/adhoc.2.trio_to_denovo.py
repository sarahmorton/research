# takes vcf directory, output new vcf with only denovo mutations
# general results, need to refine MAF, ref/(ref+alt)
# rare, pass, denovo
import gzip
import os
from optparse import OptionParser


def check_rare_exon(INFOstring):# find variant with propability < 0.1%
    threshold = 0.1 / 100
    CodingCodes={'splicing', 'exonic', 'exonic,splicing'}
    
    INFOcolumnList=INFOstring.split(";")
    INFOdict={}
    for element in INFOcolumnList:
        if '=' in element:
            FieldName,FieldValue=element.split('=',1)
            INFOdict[FieldName]=FieldValue
    
    # Get values from INFO fields
    KGscore= max(map(float,[ rate  for rate in INFOdict.get('1KGfreq',str(threshold)).split(',') if rate != '.' ]))
    ESPscore= max(map(float,[ rate  for rate in INFOdict.get('ESPfreq',str(threshold)).split(',') if rate != '.' ]))
    ExAcscore= max(map(float,[ rate  for rate in INFOdict.get('ExACfreq',str(threshold)).split(',') if rate != '.' ]))
    MutationFunct=str(INFOdict.get('VarFunc','None').split(',')[0])
    return KGscore <= threshold and ESPscore <= threshold and  ExAcscore <= threshold and MutationFunct in CodingCodes



def check_denovo(trio):

    proband= trio[0].split(':')
    Father = trio[1].split(':')
    Mother = trio[2].split(':')
    proband_GT = proband[0]
    Father_GT = Father[0]
    Mother_GT = Mother[0]
    
    if proband_GT in {'./.','0/0'}: #proband genotype missing or not denovo
        return False
    else:#GT:AD:DP:GQ:PL	0/1:16,9:.:99:205,0,501
        if Father_GT == '0/0' and Mother_GT == '0/0':
            return True
        else:
            return False


parser = OptionParser()
parser.add_option("-v", "--vcf", dest="VCFfile",help="input VCF folder", metavar="VCFfile")
(options, args) = parser.parse_args()
vcf_name = options.VCFfile

# make vcf trio dir
trio_dir = os.path.dirname(vcf_name)
denovo_dir = '/'.join(os.path.abspath(trio_dir).split('/')[:-1])+'/vcf_rare_denovo/'
if not os.path.exists(denovo_dir):
    os.makedirs(denovo_dir)


for fname in os.listdir(trio_dir):
    if fname.endswith('.vcf'):
        f1 = open(trio_dir+'/'+fname)
        fw = open(denovo_dir+fname,'w')
        for line in f1:
            if line[0]=='#': # get and write head
                fw.write(line)
            else: #write rare-deleterious-inherited mutations 	 		
                data =  line.split()
                INFOstring = data[7]
                if check_rare_exon(INFOstring): #population freq later
               	    trio = data[9:12]	    
               	    if check_denovo(trio):
                   	    fw.write("\t".join(data[:9]+trio)+'\n') 
		    	
        fw.close() 

