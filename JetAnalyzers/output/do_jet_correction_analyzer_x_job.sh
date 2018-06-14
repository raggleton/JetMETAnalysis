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
#$ -l h_fsize=3G
set -x
set -e
set -u
cd /nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output
# these hacks are because i can't figure out how to pass "" properly from cmd line
# to this to program
IFP=""
if [[ ! -z $INPUTFILEPATH ]]
then
	IFP="-inputFilePath $INPUTFILEPATH"
fi

JID=""
if [[ ! -z $JETID ]]
then 
	JID="-jetID $JETID"
fi

jet_correction_analyzer_x $IFP -inputFilename $INPUTFILENAME \
	-outputDir $ODIR -suffix $SUFFIX -algs $ALGOS \
	-levels 2 -doflavor true -pdgid $PDGID -xsection $XSEC -luminosity 35900 \
	-nrefmax $NREFMAX -ptgenmin 10 -ptrawmin 4 -relpthatmax 3.5 -relrspmax 2 -useweight $WEIGHT \
	-alphamax $ALPHA -pfCandIds $PFPID -pfCandPtMin $PFPT -pfCandDr $PFDR -efmax $EFMAX $JID\
	-findZ $FINDZ -findGamma $FINDGAMMA \
	-drmin $DRMIN -drmax $DRMAX -era $ERA -path $MYPATH

