#takes rare inherited vcf directory as input output summary csv
# python /home/local/ARCS/hq2130/Exome_Seq/scripts/python_script/adhoc.4.variants_to_csv.py -v vcf_inherited -o CHD_MedExomeKit_inherited0318.csv
import csv
import gzip
import os
from optparse import OptionParser

def info_list(INFOstring, head):
    
    INFOcolumnList=INFOstring.split(";")
    INFOdict={}
    for element in INFOcolumnList:
        if '=' in element:
            FieldName,FieldValue=element.split('=',1)
            INFOdict[FieldName]=FieldValue           
    result = []
    for e in head:
        result.append(INFOdict.get(e,'NA'))
        
    return result


parser = OptionParser()
parser.add_option("-v", "--vcf", dest="VCFfolder",help="input VCF folder", metavar="VCFfolder")
parser.add_option('-o', '--output', dest='output',help='output csv name', metavar='output')
(options, args) = parser.parse_args()
vcf_folder = options.VCFfolder
output = options.output


# get info head
for e in os.listdir(vcf_folder):
    with open(vcf_folder +'/'+ e) as f:
        head = []
        for line in f:
            if line[0] =='#':
                if line.startswith('##INFO=<ID='):
                    head.append(line.split('=')[2].split(',')[0]) # head = [AD,DP]
            else:
                break
    break
print head
mutation = {}
for e in os.listdir(vcf_folder):
    if e.endswith('.vcf'):
        with open(vcf_folder +'/'+ e) as f1:
            proband, father_ID, mother_ID= e.rsplit('.vcf')[0].split('_')
            for line in f1:
                if line[0] !='#':
                    info = line.split()
                    m = '\t'.join(info[:6]+[ info[6] ]) #before info except qual
                    
                    INFOstring = info[7]
                    INFOlist = info_list(INFOstring,head)
                    

                    proband_geno = info[9].split(':')[0]
                    proband_info = info[9]
                    Father_geno = info[10].split(':')[0]
                    Father_info = info[10]
                    Mother_geno = info[11].split(':')[0]
                    Mother_info = info[11]
                    
                    if proband_geno[0] == proband_geno[-1]: #1/1
                        parents_list = father_ID +'('+Father_info+')'+','+mother_ID +'('+ Mother_info +')'
                    elif proband_geno[-1] == Father_geno[-1] and proband_geno[-1] != Mother_geno[-1]:
                        parents_list=father_ID+'('+Father_info+')'
                    elif proband_geno[-1] != Father_geno[-1] and proband_geno[-1] == Mother_geno[-1]:
                        parents_list=mother_ID+'('+Mother_info+')'
                    else: # for strange varaints 
                        parents_list = father_ID +'('+Father_info+')'+','+mother_ID +'('+ Mother_info +')'


                    if m in mutation:
                        mutation[m][0] = proband+'('+ proband_info+')'+';'+mutation[m][0]
                        mutation[m][1] = parents_list+';'+mutation[m][1]
                       
                    else:
                        mutation[m] = [proband+'('+ proband_info +')'] + [parents_list] + INFOlist

with open(output,'wb') as f:
    w = csv.writer(f)
    w.writerow(['CHROM','POS','ID','REF','ALT','QUAL','FILTER','proband ID(GT:AD:DP:GQ:PL)','parents']+head)
    for key in mutation:
        content= key.split('\t')
        content = content + mutation[key]
        w.writerow(content)
    

