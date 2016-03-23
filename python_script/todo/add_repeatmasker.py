import csv
import subprocess

fw = open('temp.txt','w')
with open('Confirmation Core Request.csv','rU') as f:
    r = csv.reader(f)
    _ = r.next()
    head = r.next()
    for line in r:
        variant = dict(zip(head, line))
        chrom, start, end = 'chr' + variant['Chromosome'], variant['Coordinates'], variant['Coordinates']
        fw.write('\t'.join([chrom, start, end, '\n']))
fw.close()    
            
            
cmd = "bedtools intersect -a hg19.rmsk.bed -b temp.txt"
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
repeat = p.communicate()[0]

rep = {}
for hit in repeat.split('\n'):
    if len(  hit.split()) > 0:
        chrom, start, end, repname = hit.split()[:4]
        rep['_'.join([chrom, start, end])] = repname
    

with open('Confirmation Core Request.csv','rU') as f:
    r = csv.reader(f)
    _ = r.next()
    head = r.next()
    fw = open('temp.csv','w')
    w = csv.writer(fw)
    w.writerow(head + ['In repetitive regions','RepName'])
    for line in r:
        variant = dict(zip(head, line))
        chrom, start, end = 'chr' + variant['Chromosome'], variant['Coordinates'], variant['Coordinates']
        region, RepName = 'No', ''
        if '_'.join([chrom, start, end]) in rep:
            RepName = rep['_'.join([chrom, start, end])]
            region = 'Yes'
        w.writerow(line + [region, RepName])
            
    fw.close()   


       	
        