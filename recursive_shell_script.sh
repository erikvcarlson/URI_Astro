#!/bin/sh 
# autostart of all pipeline data Juergen Ott v0.1 20-10-2017
# v0.2 added a line to show which process belongs to which dataset 20-10-2017
# v0.3 added a new variable to allow for a limited number of
# v1.0 switch to qsub and change the directory structure to have the band first and then the name 19-03-2018
# v2.0 update to CASA 6 01-08-2020
# place in empty directory  and start there


NAMING='Pipe'

#Greater than one Measurement Set Example 
# DATA=('15A-033.sb30668039.eb31008641.57226.987913784724' '16B-082.sb32697585.eb32929724.57667.505691134254')
DATA=('12B-230_sb13779883_1.56249.3994171875')



# name the CASA startup string (note that --nogui and --nologger are automatically added)
RESULTSDIR=`pwd`

for i in ${DATA[@]}
do

mkdir $RESULTSDIR/${i}-${NAMING}
mkdir $RESULTSDIR/${i}-${NAMING}/working
# creating the qsub run files 
	echo ${i}
echo '#!/bin/sh' > run_casa-${i}-${NAMING}.sh 

echo '# Set PBS Directives' >> run_casa-${i}-${NAMING}.sh 
echo '# Lines starting with "#PBS", before any shell commands are' >> run_casa-${i}-${NAMING}.sh 
echo '# interpreted as command line arguments to qsub.' >> run_casa-${i}-${NAMING}.sh 
echo '# Dont put any commands before the #PBS options or they will not work.' >> run_casa-${i}-${NAMING}.sh 
#'
echo '#PBS -V    # Export all environment variables from the qsub commands environment to the batch job.' >> run_casa-${i}-${NAMING}.sh 
#Use approximately 10% of the measurement set
echo '#PBS -l pmem=32gb,pvmem=32gb       # Amount of memory needed by each process (ppn) in the job.' >> run_casa-${i}-${NAMING}.sh 
echo '## next: working directory' >> run_casa-${i}-${NAMING}.sh 
echo '#PBS -d '${RESULTSDIR}'/'${i}-${NAMING}'/working  # Working directory (PBS_O_WORKDIR)' >> run_casa-${i}-${NAMING}.sh   
echo '#PBS -m bea                 # Send mail on begin, end and abort' >> run_casa-${i}-${NAMING}.sh 
echo '# Because these start with "##PBS", they are not read by qsub.' >> run_casa-${i}-${NAMING}.sh 
echo '##PBS -l mem="16gb"    # physmem used by job. Ignored if NUM_NODES > 1. Wont kill job.' >> run_casa-${i}-${NAMING}.sh 
echo '##PBS -l pmem="16gb"    # physmem used by any process. Wont kill job.' >> run_casa-${i}-${NAMING}.sh 
echo '##PBS -l vmem="16gb"    # physmem + virtmem used by job. Kills job if exceeded.' >> run_casa-${i}-${NAMING}.sh 
echo '##PBS -l pvmem="16gb"    # physmem + virtmen used by any process. Kills job if exceeded.' >> run_casa-${i}-${NAMING}.sh 
echo '##PBS -l nodes=1:ppn=4       # default is 1 core on 1 node' >> run_casa-${i}-${NAMING}.sh 
#change the below line to your email address. 
echo '#PBS -M erikvcarlson@nrao.edu      # default is submitter'>> run_casa-${i}-${NAMING}.sh 
echo '##PBS -W umask=0117          # default is 0077'  >> run_casa-${i}-${NAMING}.sh 
echo '##PBS -l walltime=3:0:0:0      # default is 100 days.  This set it to 1 day'  >> run_casa-${i}-${NAMING}.sh 
echo '#PBS -q batch      # default is the rhel6 queue, set this to rhel7 for testing'  >> run_casa-${i}-${NAMING}.sh 
echo '# casas python requires a DISPLAY for matplot, so create a virtual X server'  >> run_casa-${i}-${NAMING}.sh 
#change the below line to run different versions of the pipeline
echo 'xvfb-run -d casa -r  6.1.1-13-pipeline-2020.1.0.36 --nologger --nogui -c '${RESULTSDIR}'/pipeline-'${i}'-'${NAMING}'.py' >> run_casa-${i}-${NAMING}.sh


chmod a+rwx run_casa-${i}-${NAMING}.sh

# creating CASA scripts 
echo 'import os' > 'pipeline-'${i}'-'${NAMING}'.py'
echo 'import sys' >> 'pipeline-'${i}'-'${NAMING}'.py'

echo 'import pipeline.recipereducer' >> 'pipeline-'${i}'-'${NAMING}'.py'

#change the below line to point to the location where you will be placing the data
echo "pipeline.recipereducer.reduce(vis=['/lustre/aoc/observers/nm-11325/data/"${i}"'],procedure='procedure_hifv.xml',loglevel='summary')" >>  'pipeline-'${i}'-'${NAMING}'.py'


done 

#fi


TESTMASTER=`uname -a`
if [[ ${TESTMASTER} == *"-master"* ]] ; then
for i in ${DATA[@]} 
do
echo ${i}'-'${NAMING}':'
qsub run_casa-${i}-${NAMING}.sh 
done

else
    echo 'Running on: '${TESTMASTER}
    echo 'Start the script on nmpost-master or cvpost-master! Exiting...'
    
fi

