import os


gvcf_adr = '/home/local/ARCS/hq2130/WES/PAH/gvcf/'
cmbgvcf_adr = 'combined_gvcf/'
name = cmbgvcf_adr + 'PAH_'
n = 300


samples = []



for e in os.listdir(gvcf_adr):
    if e.endswith('gz'): # samples using mkdup and realigned
        samples.append(gvcf_adr + e)


samples.sort()    

chunk_samples = [samples[i:i+n] for i in xrange(0, len(samples), n)]

for i, s in enumerate(chunk_samples):
    with open(name + str(i) + '.list','w') as fw:
        for e in s:
            fw.write(e+'\n')

