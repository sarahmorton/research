dir1 = '/home/local/ARCS/hq2130/WES/vcf_trio/'

with open('missing_variants') as f:
    missing = set()
    for line in f:
        missing.add(line.strip())

        

import os

fw = open('missing_vcf','w')
for variant in missing:
    
    missing_id, missing_chrom, missing_pos = variant.split(';')
    
    for filename  in os.listdir(dir1):
        proband = filename.split(';')[0]
        if proband == missing_id:
            print filename
            
            
            fw.write('\t'.join([proband,missing_chrom, str(missing_pos) ])+'\n')
            if missing_chrom != 'X':
                missing_chrom = int(missing_chrom)
            missing_pos = int(missing_pos)
            
            with open(dir1 + filename) as f:
                for line in f:
                    if line[0] != '#':
                        chrom, pos = line.split()[:2]
                        pos  = int(pos)
                        if chrom not in {'X','Y'}:
                            chrom = int(chrom)
                            
                            if chrom == missing_chrom and abs(pos - missing_pos) < 1:
                                fw.write(line)
                                break
                            if chrom > missing_chrom:
                                fw.write('not found in exon\n')
                                break
                        else:
                            if chrom == missing_chrom:
                                print missing_pos
                                if abs(pos - missing_pos) < 1:
                                    fw.write(line)
                                    break
                else:
                    fw.write('not found in exon\n')
            break
fw.close()
                        
                    
        
    
        
        