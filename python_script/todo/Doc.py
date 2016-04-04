import os
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

dir1 = 'DoC/'

fw = open(dir1 + 'DoC.txt', 'w')
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

x, y1, y2 = [], [], []
with open(dir1 + 'DoC.txt') as f:
    head = f.readline()
    for line in f:
        sample,mean, dp10, dp15 = line.strip().split()
        x.append(float(mean))
        y1.append(float(dp10))
        y2.append(float(dp15))
        
pdf = PdfPages(dir1 + 'doc.pdf')
fig, ax = plt.subplots( figsize = (8,8), dpi=150)

dp10_scatter = plt.scatter(x,y1,color='red', label='DP10')
dp15_scatter = plt.scatter(x,y2,color='blue', label='DP15')
plt.xlabel('depth mean')
plt.ylabel('percentage')
plt.legend(handles=[dp10_scatter,dp15_scatter])


#axes = plt.gca()
#axes.set_ylim([0,100])

plt.show()
pdf.savefig(bbox_extra_artists=(lgd,), bbox_inches='tight')
pdf.close()
plt.close()