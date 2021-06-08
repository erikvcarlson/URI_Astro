#!/bin/sh 
# autostart of all pipeline data Juergen Ott v0.1 20-10-2017
# v0.2 added a line to show which process belongs to which dataset 20-10-2017
# v0.3 added a new variable to allow for a limited number of
# v1.0 switch to qsub and change the directory structure to have the band first and then the name 19-03-2018
# v2.0 update to CASA 6 01-08-2020
# place in empty directory  and start there

# this script will run L S C X U K A Q guide in the /lustre/aoc/sciops/jott/pipeline/shortSB  directory

# name of the test version. This string will appear in the email that is sent
#export CASAPATH=/lustre/aoc/users/jtobin/casa-6.1.1-6
#export CASAPATH=/home/casa/packages/pipeline/casa-pipeline-prerelease-6.1.1-6.el7
#export PATH=$CASAPATH:$PATH 
#export PATH=$CASAPATH/bin:$PATH 
#export PATH=/lustre/aoc/users/jtobin/pipeline-main.git:$PATH
#export SCIPIPE_HEURISTICS="/lustre/aoc/users/jtobin/pipeline-main.git"

#export CASAPATH=/lustre/aoc/users/jtobin/casa-6.1.1-10
#export CASAPATH=/lustre/aoc/users/jtobin/casa-CAS-13176-2
#export PATH=$CASAPATH:$PATH 
#export PATH=$CASAPATH/bin:$PATH 
#export PATH=/lustre/aoc/users/jtobin/pipeline-release.git:$PATH
#export SCIPIPE_HEURISTICS="/lustre/aoc/users/jtobin/pipeline-release.git"
#export CASAPATH=/lustre/aoc/users/jtobin/casa-6.1.1-10-pipeline-2020.1.0.36/
#export PATH=$CASAPATH:$PATH 
#export PATH=$CASAPATH/bin:$PATH 
#export PATH=/lustre/aoc/users/jtobin/casa-6.1.1-10-pipeline-2020.1.0.36/pipeline:$PATH
#export SCIPIPE_HEURISTICS="/lustre/aoc/users/jtobin/casa-6.1.1-10-pipeline-2020.1.0.36/pipeline"
#PIPEVERSION=$CASAPATH/bin/casa
#export CASAPATH=/lustre/aoc/users/jtobin/casa-6.1.2-7-pipeline-2020.1.0.36/
#export PATH=$CASAPATH:$PATH 
#export PATH=$CASAPATH/bin:$PATH 
#export PATH=/lustre/aoc/users/jtobin/casa-6.1.2-7-pipeline-2020.1.0.36/pipeline:$PATH
#export SCIPIPE_HEURISTICS="/lustre/aoc/users/jtobin/casa-6.1.2-7-pipeline-2020.1.0.36/pipeline"
#PIPEVERSION=$CASAPATH/bin/casa
NAMING='Pipe'


# what bands/DATASETS shall the script run? 


#DATA='L S X C U K A Q guide'
DATA=('15A-033.sb30668039.eb31008641.57226.987913784724')
#DATA='L S C X U K A Q m-S-to-A m-C-X'
#DATA='L C X K Q m-S-to-A m-C-X'
#DATA='m-A-Q m-L-Q m-All'
#DATA='L C X m-S-to-A m-C-X'
#DATA='C'
#DATA='guide'
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
echo '#PBS -M erikvcarlson@gmail.com      # default is submitter'>> run_casa-${i}-${NAMING}.sh 
echo '##PBS -W umask=0117          # default is 0077'  >> run_casa-${i}-${NAMING}.sh 
echo '##PBS -l walltime=3:0:0:0      # default is 100 days.  This set it to 1 day'  >> run_casa-${i}-${NAMING}.sh 
echo '#PBS -q batch      # default is the rhel6 queue, set this to rhel7 for testing'  >> run_casa-${i}-${NAMING}.sh 
#echo 'export CASAPATH='${CASAPATH}''>> run_casa-${i}-${NAMING}.sh
#echo 'export SCIPIPE_HEURISTICS='${SCIPIPE_HEURISTICS}''>> run_casa-${i}-${NAMING}.sh
#echo 'export PATH=$CASAPATH/bin/:$SCIPIPE_HEURISTICS:$PATH'>> run_casa-${i}-${NAMING}.sh
echo '# casas python requires a DISPLAY for matplot, so create a virtual X server'  >> run_casa-${i}-${NAMING}.sh 
#echo 'xvfb-run -d casa --nogui -c /lustre/aoc/observers/nm-4386/run_casa.py
echo 'xvfb-run -d casa -r  6.1.1-13-pipeline-2020.1.0.36 --nologger --nogui -c '${RESULTSDIR}'/pipeline-'${i}'-'${NAMING}'.py' >> run_casa-${i}-${NAMING}.sh


