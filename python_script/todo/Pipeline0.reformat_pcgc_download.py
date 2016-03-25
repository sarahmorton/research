import os 
import shutil
filename = "/home/local/ARCS/hq2130/WES/fastq/pcgc_download.sh"

from collections import defaultdict

add = defaultdict(lambda : [])

with open(filename) as f:
    for line in f:
        if line.startswith('fetch '):
            print line 
            if len(line.split('__')) > 0:
		ids = line.split('__')[1]
            	add[ids].append(line)
print      add           
fw = open('/home/local/ARCS/hq2130/WES/fastq/download.sh','w')    
with open(filename) as f:
    for line in f:
        if line.startswith('fetch '):
            break
        else:
            fw.write(line)
for ids, adds in add.items():
    for e in adds:
        fw.write(e)
fw.write('exit 0\n')
fw.close()
