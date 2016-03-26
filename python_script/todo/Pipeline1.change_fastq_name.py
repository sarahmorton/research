import os
import shutil
directory = 'fastq/'
directory = '/home/local/ARCS/hq2130/WES/fastq/temp/'
directory ='/home/local/ARCS/hq2130/CHD_MedExomeKit/fastq/'
directory = '/home/local/ARCS/hq2130/WES/fastq/'

directory  = 'fastq/'
all_id = set()
multi_id = set()

for e in os.listdir(directory):
    if not e.startswith('PCGC'): continue
    if e.endswith('P1.fastq.gz'):
        if not e.startswith('PCGC'):
            ids = e.split('_')[0]
            if ids not in all_id:
                all_id.add(ids)
            else:
                multi_id.add(ids)
            
        else:
            ids = e.split('__')[1]
            if ids not in all_id:
                all_id.add(ids)
            else:
                multi_id.add(ids)

for e in os.listdir(directory):
    if not e.startswith('PCGC'): continue
    if e.endswith('fastq.gz'):
        if  e.startswith('PCGC'):
            ids = e.split('__')[1]
            pair = e.split('_')[-1]
            unique = e.split('_')[-4]
            if ids  in multi_id:
                new_name = '_'.join([ids, unique, pair])
            else:
                new_name = '_'.join([ids, pair])
            print new_name
            shutil.move(directory + e, directory+new_name)
