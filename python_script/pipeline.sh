

python $EXOMPY/adhoc.1.vcf_to_trio.py -p CDH0219.ped -v MGH_VQSR.vcf

python $EXOMPY/adhoc.2.trio_to_denovo.py -v vcf_trio

python $EXOMPY/adhoc.3.variants_to_csv.py -v vcf_rare_denovo -o CDH_denovo.csv

python $EXOMPY/adhoc.4.denovo_filter.py -o CDH_denovo.csv
