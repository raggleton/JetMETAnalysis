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
# jet_response_analyzer_x ../config/jra_flavour.config -input $JRAINPUT -output $JRAOUTPUT -algs $ALGOS -flavorDefinition $FLAVDEF -xsection $XSEC -luminosity 35900 -jtptmin 4 -relpthatmax 5 -nbinsrelrsp 100
jet_response_analyzer_x ../config/jra_flavour.config -input $JRAINPUT -output $JRAOUTPUT -algs $ALGOS -flavorDefinition $FLAVDEF -xsection $XSEC -luminosity 35900 -jtptmin 4 -relpthatmax 5 -nbinsrelrsp 10000  -relrspmax 6 -useweight $WEIGHT
# jet_response_analyzer_x ../config/jra.config -input $JRAINPUT -doflavor true -algs ak4pfchs:0.2 -output $JRAOUTPUT -xsection $XSEC -luminosity 35900

