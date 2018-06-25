#!/bin/bash -e

# only for pt-binned pythia samples

filedir="QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_nbinsrelrsp_10k"
# filedir="DYJets_HT_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k"
# filedir="QCD_HT_NoJEC_relPtHatCut5_jtptmin4_nbinsrelrsp_10k"
# filedir="GJet_HT_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k"

# append="_standardMedianErr_meanWhenSmall_rspRangeLarge_fitMin15_useFitRange"
# append="_standardMedianErr_meanWhenSmall_relRspMax2_fitMin15_useFitRange_ptGenMin10_fewerBins"
# append="_standardMedianErr_meanWhenSmall_relRspMax2_fitMin15_useFitRange_ptGenMin10_fewerBins_jtnefLt0p7_jtcefLt0p7_jtmufLt0p7_nrefmax2"
# append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_oppositeJEC_j2OvZLt0p3_nrefmax1_drmin0p8_ptGenOverlap10"
# append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_abseta_j2OvZLt0p3_nrefmax1_drmin0p8_ptGenOverlap10_emugCandOverlapGt0p5" 
# append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_j2OvZLt0p3_nrefmax1_drmin0p8_ptGenOverlap10_emugCandOverlapGt0p5"
# append="_relRspMax2_relPtHatMax3p5_ptGenMin10_absEta_alpha0p3_nrefmax1_drmin0p8_ptGenOverlap10_findZ"
# append="_relRspMax2_relPtHatMax3p5_ptGenMin10_absEta_noDPhiCut_alpha0p3_nrefmax1_drmin0p8_ptGenOverlap10_findZ"
# append="_relRspMax2_relPtHatMax3p5_ptGenMin10_absEta_alpha0p3_nrefmax1_drmin0p8_ptGenOverlap10_findGamma"
# append="_relRspMax2_relPtHatMax3p5_ptGenMin10_absEta_noDPhiCut_alpha0p3_nrefmax1_drmin0p8_ptGenOverlap10_findGamma"
# append="_relRspMax2_relPtHatMax3p5_ptGenMin10_absEta_nrefmax2_drmin0p8_ptGenOverlap10"
# append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_j2OvZLt0p3_nrefmax1_drmin0p8_ptGenOverlap10_egCandOverlapGt0p5"
# append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_abseta_nrefmax2_drmin0p8_ptGenOverlap10" 
# append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_abseta_nrefmax2_drmin0p8_ptGenOverlap10_emugCandOverlapGt0p5" 
# append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_abseta_nrefmax2_drmin0p8_ptGenOverlap10" 
# append="_relRspMax2_ptGenMin10_jtnefLt99_jtcefLt99_jtmufLt99_centralEFcuts_unscaleEF_nrefmax2_drmin0p8_ptGenOverlap10" 
# append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_abseta_j2OvZLt0p3_nrefmax1_drmin0p8_ptGenOverlap10_egCandOverlapGt0p5" 

# _emugCandOverlapGt0p5"
# append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_oppositeJEC_nrefmax2_drmin0p8_ptGenOverlap10"
# append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_nrefmax2_drmin0p8_ptGenOverlap10"
# append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_nrefmax1"

flavs=("ud" "s" "c" "b" "g")

for flav in ${flavs[@]}
do
	# target="${filedir}"/Closure_ak4pfchsl1QCD_Pt_15toInf_NoJEC_newFlav_${append}_${flav}.root
	# target="${filedir}"/Closure_ak4pfchsl1DYJetsToLL_HT-70toInf_NoJEC_newFlav_${append}_${flav}.root
	# target="${filedir}"/Closure_ak4pfchsl1QCD_HT-50toInf_NoJEC_newFlav_${append}_${flav}.root
	target="${filedir}"/Closure_ak4pfchsl1GJets_HT40ToInf_NoJEC_newFlav_${append}_${flav}.root
	if [ -f $target ];
	then
		rm $target
	fi
	# hadd -f "$target" ${filedir}/Closure_ak4pfchsl1QCD_Pt_*_NoJEC_newFlav_${append}_${flav}.root
	# hadd -f "$target" ${filedir}/Closure_ak4pfchsl1DYJetsToLL_HT-*_NoJEC_newFlav_${append}_${flav}.root
	# hadd -f "$target" ${filedir}/Closure_ak4pfchsl1QCD_HT*_NoJEC_newFlav_${append}_${flav}.root
	hadd -f "$target" ${filedir}/Closure_ak4pfchsl1GJets_*_NoJEC_newFlav_${append}_${flav}.root
done
