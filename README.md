# bioinformatics research


Pipeline to Call varinats:
seq 1 19 | parallel -j 12 --eta sh $EXOMPPLN/ExmAln.1a.Align_Fastq_to_Bam_with_BWAmem.sh -i fastq_head2.txt -r $EXOMPPLN/WES_Pipeline_References.b37.sh -a {}