chmod a+rwx run_casa-${i}-${NAMING}.sh

# creating CASA scripts 
echo 'import os' > 'pipeline-'${i}'-'${NAMING}'.py'
echo 'import sys' >> 'pipeline-'${i}'-'${NAMING}'.py'
#echo 'import pipeline' >> 'pipeline-'${i}'-'${NAMING}'.py'
#echo 'import pipeline.recipes.hifv as hifv' > 'pipeline-'${i}'-'${NAMING}'.py'
#echo 'pipeline.initcli()' >> 'pipeline-'${i}'-'${NAMING}'.py'
#echo 'sys.path.insert (0, os.path.expandvars("$SCIPIPE_HEURISTICS"))' >> 'pipeline-'${i}'-'${NAMING}'.py'
echo 'import pipeline.recipereducer' >> 'pipeline-'${i}'-'${NAMING}'.py'
echo "pipeline.recipereducer.reduce(vis=['/lustre/aoc/observers/nm-11325/data/"${i}"'],procedure='procedure_hifv.xml',loglevel='summary')" >>  'pipeline-'${i}'-'${NAMING}'.py'
#echo "myvis = '/lustre/aoc/observers/nm-11325/data/working/"${i}"-Pipe/${i}.ms' " >> 'pipeline-'${i}'-'${NAMING}'.py'
#echo "os.chdir('/lustre/aoc/observers/nm-11325/data/"${i}"-Pipe/working/') " >>  'pipeline-'${i}'-'${NAMING}'.py'
#echo "execfile('/lustre/aoc/observers/nm-11325/Files/source_finder_for_large_datasets.py') " >> 'pipeline-'${i}'-'${NAMING}'.py'

done 





#if [ -e  pipeline-SH0469.sb33049163.eb33055372.57726.33158784722-${NAMING}.py ]
#then
#echo "pipeline.recipereducer.reduce(vis=['/lustre/aoc/observers/nm-11325/data/SH0469.sb33049163.eb33055372.57726.33158784722'],procedure='procedure_hifv.xml',loglevel='summary')" >>  pipeline-SH0469.sb33049163.eb33055372.57726.33158784722-${NAMING}.py
#echo "myvis = '/lustre/aoc/observers/nm-11325/data/SH0469.sb33049163.eb33055372.57726.33158784722-Pipe/SH0469.sb33049163.eb33055372.57726.33158784722.ms' " >>  pipeline-SH0469.sb33049163.eb33055372.57726.33158784722-${NAMING}.py
#echo "os.chdir('/lustre/aoc/observers/nm-11325/data/SH0469.sb33049163.eb33055372.57726.33158784722-Pipe/working/') " >>  pipeline-SH0469.sb33049163.eb33055372.57726.33158784722-${NAMING}.py
#echo "execfile('/lustre/aoc/observers/nm-11325/Files/source_finder_for_large_datasets.py') " >>  pipeline-SH0469.sb33049163.eb33055372.57726.33158784722-${NAMING}.py


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

