import gzip
import os
import shutil


dir2 = '/home/local/ARCS/hq2130/WES/'


for f in os.listdir('.'):
    if f.endswith('gz'):
        if 's1' in f or 'fa' in f or 'mo' in f:
            name = '.'.join(f.split('.g.vcf.gz')[:1])
    
        else:
           name = f.split('.')[0]
        f1 = gzip.open(dir2+f)
        for line in f1:
            if line.startswith('#CHROM'):
                gvcf_name = line.strip().split()[-1]
                break
        f1.close()
        
        if gvcf_name != name:
            print gvcf_name , name
            print 'change', f
            f1 = gzip.open(dir2+f)
            f2 = open('temp/'+f, 'w')
            for line in f1:
                if line.startswith('#CHROM'):
                    new_line = line.strip().split()
                    new_line[-1] = name
                    line = '\t'.join(new_line)+'\n'
                f2.write(line)
            f1.close()
            f2.close()

