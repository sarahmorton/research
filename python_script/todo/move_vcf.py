import gzip
import os
import shutil

dir1 = '/ifs/scratch/c2b2/ys_lab/hq2130/gvcf/'
dir2 = '/ifs/scratch/c2b2/ys_lab/hq2130/gvcf_hongjian/'
dir3 = '/ifs/scratch/c2b2/ys_lab/hq2130/temp/'
fw = open('moved_vcf','w')
for f in os.listdir(dir1):
    if f.endswith('gz'):
        
        name = f.split('.g.vcf.gz')[0]
        f1 = gzip.open(dir1+f)
        for line in f1:
            if line.startswith('#CHROM'):
                gvcf_name = line.strip().split()[-1]
                break
        f1.close()
        if gvcf_name == name:
            print f
            shutil.move(dir1 + f, dir2 + f)
        else:
            print 'change', f
	    fw.write(f+'\n')
            f1 = gzip.open(dir1+f)
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
