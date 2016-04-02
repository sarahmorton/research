https://github.com/macarthur-lab/igv_plotter
https://github.com/chrisamiller/igvScreenshot


Variants visualization scripts using IGV. 
Based on scripts from Qiang Huang.

the IGV script requires IGV session and remote X window. On Mac OS X, I used [xquartz](http://www.xquartz.org/) to remote connect the server.

variants file in the format of: CHROM	POS 	BAM_file_name


# Example
sh Generate_IGV_plots.sh -v example/IGV_variants.txt -b example/bam.txt