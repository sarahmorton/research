# bioinformatics research


Pipeline to Call varinats:
seq 1 19 | parallel -j 12 --eta sh $EXOMPPLN/ExmAln.1a.Align_Fastq_to_Bam_with_BWAmem.sh -i fastq_head2.txt -r $EXOMPPLN/WES_Pipeline_References.b37.sh -a {}

To do:
finish pipeline part
	add if process multi fastq line part


finish qc part --- ash's hist plots
			   --- doc part 
			   --- my de novo counts

finish analysis part
			--- burden
			--- add mapp and reapmask


How to mount folder from home(through one hidden ssh)?
using transmit
http://superuser.com/questions/49838/how-to-transfer-files-when-given-two-ssh-accounts

