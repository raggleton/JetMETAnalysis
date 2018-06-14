#!/usr/bin/env python


import subprocess


items = [
# dict(
#     filedir="QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_nbinsrelrsp_10k",
#     # append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_abseta_nrefmax2_drmin0p8_ptGenOverlap10",
#     append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_abseta_nrefmax2_drmin0p8_ptGenOverlap10_emugCandOverlapGt0p5",
#     stem="Closure_ak4pfchsl1QCD_Pt_15toInf_NoJEC_newFlav",
#     title="QCD MC"
# ),
# dict(
#     filedir="QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k",
#     # append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_nrefmax2_drmin0p8_ptGenOverlap10",
#     # append="_relRspMax2_ptGenMin10_jtnefLt99_jtcefLt99_jtmufLt99_centralEFcuts_unscaleEF_abseta_nrefmax2_drmin0p8_ptGenOverlap10",
#     append="_relRspMax2_relPtHatMax3p5_ptGenMin10_absEta_noDPhiCut_nrefmax2_drmin0p8_ptGenOverlap10",
#     # append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_abseta_nrefmax2_drmin0p8_ptGenOverlap10_emugCandOverlapGt0p5",
#     stem="Closure_ak4pfchsl1QCD_Pt_15toInf_NoJEC_newFlav",
#     title="QCD MC"
# ),

# dict(
#     filedir="QCD_HT_NoJEC_relPtHatCut5_jtptmin4_nbinsrelrsp_10k",
#     append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_nrefmax2_drmin0p8_ptGenOverlap10",
#     stem="Closure_ak4pfchsl1QCD_HT-50toInf_NoJEC_newFlav",
#     title="QCD MC"
# ),
dict(
    filedir="DYJets_HT_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k",
    # append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_abseta_j2OvZLt0p3_nrefmax1_drmin0p8_ptGenOverlap10", #_emugCandOverlapGt0p5",
    # append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_j2OvZLt0p3_nrefmax1_drmin0p8_ptGenOverlap10_emugCandOverlapGt0p5",
    append="_relRspMax2_relPtHatMax3p5_ptGenMin10_absEta_noDPhiCut_alpha0p3_nrefmax1_drmin0p8_ptGenOverlap10_findZ",
    stem="Closure_ak4pfchsl1DYJetsToLL_HT-70toInf_NoJEC_newFlav",
    title='DY+Jets MC'
),
# dict(
#     filedir="TT_Pythia_NoJEC_relPtHatCut5_jtptmin4_nbinsrelrsp_10k",
#     append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_nrefmax7_drmin0p8_ptGenOverlap10",
#     stem="Closure_ak4pfchsl1TT_Pythia_NoJEC_newFlav",
#     title="t#bar{t} MC"
# ),
# dict(
#     filedir="QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_nbinsrelrsp_10k",
#     # append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_abseta_nrefmax2_drmin0p8_ptGenOverlap10",
#     append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_abseta_nrefmax2_drmin0p8_ptGenOverlap10_emugCandOverlapGt0p5",
#     stem="Closure_ak4pfchsl1QCD_Pt_15to7000_Herwig_NoJEC_newFlav",
#     title='QCD MC'
# ),
# ]event.items = [
# dict(
#     filedir="QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k",
#     # append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_abseta_nrefmax2_drmin0p8_ptGenOverlap10",
#     # append="_relRspMax2_ptGenMin10_jtnefLt99_jtcefLt99_jtmufLt99_centralEFcuts_unscaleEF_nrefmax2_drmin0p8_ptGenOverlap10",
#     append="_relRspMax2_relPtHatMax3p5_ptGenMin10_absEta_nrefmax2_drmin0p8_ptGenOverlap10",
#     stem="Closure_ak4pfchsl1QCD_Pt_15to7000_Herwig_NoJEC_newFlav",
#     title='QCD MC'
# ),
dict(
    filedir="GJet_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k",
    # append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_abseta_j2OvZLt0p3_nrefmax1_drmin0p8_ptGenOverlap10", #_egCandOverlapGt0p5",
    # append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_j2OvZLt0p3_nrefmax1_drmin0p8_ptGenOverlap10_egCandOverlapGt0p5",
    append="_relRspMax2_relPtHatMax3p5_ptGenMin10_absEta_noDPhiCut_alpha0p3_nrefmax1_drmin0p8_ptGenOverlap10_findGamma",
    stem="Closure_ak4pfchsl1GJets_Herwig_NoJEC_newFlav",
    title='#gamma+jets MC'
),
# dict(
#     filedir="TT_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_nbinsrelrsp_10k",
#     append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_nrefmax7_drmin0p8_ptGenOverlap10_emuCandOverlapGt0p5",
#     stem="Closure_ak4pfchsl1TT_Herwig_NoJEC_newFlav",
#     title="t#bar{t} MC"
# ),
# dict(
#     filedir="Dijet_Powheg_Pythia_NoJEC_relPtHatCut5_jtptmin4_nbinsrelrsp_10k",
#     append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_nrefmax3_drmin0p8_ptGenOverlap10",
#     stem="Closure_ak4pfchsl1Dijet_Powheg_Pythia_NoJEC_newFlav",
#     title="Dijet"
# ),
dict(
    filedir="DYJets_MG_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k",
    # append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_abseta_j2OvZLt0p3_nrefmax1_drmin0p8_ptGenOverlap10", #_emugCandOverlapGt0p5",
    # append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_puMin35_j2OvZLt0p3_nrefmax1_drmin0p8_ptGenOverlap10_emugCandOverlapGt0p5",
    append="_relRspMax2_relPtHatMax3p5_ptGenMin10_absEta_noDPhiCut_alpha0p3_nrefmax1_drmin0p8_ptGenOverlap10_findZ",
    stem="Closure_ak4pfchsl1DYJetsToLL_MG_Herwig_NoJEC_newFlav",
    title='DY+Jets MC'
),
dict(
    filedir="GJet_HT_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k",
#     # append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_abseta_j2OvZLt0p3_nrefmax1_drmin0p8_ptGenOverlap10", #_emugCandOverlapGt0p5",
    # append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_j2OvZLt0p3_nrefmax1_drmin0p8_ptGenOverlap10_egCandOverlapGt0p5",
    append="_relRspMax2_relPtHatMax3p5_ptGenMin10_absEta_noDPhiCut_alpha0p3_nrefmax1_drmin0p8_ptGenOverlap10_findGamma",
    stem="Closure_ak4pfchsl1GJets_HT40ToInf_NoJEC_newFlav",
    title='#gamma+Jets MC'
),
dict(
    filedir="DYJets_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k",
    # append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_abseta_j2OvZLt0p3_nrefmax1_drmin0p8_ptGenOverlap10", #_emugCandOverlapGt0p5",
    # append="_relRspMax2_ptGenMin10_jtnefLt0p8_jtcefLt0p8_jtmufLt0p8_centralEFcuts_unscaleEF_puMin35_j2OvZLt0p3_nrefmax1_drmin0p8_ptGenOverlap10_emugCandOverlapGt0p5",
    append="_relRspMax2_relPtHatMax3p5_ptGenMin10_absEta_noDPhiCut_alpha0p3_nrefmax1_drmin0p8_ptGenOverlap10_findZ",
    stem="Closure_ak4pfchsl1DYJetsToLL_Herwig_NoJEC_newFlav",
    title='DY+Jets MC'
),
][-1:]

flavs = ["ud", "s", "c", "b", "g"][:]

for item_dict in items:
    for flav in flavs:
        item_dict['flav'] = flav
        cmd = 'jet_draw_closure_x -doPt true -doEta true '\
            '-doRatioPt false -doRatioEta false -ptcl false '\
            '-histMet median -outputFormat ".pdf" '\
            '-filename "{filedir}/{stem}_{append}_{flav}" '\
            '-outputFilename "Plots_{stem}_{append}_{flav}.root" '\
            '-title "{title} ({flav} jets)" '\
            '-outputDir "{filedir}/Plots_{stem}_{append}_{flav}"'.format(**item_dict)
        print cmd
        subprocess.check_call(cmd, shell=True)
