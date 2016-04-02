#!/bin/bash
#$ -cwd -l mem=4G,time=2:: -N buildindex -j y

#This script takes a raw VCF file and performs GATK's variant quality score recalibration
#    InpFil - (required) - Path to VCF file or a list of VCF Files to be recalibrated
#    RefFil - (required) - shell file containing variables with locations of reference files, jar files, and resource directories; see list below for required variables
#    LogFil - (optional) - File for logging progress
#    Flag - B - BadET - prevent GATK from phoning home
#    Help - H - (flag) - get usage information

#list of required vairables in reference file:
# $REF - reference genome in fasta format - must have been indexed using 'bwa index ref.fa'
# $DBSNP - dbSNP vcf from GATK
# $HAPMAP - hapmap vcf from GATKf
# $EXOMPPLN - directory containing exome analysis pipeline scripts
# $GATK - GATK jar file 
# $ETKEY - GATK key file for switching off the phone home feature, only needed if using the B flag

#list of required tools:
# java <http://www.oracle.com/technetwork/java/javase/overview/index.html>
# GATK <https://www.broadinstitute.org/gatk/> <https://www.broadinstitute.org/gatk/download>

## This file also requires exome.lib.sh - which contains various functions used throughout the Exome analysis scripts; this file should be in the same directory as this script

###############################################################

#set default arguments
usage="ExmVC.6.build index.sh -i <InputFile> -r <reference_file> -H
     -i (required) - Path to list of Bam files for variant calling
     -r (required) - shell file containing variables with locations of reference files and resource directories
     -H (flag) - echo this message and exit
"


while getopts i:r:a:l:BH opt; do
    case "$opt" in
        i) InpFil="$OPTARG";;
        r) RefFil="$OPTARG";; 
        H) echo "$usage"; exit;;
  esac
done



#Call the RefFil to load variables
RefFil=`readlink -f $RefFil`
source $RefFil

#Load script library
source $EXOMPPLN/exome.lib.sh #library functions begin "func" #library functions begin "func"

InpFil=`readlink -f $InpFil` #resolve absolute path to bam


if [[ -z "$VcfFil" ]];then VcfFil=`basename $InpFil`; VcfNam=${VcfFil/.list/}; fi # a name for the output files
if [[ -z $LogFil ]]; then LogFil=$VcfNam.GgVCF.log; fi # a name for the log file
VcfFil=$VcfNam.vcf #Output File
GatkLog=$VcfNam.GgVCF.gatklog 
TmpLog=$BamNam.HCgVCF.temp.log #temporary log file
TmpDir=$BamNam.HCgVCF.tempdir; mkdir -p $TmpDir #temporary directory

#Start Log File
ProcessName="Combine VCFs" # Description of the script - used in log
funcWriteStartLog


##Run Joint Variant Calling
StepName="Combine VCFs with GATK"
StepCmd="java -Xmx5G -Djava.io.tmpdir=$TmpDir -jar $GATKJAR
 -T CombineVariants
 -R $REF
 -V $InpFil
 -o $VcfFil
 --genotypemergeoption UNIQUIFY
 -log $GatkLog" #command to be run
funcRunStep
#End Log
funcWriteEndLog

echo 'finished'
