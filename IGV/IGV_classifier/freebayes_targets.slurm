samtools view $1 -L $3.bed -T Homo_sapiens_assembly38.fasta -b | \
        freebayes --stdin -f Homo_sapiens_assembly38.fasta --vcf $2.denovo.fb.vcf
