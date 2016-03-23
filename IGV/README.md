
Variants visualization scripts using IGV. 
Based on scripts from Qiang Huang
the IGV script requires IGV session and remote X window.
On Mac OS, I used [xquartz](http://www.xquartz.org/) to remote the server.

variants file in the format of: CHROM	POS 	BAM_file_name


# Example
sh Generate_IGV_plots.sh -v example/IGV_variants.txt -b example/bam.txt