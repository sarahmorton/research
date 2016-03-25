

import os

dir1 = 'DoC/'
fw = open('target2_doc.txt', 'w')
for e in os.listdir(dir1):
    if e.endswith('sample_summary'):
        with open(dir1+e) as f:
            head = f.readline()
            lst = f.readline().strip().split()
            sample = lst[0]
            d_mean = lst[2]
            dp10 = lst[-2]
            dp15 = lst[-1]
            fw.write('\t'.join([sample, d_mean, dp10, dp15, '\n']))
fw.close()