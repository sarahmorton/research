import gzip
import os
import shutil

dir1 = '/home/local/ARCS/hq2130/WES/gvcf_renamed/'
dir2 = '/home/local/ARCS/hq2130/WES/gvcf/'
dir3 = '/home/local/ARCS/hq2130/WES/temp/'

processed = set()
for f in os.listdir(dir1):
    if f.endswith('gz'):
        if 's1' in f or 'fa' in f or 'mo' in f:
            name = '.'.join(f.split('.g.vcf.gz')[:1])
    
        else:
            name = f.split('.')[0]
        processed.add(name)

print len(processed)
fw = open('moved_vcf','w')
for f in os.listdir(dir2):
    if f.endswith('gz'):
        if 's1' in f or 'fa' in f or 'mo' in f:
            name = '.'.join(f.split('.g.vcf.gz')[:1])
    
        else:
           name = f.split('.')[0]
        if name in processed : continue
        f1 = gzip.open(dir2+f)
        for line in f1:
            if line.startswith('#CHROM'):
                gvcf_name = line.strip().split()[-1]
                break
        f1.close()
        
        if gvcf_name != name:
            print gvcf_name , name
            print 'change', f
	    fw.write(f+'\n')
            f1 = gzip.open(dir2+f)
            f2 = gzip.open(dir3+f, 'w')
            for line in f1:
                if line.startswith('#CHROM'):
                    new_line = line.strip().split()
                    new_line[-1] = name
                    line = '\t'.join(new_line)+'\n'
                f2.write(line)
            f1.close()
            f2.close()
                
fw.close()
