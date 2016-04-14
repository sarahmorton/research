
from __future__ import division
import csv
import gzip
import shutil
import subprocess
import os
import math
from optparse import OptionParser
from collections import defaultdict



parser = OptionParser()
parser.add_option("-c", "--csv", dest="CSVfile",help="input CSV file", metavar="CSVfile")
parser.add_option("-d", "--doc", dest="DOCfile", help="input doc file",metavar="DOCfile")
(options, args) = parser.parse_args()
csv_name = os.path.abspath(options.CSVfile)

new_head = ['proband ID(GT:AD:DP:GQ:PL)', 'parents', 'GeneName', 'VarClass', 'VarFunc', \
'CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'AAChange', 'AC', 'AF', 'MetaSVMprd', \
'PP2.hdiv.prd', 'CADDphred', 'ExACfreq', '1KGfreq', 'ESPfreq', 'QD', 'FS', 'ReadPosRankSum', \
'MQ', 'MQ0', 'SegDup', 'VQSLOD','culprit']

doc = {}
if options.DOCfile:
    doc_name  = os.path.abspath(options.DOCfile)
    with open(doc_name) as f:
        head = f.readline()
        doc = dict(dp.strip().split() for dp in f.readlines())

# add info part
filtered_denovo = csv_name

# add mappability 
fw = open('temp.txt','w')
with open(filtered_denovo,'rU') as f:
    r = csv.reader(f)
    head = r.next()
    for line in r:
        variant = dict(zip(head, line))
        chrom, start, end = 'chr' + variant['CHROM'], variant['POS'], variant['POS']
        fw.write('\t'.join([chrom, start, end, '\n']))
fw.close()    
            
dir_map = '/home/local/ARCS/hq2130/Exome_Seq/resources/mappability/'
cmd = 'bedtools intersect -a '+dir_map+'hg19.rmsk.bed -b temp.txt'
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
repeat = p.communicate()[0]

rep = {}
for hit in repeat.split('\n'):
    if len(  hit.split()) > 0:
        chrom, start, end, repname = hit.split()[:4]
        rep['_'.join([chrom, start, end])] = repname

cmd = 'bedtools intersect -a '+dir_map+'wgEncodeCrgMapabilityAlign75mer.bedGraph -b temp.txt'
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
repeat = p.communicate()[0]

map_75bp = {}
for hit in repeat.split('\n'):
    if len(  hit.split()) > 0:
        chrom, start, end, mappability = hit.split()[:4]
        map_75bp['_'.join([chrom, start, end])] = mappability


with open(filtered_denovo,'rU') as f:
    r = csv.reader(f)
    head = r.next()
    fw = open('temp.csv','w')
    w = csv.writer(fw)
    w.writerow(new_head + ['In repetitive regions','75bp_mappability','Avg_DP','> sd of Avg_DP'])
    for line in r:
        variant = dict(zip(head, line))
        chrom, start, end = 'chr' + variant['CHROM'], variant['POS'], variant['POS']
        variant_id = '_'.join([chrom, start, end])
        proband, dp = variant['proband ID(GT:AD:DP:GQ:PL)'].split('(')
        dp = int(dp.split(':')[2])

        newline = []
        for h in new_head:
            newline.append(variant[h])
        region,  mappability , avg_dp, large_dp= 'No', '', 'NA', 'NA'
        if variant_id in rep:
            region = 'Yes'
        if variant_id in map_75bp:
            mappability = map_75bp[variant_id]
        if proband in doc:
            avg_dp = float(doc[proband])
            print dp, (dp - avg_dp) /  math.sqrt(avg_dp) 
            large_dp = (dp - avg_dp) /  math.sqrt(avg_dp) 

        w.writerow(newline + [region , mappability, avg_dp, large_dp])
    fw.close() 
shutil.move('temp.csv', filtered_denovo)
os.remove('temp.txt')


