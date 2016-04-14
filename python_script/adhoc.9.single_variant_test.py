

import csv
import os 
from optparse import OptionParser
from utils import check_rare_exon, get_variant_type, get_GQ, get_DP

def get_useful_info(useful_info, INFOstring):
    '''
    function to reformat the info string in the sequence in head 

    Parameters
    ----------
    :type head: list 
    :param head: info matches head

    :type INFOstring: str 
    :param INFOstring: info column in vcf file

    returns
    ----------
    :type row : list
    :           list of info extraced from INFOstring
    '''    
    INFOcolumnList=INFOstring.split(";")
    INFOdict={}
    for element in INFOcolumnList:
        if '=' in element:
            FieldName,FieldValue=element.split('=',1)
            INFOdict[FieldName]=FieldValue
    row = []
    for useful_column in useful_info:
        row.append(INFOdict.get(useful_column, 'NA'))
    return row


usage = "usage: %prog [options] arg1 arg2"
parser = OptionParser(usage=usage)
parser.add_option("-v", "--vcf", dest="VCFfile",help="input VCF file", metavar="VCFfile")
parser.add_option("-c", "--case", dest="CASEfile",help="input case file", metavar="CASEfile")
parser.add_option("-o", "--output", dest="OutputFileName",help="user specified name of file for output to be written", metavar="OutputFileName")

(options, args) = parser.parse_args()
vcfname = os.path.abspath(options.VCFfile)
case_file = os.path.abspath(options.CASEfile)
out_csv = options.OutputFileName

with open(vcfname, 'r') as f:
    for line in f: 
        if line[:6]=='#CHROM': 
            samples = line.strip().split('\t')
            break

case_index=[]
with open(case_file) as f:
    for line in f:
        case = line.strip()
        if case in samples:
            case_index.append(samples.index(case))
        

fw = open(out_csv,'wb')
w = csv.writer(fw)
useful_info = ['GeneName', 'AC', 'AF','AN','VarClass', 'VarFunc', 'MetaSVMprd',
                'PP2.hdiv.prd', 'CADDphred', 'AAChange',  'ExACfreq', 'QD', 'SegDup']
w.writerow(['Homo', 'Het', 'WT', 'variant-type','CHROM', 'POS', 'REF', 'ALT', 'FILTER' ] + useful_info)

# process vcfs to extract info of single variant 
with open(vcfname)  as f:
    for line in f:
        if line[0] == '#':
            continue
        else:
            data =  line.split('\t')
            INFOstring = data[7]

            if check_rare_exon(INFOstring):
                homo, het, wt = 0, 0, 0
                for index in case_index:
                    info = dict(zip(data[8].split(':'),data[index].split(':')))
                    GT = info.get('GT')
                    if GT != './.':
                        
                        GQ = get_DP(info)
                        DP = get_DP(info)
                        if int(info['GQ']) >= 20 and DP >= 10:
                            if GT == '0/0':
                                wt += 1

                            elif GT[0] == '0':
                                het += 1

                            elif GT[0] == GT[2]:
                                homo += 1
                            else:
                                # ignore variants like 1/2, 1/3, 1/4
                                pass
                                
                if homo + het > 0:
                    row = get_useful_info(useful_info, INFOstring)
                    variant_type = get_variant_type(INFOstring)
                    w.writerow([homo, het, wt, variant_type] + data[0:2] + data[3:5] + [data[6]]+ row)


fw.close()