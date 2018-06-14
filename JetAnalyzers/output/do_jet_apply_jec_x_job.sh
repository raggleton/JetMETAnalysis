#!/bin/bash
#$ -l os=sld6
#$ -l site=hh
#$ -P unihh2
#$ -cwd
##You need to set up sframe
#$ -V
##email Notification
#$ -m eas
#$ -M robin.aggleton@desy.de
##CPU memory
#$ -l h_vmem=3G
##DISK memory
#$ -l h_fsize=6G
cd /nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output
sleep 10
DUMMY=$INPUT
echo $DUMMY
sleep 10
jet_apply_jec_x -input $INPUT -output $OUTPUT -algs $ALGOS -levels $LEVELS -era $ERA -jecpath $JECPATH -L1FastJet true -saveitree false

