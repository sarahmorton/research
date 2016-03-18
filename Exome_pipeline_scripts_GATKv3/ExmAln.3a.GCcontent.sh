#!/bin/bash
#$ -cwd -l mem=8G,time=6:: -N BamMtr 

# This script takes a bam file and generates insert size, GC content and quality score metrics using Picard
#    InpFil - i - (required) - Path to Bam file or a file containing a list of bam files one per line (file names must end ".list")
#    RefFiles - r - (required) - shell file containing variables with locations of reference files, jar files, and resource directories; see list below for required variables
#    LogFil - l - (optional) - File for logging progress
#    Metrics: G, I, Q - (flags) - will run GC bias (G), Insert Size (I) or Quality Distribution (Q); default is to run all metrics, specifying one or more will only run those specified
#    Help - H - (flag) - get usage information

#list of required vairables in reference file:
# $REF - reference genome in fasta format - must have been indexed using 'bwa index ref.fa'
# $PICARD - directory containing Picard jar files

#list of required tools:
# java <http://www.oracle.com/technetwork/java/javase/overview/index.html>
# picard <http://picard.sourceforge.net/> <http://sourceforge.net/projects/picard/files/>

## This file also requires exome.lib.sh - which contains various functions used throughout the Exome analysis scripts; this file should be in the same directory as this script

###############################################################


usage="
ExmAln.3a.Bam_metrics.sh -i <InputFile> -r <reference_file> -l <logfile> -H

     -i (required) - Path to Bam file or \".list\" file containing a multiple paths
     -r (required) - shell file containing variables with locations of reference files and resource directories
     -l (optional) - Log file
     -H (flag) - echo this message and exit
"

#get arguments
while getopts i:r:a:l:H opt; do
    case "$opt" in
        i) InpFil="$OPTARG";;
        r) RefFil="$OPTARG";;
        a) ArrNum="$OPTARG";; 
        l) LogFil="$OPTARG";;
        H) echo "$usage"; exit;;
    esac
done

#check all required paramaters present
if [[ ! -e "$InpFil" ]] || [[ ! -e "$RefFil" ]]; then echo "Missing/Incorrect required arguments"; echo "$usage"; exit; fi

#Call the RefFil to load variables
RefFil=`readlink -f $RefFil`
source $RefFil

#Load script library
source $EXOMPPLN/exome.lib.sh #library functions begin "func"

InpFil=`readlink -f $InpFil` #resolve absolute path to bam
BamFil=$(tail -n+$ArrNum $InpFil | head -n 1) 
BamNam=`basename $BamFil | sed s/.bam$//` #a name to use for the various output files
if [[ -z $LogFil ]];then
    LogFil=$BamNam.BamMetrics.log # a name for the log file
fi
TmpLog=$BamNam.BamMet.temp.log #temporary log file 
TmpDir=$BamNam.BamMet.tempdir; mkdir -p $TmpDir #temporary directory

#Start Log
ProcessName="Start Get GC metrics with Picard" # Description of the script - used in log
funcWriteStartLog

#Get GC metrics with Picard

StepName="Get GC Metrics with Picard" # Description of this step - used in log
StepCmd="java -Xmx4G -Djava.io.tmpdir=$TmpDir -jar  $PICARD/picard.jar CollectGcBiasMetrics 
INPUT=$BamFil
OUTPUT=$BamNam.GCbias_detail
CHART=$BamNam.GCbias.pdf
SUMMARY_OUTPUT=$BamNam.GCsum
REFERENCE_SEQUENCE=$REF2
VALIDATION_STRINGENCY=SILENT
WINDOW_SIZE=200" #command to be run
funcRunStep


#End Log
funcWriteEndLog
