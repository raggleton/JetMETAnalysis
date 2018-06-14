#!/bin/bash
set -u

# INPUT="QCD_Pt_NoJEC_relPtHatCut5_jtptmin4/jra_QCD_Pt_15toInf_NoJEC_newFlav_L1FastJet_fineBinning.root"
# INPUT="QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_nbinsrelrsp_10k/jra_QCD_Pt_15toInf_NoJEC_newFlav_ak4pfchs_L1FastJet_fineBinning_rspRangeLarge.root"
# INPUT="QCD_Pt_NoJEC_relPtHatCut5_jtptmin4/jra_QCD_Pt_15toInf_NoJEC_newFlav_L1FastJet.root"
# INPUT="QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_nbinsrelrsp_10k/jra_QCD_Pt_15to7000_Herwig_NoJEC_newFlav_L1FastJet_fineBinning.root"
# INPUT="QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_nbinsrelrsp_10k/jra_QCD_Pt_15to7000_Herwig_NoJEC_newFlav_L1FastJet_rspRangeLarge.root"
INPUT="QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_nbinsrelrsp_10k/jra_QCD_Pt_15to7000_Herwig_NoJEC_newFlav_L1FastJet_fineBinning_rspRangeLarge_withWeight.root"

OUTPUTDIR="$(dirname $INPUT)"
# OUTPUTDIR="QCD_Pt_NoJEC_relPtHatCut5_jtptmin4"
# OUTPUTDIR="QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_nbinsrelrsp_10k"
# OUTPUTDIR="QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4"

FITMIN=15

# APPEND="_fineBinning_standardMedianErr_meanWhenSmall_min8_allPoints"
APPEND="_standardMedianErr_meanWhenSmall_rspRangeLarge_withWeight_min${FITMIN}_useFitRange"
# APPEND=""

flavors=("" "ud_" "s_" "c_" "b_" "g_")
# flavors=("g_")

declare -a OUTPUTFILES

for flav in "${flavors[@]}"
do
	echo ${flav/_/}
	flavname="${flav/_/}"
	if [ -z "$flavname" ]
	then
		flavname="all"
	fi
	OUTPUTFILE="l2"$APPEND"_"$flavname".root"
	jet_l2_correction_x -input "$INPUT" -algs ak4pfchsl1 -l2l3 true -histMet median -era Fall17_07Aug17"$APPEND"_"$flavname" -outputDir "$OUTPUTDIR" -output "$OUTPUTFILE" -batch true -flavor "$flav" -fitMin "$FITMIN"
	OUTPUTFILES+=("$OUTPUTDIR/$OUTPUTFILE")
done
hadd -f "$OUTPUTDIR/l2_hadd$APPEND.root" "${OUTPUTFILES[@]}"
