#!/bin/bash

###############################################################

#set default arguments
usage="
ExmAln.5.GenerateBQSRTable.sh -i <InputFile> -r <reference_file> -t <targetfile> -l <logfile> -PABH

     -i (required) - Path to Bam file
     -r (required) - shell file containing variables with locations of reference files and resource directories
     -t (required) - Exome capture kit targets or other genomic intervals bed file (must end .bed for GATK compatability)
     -l (optional) - Log file
     -P (flag) - Call next step of exome analysis pipeline after completion of script
     -A (flag) - AllowMisencoded - see GATK manual
     -B (flag) - Prevent GATK from phoning home
     -H (flag) - echo this message and exit
"

AllowMisencoded="false"
PipeLine="false"
BadET="false"

#get arguments
while getopts i:r:a:l:PABH opt; do
    case "$opt" in
        i) InpFil="$OPTARG";;
        r) RefFil="$OPTARG";; 
        a) ArrNum="$OPTARG";; 
        l) LogFil="$OPTARG";;
        P) PipeLine="true";;
        A) AllowMisencoded="true";;
        B) BadET="true";;
        H) echo "$usage"; exit;;
    esac
done

#check all required paramaters present
if [[ ! -e "$InpFil" ]] || [[ ! -e "$RefFil" ]] ; then echo "Missing/Incorrect required arguments"; echo "$usage"; exit; fi

#Call the RefFil to load variables
RefFil=`readlink -f $RefFil`
source $RefFil

#Load script library
source $EXOMPPLN/exome.lib.sh #library functions begin "func" #library functions begin "func"

InpFil=`readlink -f $InpFil` #resolve absolute path to bam
BamFil=$(tail -n+$ArrNum $InpFil | head -n 1) 
BamNam=`basename $BamFil | sed s/.bam//` #a name to use for the various files
RclFil=$BamNam.printedreads.bam
if [[ -z "$LogFil" ]];then LogFil=$BamNam.PrintReads.log; fi # a name for the log file
GatkLog=$BamNam.gatklog #a log for GATK to output to, this is then trimmed and added to the script log
TmpLog=$BamNam.PrintReads.temp.log #temporary log file 
TmpDir=$BamNam.PrintReads.tempdir; mkdir -p $TmpDir #temporary directory

#Start Log
ProcessName="PrintReads with GATK" # Description of the script - used in log
funcWriteStartLog


#PrintReads
StepName="PrintReads using GATK PrintReads" # Description of this step - used in log
StepCmd="java -Xmx7G -Djava.io.tmpdir=$TmpDir -jar $GATKJAR
 -T PrintReads 
 -R $REF 
 -I $BamFil 
 -fixMisencodedQuals
 -o $RclFil
 -log $GatkLog" #command to be run
funcGatkAddArguments # Adds additional parameters to the GATK command depending on flags (e.g. -B or -F)
funcRunStep

#End Log
funcWriteEndLog

#Clean up
#if [[ -e $RclFil ]] && [[ "$KillFile" == "true" ]]; then rm $BamFil ${BamFil/bam/bai}; fi
