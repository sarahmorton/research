# -*- coding: utf-8 -*-
from __future__ import division
import csv
import scipy.stats
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
    

with open('PAH.summary') as f:
    xxx= f.readline()
    sample = f.readline().split()
    print len(sample)
    
    for line in f:
        info = line.strip().split('\t')
        xxx = 'known Ti/TV ratio'
        print info[0]
        if info[0] == xxx:
            hist = map(float,info[2:])
            print 'mean:' + str(np.round(np.mean(hist),decimals = 3))
            print 'median:'+ str(np.round( np.median(hist),decimals = 3))
            pdf = PdfPages('x.pdf')


            fig, ax = plt.subplots(dpi = 100)
            rects1 = ax.hist(hist, bins = 50)
      

            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')
            ax.set_title('coding '+xxx+'\n'+ 'mean:' + str(np.round(np.mean(hist),decimals = 3))+' '+\
            'median:'+ str(np.round( np.median(hist),decimals = 3)))
            plt.show()
            plt.tight_layout()
            
            pdf.savefig(bbox_inches='tight')
            #plt.subplots_adjust(left=0.5, right=0.9, top=0.9, bottom=0.1)
            #plt.close()
            pdf.close()
            plt.close()

            break
