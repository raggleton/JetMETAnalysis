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
#$ -l h_vmem=4G
##DISK memory
#$ -l h_fsize=2G
cd /nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output
jet_l2_correction_x -input "$INPUT" -algs "$ALGOS" -l2l3 true -histMet median -era "$ERA" -outputDir "$OUTPUTDIR" -output "$OUTPUTFILE" -batch true -flavor "$PDGID" -fitMin "$FITMIN"

