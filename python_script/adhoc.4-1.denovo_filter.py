
from __future__ import division
import csv
import gzip
import shutil
import subprocess
import os
from optparse import OptionParser


def reads_filter(proband,parents,parameter): # R,A used for checking indel AC is [1,1]
    ID, geno =  proband.split('(')
    father,mother = parents.split('),')
    fatherID,fathergeno = father.split('(')
    motherID,mothergeno = mother[:-1].split('(')
    
    if len(geno[:-1].split(':')) == 5:
        GT,AD,DP,GQ,PL =  geno[:-1].split(':')
        fGT,fAD,fDP,fGQ,fPL =  fathergeno.split(':')
        mGT,mAD,mDP,mGQ,mPL =  mothergeno.split(':')
    elif len(geno[:-1].split(':')) == 7:
        GT,AD,DP,GQ,_,_, PL =  geno[:-1].split(':')
        fGT,fAD,fDP,fGQ,_, _, fPL =  fathergeno.split(':')
        mGT,mAD,mDP,mGQ,_,_, mPL =  mothergeno.split(':')
    else:
        GT,_,AD,DP,GQ, PL =  geno[:-1].split(':')
        fGT,_, fAD,fDP,fGQ, fPL =  fathergeno.split(':')
        mGT,_, mAD,mDP,mGQ,mPL =  mothergeno.split(':')
        
    ref, alt = map(int,GT.split('/'))
    
    # parents filter
    if  mDP == '.':
        print mother
        mDP = 1
    if  fDP == '.':
        fDP = 1
    if  DP == '.':
        DP = 1  
                
    if float(mDP) < 1:
        mDP = 1
    if float(fDP) < 1:
        fDP = 1
    Fmaf = int(fAD.split(',')[alt])/float(fDP)
    Mmaf = int(mAD.split(',')[alt])/float(mDP) 
    
    # proband filter
    AD = map(int,AD.split(','))
    DP = float(DP)
    proband_PL = int(PL.split(',')[0])


    return int(AD[alt]) >= 6  and proband_PL >= parameter['probandPL'] and\
    Fmaf <= parameter['MAF']/100 and Mmaf <= parameter['MAF']/100 and \
    int(mDP) >= parameter['PDP'] and int(fDP)>= parameter['PDP'] \
    and int(mGQ) >=parameter['PGQ'] and int(fGQ) >= parameter['PGQ']

        
def info_filter(variants, snps):
    '''
    functions that flag the variant of FS, QD
    '''
    p = True
    if snps:
        if float(variants['FS']) >= 25:
            p = False
        if float(variants['QD']) < 2:
            p = False 
    else:
        if float(variants['FS']) >= 25:
            p = False
        if float(variants['QD']) < 1:
            p = False   
        if variants['ReadPosRankSum'] != 'NA' and float(variants['ReadPosRankSum']) < -3.0:
            p = False         
    return p
 

def variants_tune(filename,parameter):
    
    with open(filename,'Ur') as denovo_f:
        denovo_r = csv.reader(denovo_f)
        head = denovo_r.next()

        denovo_snp, denovo_indel =[], []
        denovo_w1= open(filename.split('.csv')[0] + '.snp.csv','wb')
        w1= csv.writer(denovo_w1)
        w1.writerow(head)
        denovo_w2= open(filename.split('.csv')[0] + '.indel.csv','wb')
        w2= csv.writer(denovo_w2)
        w2.writerow(head)   
        denovo_w3= open(filename.split('.csv')[0] + '.snpindel.csv','wb')
        w3= csv.writer(denovo_w3)
        w3.writerow(head) 
        
        idx = dict(zip(head, range(len(head))))
        for line in denovo_r:
            variants = dict(zip(head, line))
            chrom = variants['CHROM']
            pos = variants['POS']
            Ref = variants['REF']
            Alt = variants['ALT']
            probands = variants['proband ID(GT:AD:DP:GQ:PL)'].split(';')
            parents = variants['parents'].split(';')
            AC = variants['AC'].split(',') 
            
                    
            if len(Alt.split(',')) > 2 : continue # remove multi-allel sites(3 or more alt)
            if 'MUC' in variants['GeneName']: continue # remove MUC
            if 'HLA' in variants['GeneName']: continue # remove HLA 
            if 'GL' in chrom: continue
            
            SegDup = 0 if variants.get('SegDup') == 'NA' else float(variants.get('SegDup',':0').split(':')[1].split(',')[0])
            if SegDup > parameter['general']['SegDup']: continue
         
            for i in range(len(probands)) :
                newline = list(line)
                proband = probands[i]
                newline[idx['proband ID(GT:AD:DP:GQ:PL)']] = proband
                parent = parents[i] 
                newline[idx['parents']] = parent
                ID, geno = proband.split('(')
                GT = geno[:-1].split(':')[0]
                ref, alt = map(int,GT.split('/'))
                newline[idx['ALT']] = Alt.split(',')[alt-1]                
                real_AC = int(AC[alt-1])
                if real_AC > parameter['general']['AC']: continue
                variant_id = '_'.join([ID,chrom,pos])
                if len(variants['VarClass'].split(',')) > 1:
                    newline[idx['VarClass']] = variants['VarClass'].split(',')[alt-1]

                snp = len(newline[idx['ALT']]) == len(Ref) and newline[idx['ALT']] != '*'
                if snp: 
                    if info_filter(variants, True) and reads_filter(proband,parent,parameter['snp']) :
                        denovo_snp.append(variant_id)
                        w1.writerow(newline)   
                        w3.writerow(newline)   
                else:
                    if info_filter(variants, False) and reads_filter(proband,parent,parameter['indel']):
                        denovo_indel.append( variant_id)
                        w2.writerow(newline)   
                        w3.writerow(newline)               
        denovo_w1.close()
        denovo_w2.close()
        denovo_w3.close()
        denovo_f.close()
    return denovo_snp, denovo_indel



# python /home/local/ARCS/hq2130/Exome_Seq/scripts/python_script/adhoc.5.denovo_filter.py -c CHD_MedExomeKit_denovo0318.csv 
parser = OptionParser()
parser.add_option("-c", "--csv", dest="CSVfile",help="input CSV file", metavar="CSVfile")
(options, args) = parser.parse_args()
csv_name = options.CSVfile

csv_name  = os.path.abspath(csv_name)
parameter = {'snp':{'MAF': 5, 'PDP':8, 'PGQ':30,'probandPL':30}, \
             'indel': {'MAF': 5, 'PDP':10, 'PGQ':30,'probandPL':70},\
             'general':{'AC':4, 'SegDup':0.99}}
denovo_snp, denovo_indel = variants_tune(csv_name,parameter)
print '%s denovo snp, %s denovo indels'%(len(denovo_snp), len(denovo_indel))


