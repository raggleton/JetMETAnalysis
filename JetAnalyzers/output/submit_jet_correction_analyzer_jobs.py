#!/usr/bin/env python


import os
import subprocess
from glob import glob
from collections import OrderedDict
from itertools import chain


ORIGINAL_ERA_DIR = "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JECDatabase/textFiles/Summer16_07Aug2017_V15_MC"
PYTHIA_ERA_DIR = "QCD_Pt_NoJEC_relPtHatCut2p5_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_HadronParton_nbinsrelrsp_10k_fineBinning_etaPlusMinus"
HERWIG_ERA_DIR = "QCD_Pt_Herwig_NoJEC_relPtHatCut2p5_jtptmin4_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_HadronParton_nbinsrelrsp_10k_fineBinning_etaPlusMinus"

# QCD_PT_INPUT_DIR = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF"
# QCD_PT_INPUT_DIR = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10"
QCD_PT_INPUT_DIR = "QCD_Pt_NoJEC_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC"
QCD_HERWIG_INPUT_DIR = "QCD_Pt_Herwig_NoJEC_jtptmin4_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC"

# DY_INPUT_DIR = "DYJets_HT_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10"
# GJETS_HT_INPUT_DIR = "GJet_HT_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10"

# QCD_PT_OUTPUT_DIR = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k"
QCD_PT_OUTPUT_DIR = "QCD_Pt_NoJEC_relPtHatCut2p5_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_HadronParton_nbinsrelrsp_10k_fineBinning_etaPlusMinus"
QCD_HERWIG_OUTPUT_DIR = "QCD_Pt_Herwig_NoJEC_relPtHatCut2p5_jtptmin4_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_HadronParton_nbinsrelrsp_10k_fineBinning_etaPlusMinus"
QCD_HT_OUTPUT_DIR = "QCD_HT_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k"
DY_HT_OUTPUT_DIR = "DYJets_HT_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k"
GJETS_HT_OUTPUT_DIR = "GJet_HT_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k"

QCD_NREFMAX = 2
DY_NREFMAX = 1
TT_NREFMAX = 7

alpha = 0.3

DUMMY_PF_ID = "99999"

DY_PF_PID = "2 3 4"
DY_PF_PID = DUMMY_PF_ID
DY_PF_PT = 5
PF_DR = 0.4

GJETS_PF_PID = "2 4" # 2 = e, 3 = mu, 4 = gamma
GJETS_PF_PID = DUMMY_PF_ID

# run on ntuples
infos_qcd_pythia = [
# QCD PT BINNED
# ==============================================================================
# {
#     "name": "QCD_Pt_15to30_NoJEC_newFlav",
#     "input": "%s/QCD_Pt_15to30_NoJEC_newFlav/" % QCD_PT_INPUT_DIR,
#     "xsec": 1837410000,
#     "output_dir": QCD_PT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_Pt_30to50_NoJEC_newFlav",
#     "input": "%s/QCD_Pt_30to50_NoJEC_newFlav/" % QCD_PT_INPUT_DIR,
#     "xsec": 140932000,
#     "output_dir": QCD_PT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_Pt_50to80_NoJEC_newFlav",
#     "input": "%s/QCD_Pt_50to80_NoJEC_newFlav/" % QCD_PT_INPUT_DIR,
#     "xsec": 19204300,
#     "output_dir": QCD_PT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_Pt_80to120_NoJEC_newFlav",
#     "input": "%s/QCD_Pt_80to120_NoJEC_newFlav/" % QCD_PT_INPUT_DIR,
#     "xsec": 2762530,
#     "output_dir": QCD_PT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
{
    "name": "QCD_Pt_120to170_NoJEC_newFlav",
    "input": "%s/QCD_Pt_120to170_NoJEC_newFlav/" % QCD_PT_INPUT_DIR,
    "xsec": 471100,
    "output_dir": QCD_PT_OUTPUT_DIR,
    "era_dir": PYTHIA_ERA_DIR,
    "nrefmax": QCD_NREFMAX,
},
# {
#     "name": "QCD_Pt_170to300_NoJEC_newFlav",
#     "input": "%s/QCD_Pt_170to300_NoJEC_newFlav/" % QCD_PT_INPUT_DIR,
#     "xsec": 117276,
#     "output_dir": QCD_PT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_Pt_300to470_NoJEC_newFlav",
#     "input": "%s/QCD_Pt_300to470_NoJEC_newFlav/" % QCD_PT_INPUT_DIR,
#     "xsec": 7823,
#     "output_dir": QCD_PT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_Pt_470to600_NoJEC_newFlav",
#     "input": "%s/QCD_Pt_470to600_NoJEC_newFlav/" % QCD_PT_INPUT_DIR,
#     "xsec": 648.2,
#     "output_dir": QCD_PT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_Pt_600to800_NoJEC_newFlav",
#     "input": "%s/QCD_Pt_600to800_NoJEC_newFlav/" % QCD_PT_INPUT_DIR,
#     "xsec": 186.9,
#     "output_dir": QCD_PT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_Pt_800to1000_NoJEC_newFlav",
#     "input": "%s/QCD_Pt_800to1000_NoJEC_newFlav/" % QCD_PT_INPUT_DIR,
#     "xsec": 32.293,
#     "output_dir": QCD_PT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_Pt_1000to1400_NoJEC_newFlav",
#     "input": "%s/QCD_Pt_1000to1400_NoJEC_newFlav/" % QCD_PT_INPUT_DIR,
#     "xsec": 9.4183,
#     "output_dir": QCD_PT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_Pt_1400to1800_NoJEC_newFlav",
#     "input": "%s/QCD_Pt_1400to1800_NoJEC_newFlav/" % QCD_PT_INPUT_DIR,
#     "xsec": 0.84265,
#     "output_dir": QCD_PT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_Pt_1800to2400_NoJEC_newFlav",
#     "input": "%s/QCD_Pt_1800to2400_NoJEC_newFlav/" % QCD_PT_INPUT_DIR,
#     "xsec": 0.114943,
#     "output_dir": QCD_PT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_Pt_2400to3200_NoJEC_newFlav",
#     "input": "%s/QCD_Pt_2400to3200_NoJEC_newFlav/" % QCD_PT_INPUT_DIR,
#     "xsec": 0.0068298,
#     "output_dir": QCD_PT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_Pt_3200toInf_NoJEC_newFlav",
#     "input": "%s/QCD_Pt_3200toInf_NoJEC_newFlav/" % QCD_PT_INPUT_DIR,
#     "xsec": 0.0001654,
#     "output_dir": QCD_PT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# QCD HT BINNED
# ==============================================================================
# {
#     "name": "QCD_HT50to100_NoJEC_newFlav",
#     "input": "QCD_HT_NoJEC_relPtHatCut5_jtptmin4/QCD_HT50to100_NoJEC_newFlav/",
#     "xsec": 246300000.0,
#     "output_dir": QCD_HT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_HT100to200_NoJEC_newFlav",
#     "input": "QCD_HT_NoJEC_relPtHatCut5_jtptmin4/QCD_HT100to200_NoJEC_newFlav/",
#     "xsec": 27990000.0000,
#     "output_dir": QCD_HT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_HT300to500_NoJEC_newFlav",
#     "input": "QCD_HT_NoJEC_relPtHatCut5_jtptmin4/QCD_HT300to500_NoJEC_newFlav/",
#     "xsec": 347700.0000,
#     "output_dir": QCD_HT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_HT500to700_NoJEC_newFlav",
#     "input": "QCD_HT_NoJEC_relPtHatCut5_jtptmin4/QCD_HT500to700_NoJEC_newFlav/",
#     "xsec": 32100.0000,
#     "output_dir": QCD_HT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_HT700to1000_NoJEC_newFlav",
#     "input": "QCD_HT_NoJEC_relPtHatCut5_jtptmin4/QCD_HT700to1000_NoJEC_newFlav/",
#     "xsec": 6831.0000,
#     "output_dir": QCD_HT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_HT1000to1500_NoJEC_newFlav",
#     "input": "QCD_HT_NoJEC_relPtHatCut5_jtptmin4/QCD_HT1000to1500_NoJEC_newFlav/",
#     "xsec": 1207.0000,
#     "output_dir": QCD_HT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
# {
#     "name": "QCD_HT2000toInf_NoJEC_newFlav",
#     "input": "QCD_HT_NoJEC_relPtHatCut5_jtptmin4/QCD_HT2000toInf_NoJEC_newFlav/",
#     "xsec": 25.2400,
#     "output_dir": QCD_HT_OUTPUT_DIR,
#     "era_dir": PYTHIA_ERA_DIR,
#     "nrefmax": QCD_NREFMAX,
# },
]

infos_ttbar_pythia = [
    # don't hadd beforehand, super slow
    {
        "name": "TT_Pythia_NoJEC_newFlav",
        "input": "TT_Pythia_NoJEC_relPtHatCut5_jtptmin4/TT_Pythia_NoJEC_newFlav/",
        "xsec": -1,
        "output_dir": "TT_Pythia_NoJEC_relPtHatCut5_jtptmin4_nbinsrelrsp_10k",
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": TT_NREFMAX,
        # "pf_PID": "2 3",  # 2 = e, 3 = mu, 4 = gamma
        # "pf_pt": 5,
        # "pf_dr": 0.4
    },
]

infos_dy_pythia = [
    {
        "name": "DYJetsToLL_HT-70to100_NoJEC_newFlav",
        "input": "%s/DYJetsToLL_HT-70to100_NoJEC_newFlav/" % DY_INPUT_DIR,
        "xsec": 215.6190,
        "output_dir": DY_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": DY_PF_PID,
        "pf_pt": DY_PF_PT,
        "pf_dr": PF_DR,
        "findZ": True,
    },
    {
        "name": "DYJetsToLL_HT-100to200_NoJEC_newFlav",
        "input": "%s/DYJetsToLL_HT-100to200_NoJEC_newFlav/" % DY_INPUT_DIR,
        "xsec": 181.3020,
        "output_dir": DY_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": DY_PF_PID,
        "pf_pt": DY_PF_PT,
        "pf_dr": PF_DR,
        "findZ": True,
    },
    {
        "name": "DYJetsToLL_HT-100to200_ext_NoJEC_newFlav",
        "input": "%s/DYJetsToLL_HT-100to200_ext_NoJEC_newFlav/" % DY_INPUT_DIR,
        "xsec": 181.3020,
        "output_dir": DY_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": DY_PF_PID,
        "pf_pt": DY_PF_PT,
        "pf_dr": PF_DR,
        "findZ": True,
    },
    {
        "name": "DYJetsToLL_HT-200to400_NoJEC_newFlav",
        "input": "%s/DYJetsToLL_HT-200to400_NoJEC_newFlav/" % DY_INPUT_DIR,
        "xsec": 50.4177,
        "output_dir": DY_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": DY_PF_PID,
        "pf_pt": DY_PF_PT,
        "pf_dr": PF_DR,
        "findZ": True,
    },
    {
        "name": "DYJetsToLL_HT-200to400_ext_NoJEC_newFlav",
        "input": "%s/DYJetsToLL_HT-200to400_ext_NoJEC_newFlav/" % DY_INPUT_DIR,
        "xsec": 50.4177,
        "output_dir": DY_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": DY_PF_PID,
        "pf_pt": DY_PF_PT,
        "pf_dr": PF_DR,
        "findZ": True,
    },
    {
        "name": "DYJetsToLL_HT-400to600_NoJEC_newFlav",
        "input": "%s/DYJetsToLL_HT-400to600_NoJEC_newFlav/" % DY_INPUT_DIR,
        "xsec": 6.9839,
        "output_dir": DY_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": DY_PF_PID,
        "pf_pt": DY_PF_PT,
        "pf_dr": PF_DR,
        "findZ": True,
    },
    {
        "name": "DYJetsToLL_HT-400to600_ext_NoJEC_newFlav",
        "input": "%s/DYJetsToLL_HT-400to600_ext_NoJEC_newFlav/" % DY_INPUT_DIR,
        "xsec": 6.9839,
        "output_dir": DY_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": DY_PF_PID,
        "pf_pt": DY_PF_PT,
        "pf_dr": PF_DR,
        "findZ": True,
    },
    {
        "name": "DYJetsToLL_HT-600to800_NoJEC_newFlav",
        "input": "%s/DYJetsToLL_HT-600to800_NoJEC_newFlav/" % DY_INPUT_DIR,
        "xsec": 1.6814,
        "output_dir": DY_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": DY_PF_PID,
        "pf_pt": DY_PF_PT,
        "pf_dr": PF_DR,
        "findZ": True,
    },
    {
        "name": "DYJetsToLL_HT-800to1200_NoJEC_newFlav",
        "input": "%s/DYJetsToLL_HT-800to1200_NoJEC_newFlav/" % DY_INPUT_DIR,
        "xsec": 0.7754,
        "output_dir": DY_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": DY_PF_PID,
        "pf_pt": DY_PF_PT,
        "pf_dr": PF_DR,
        "findZ": True,
    },
    {
        "name": "DYJetsToLL_HT-1200to2500_NoJEC_newFlav",
        "input": "%s/DYJetsToLL_HT-1200to2500_NoJEC_newFlav/" % DY_INPUT_DIR,
        "xsec": 0.1862,
        "output_dir": DY_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": DY_PF_PID,
        "pf_pt": DY_PF_PT,
        "pf_dr": PF_DR,
        "findZ": True,
    },
    {
        "name": "DYJetsToLL_HT-2500toInf_NoJEC_newFlav",
        "input": "%s/DYJetsToLL_HT-2500toInf_NoJEC_newFlav/" % DY_INPUT_DIR,
        "xsec": 0.0044,
        "output_dir": DY_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": DY_PF_PID,
        "pf_pt": DY_PF_PT,
        "pf_dr": PF_DR,
        "findZ": True,
    },

    {
        "name": "DYJetsToLL_MG_Herwig_NoJEC_newFlav",
        "input": "DYJets_MG_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/DYJetsToLL_MG_Herwig_NoJEC_newFlav",
        "xsec": -1.,
        "output_dir": "DYJets_MG_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k",
        "era_dir": HERWIG_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": DY_PF_PID,  # 2 = e, 3 = mu, 4 = gamma
        "pf_pt": DY_PF_PT,
        "pf_dr": PF_DR,
        "findZ": True,
    },
]

infos_gjets_pythia = [
    {
        "name": "GJets_HT-40To100_NoJEC_newFlav",
        "input": "%s/GJets_HT-40To100_NoJEC_newFlav" % GJETS_HT_INPUT_DIR,
        "xsec": 20660.0,
        "output_dir": GJETS_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": GJETS_PF_PID,  # 2 = e, 3 = mu, 4 = gamma
        "pf_pt": 5,
        "pf_dr": 0.4,
        "findGamma": True,
    },
    {
        "name": "GJets_HT-40To100_ext_NoJEC_newFlav",
        "input": "%s/GJets_HT-40To100_ext_NoJEC_newFlav" % GJETS_HT_INPUT_DIR,
        "xsec": 20660.0,
        "output_dir": GJETS_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": GJETS_PF_PID,  # 2 = e, 3 = mu, 4 = gamma
        "pf_pt": 5,
        "pf_dr": 0.4,
        "findGamma": True,
    },
    {
        "name": "GJets_HT-100To200_NoJEC_newFlav",
        "input": "%s/GJets_HT-100To200_NoJEC_newFlav" % GJETS_HT_INPUT_DIR,
        "xsec": 9249.0,
        "output_dir": GJETS_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": GJETS_PF_PID,  # 2 = e, 3 = mu, 4 = gamma
        "pf_pt": 5,
        "pf_dr": 0.4,
        "findGamma": True,
    },
    {
        "name": "GJets_HT-100To200_ext_NoJEC_newFlav",
        "input": "%s/GJets_HT-100To200_ext_NoJEC_newFlav" % GJETS_HT_INPUT_DIR,
        "xsec": 9249.0,
        "output_dir": GJETS_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": GJETS_PF_PID,  # 2 = e, 3 = mu, 4 = gamma
        "pf_pt": 5,
        "pf_dr": 0.4,
        "findGamma": True,
    },
    {
        "name": "GJets_HT-200To400_NoJEC_newFlav",
        "input": "%s/GJets_HT-200To400_NoJEC_newFlav" % GJETS_HT_INPUT_DIR,
        "xsec": 2321.0,
        "output_dir": GJETS_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": GJETS_PF_PID,  # 2 = e, 3 = mu, 4 = gamma
        "pf_pt": 5,
        "pf_dr": 0.4,
        "findGamma": True,
    },
    {
        "name": "GJets_HT-200To400_ext_NoJEC_newFlav",
        "input": "%s/GJets_HT-200To400_ext_NoJEC_newFlav" % GJETS_HT_INPUT_DIR,
        "xsec": 2321.0,
        "output_dir": GJETS_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": GJETS_PF_PID,  # 2 = e, 3 = mu, 4 = gamma
        "pf_pt": 5,
        "pf_dr": 0.4,
        "findGamma": True,
    },
    {
        "name": "GJets_HT-400To600_NoJEC_newFlav",
        "input": "%s/GJets_HT-400To600_NoJEC_newFlav" % GJETS_HT_INPUT_DIR,
        "xsec": 275.2,
        "output_dir": GJETS_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": GJETS_PF_PID,  # 2 = e, 3 = mu, 4 = gamma
        "pf_pt": 5,
        "pf_dr": 0.4,
        "findGamma": True,
    },
    {
        "name": "GJets_HT-400To600_ext_NoJEC_newFlav",
        "input": "%s/GJets_HT-400To600_ext_NoJEC_newFlav" % GJETS_HT_INPUT_DIR,
        "xsec": 275.2,
        "output_dir": GJETS_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": GJETS_PF_PID,  # 2 = e, 3 = mu, 4 = gamma
        "pf_pt": 5,
        "pf_dr": 0.4,
        "findGamma": True,
    },
    {
        "name": "GJets_HT-600ToInf_NoJEC_newFlav",
        "input": "%s/GJets_HT-600ToInf_NoJEC_newFlav" % GJETS_HT_INPUT_DIR,
        "xsec": 93.19,
        "output_dir": GJETS_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": GJETS_PF_PID,  # 2 = e, 3 = mu, 4 = gamma
        "pf_pt": 5,
        "pf_dr": 0.4,
        "findGamma": True,
    },
    {
        "name": "GJets_HT-600ToInf_ext_NoJEC_newFlav",
        "input": "%s/GJets_HT-600ToInf_ext_NoJEC_newFlav" % GJETS_HT_INPUT_DIR,
        "xsec": 93.19,
        "output_dir": GJETS_HT_OUTPUT_DIR,
        "era_dir": PYTHIA_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": GJETS_PF_PID,  # 2 = e, 3 = mu, 4 = gamma
        "pf_pt": 5,
        "pf_dr": 0.4,
        "findGamma": True,
    },
    {
        "name": "GJets_Herwig_NoJEC_newFlav",
        "input": "GJet_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/GJets_Herwig_NoJEC_newFlav/",
        "xsec": -1,
        "output_dir": "GJet_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k",
        "era_dir": HERWIG_ERA_DIR,
        "nrefmax": DY_NREFMAX,
        "alpha": alpha,
        "pf_PID": GJETS_PF_PID,
        "pf_pt": 5,
        "pf_dr": 0.4,
        "findGamma": True,
    },
]

# HERWIG SAMPLES
# ==============================================================================
infos_qcd_herwig = [
    {
        "name": "QCD_Pt_15to7000_Herwig_NoJEC_newFlav",
        "input": "%s/QCD_Pt_15to7000_Herwig_NoJEC_newFlav/" % QCD_HERWIG_INPUT_DIR,
        "xsec": -1,
        "output_dir": QCD_HERWIG_OUTPUT_DIR,
        "era_dir": HERWIG_ERA_DIR,
        "nrefmax": QCD_NREFMAX,
        # "pf_PID": "2 3 4",  # 2 = e, 3 = mu, 4 = gamma
        # "pf_pt": 5,
        # "pf_dr": 0.4
    },
]

infos_dy_herwig = [
    {
            "name": "DYJetsToLL_Herwig_NoJEC_newFlav",
            "input": "DYJets_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/DYJetsToLL_Herwig_NoJEC_newFlav",
            "xsec": -1.,
            "output_dir": "DYJets_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k_dummy",
            "era_dir": HERWIG_ERA_DIR,
            "nrefmax": DY_NREFMAX,
            "alpha": alpha,
            "pf_PID": DY_PF_PID,  # 2 = e, 3 = mu, 4 = gamma
            "pf_pt": DY_PF_PT,
            "pf_dr": PF_DR,
            "findZ": True,
    },
]

infos_gjets_herwig = [
    {
        "name": "GJets_Herwig_NoJEC_newFlav",
        "input": "GJet_Herwig_NoJEC_relPtHatCut5_jtptmin4/GJets_Herwig_NoJEC_newFlav/jaj_GJets_Herwig_NoJEC_newFlav_L1FastJet.root",
        "xsec": -1,
        "output_dir": "GJet_Herwig_NoJEC_relPtHatCut5_jtptmin4_nbinsrelrsp_10k",
        "era_dir": HERWIG_ERA_DIR,
        "nrefmax": DY_NREFMAX,
    },
]

infos_ttbar_herwig = [
    {
        "name": "TT_Herwig_NoJEC_newFlav",
        "input": "TT_Herwig_NoJEC_relPtHatCut5_jtptmin4/TT_Herwig_NoJEC_newFlav/jaj_TT_Herwig_NoJEC_newFlav_L1FastJet.root",
        "xsec": -1.,
        "output_dir": "TT_Herwig_NoJEC_relPtHatCut5_jtptmin4_nbinsrelrsp_10k",
        "era_dir": HERWIG_ERA_DIR,
        "nrefmax": TT_NREFMAX,
        # "pf_PID": "2 3",  # 2 = e, 3 = mu, 4 = gamma
        # "pf_pt": 5,
        # "pf_dr": 0.4
    },
]

# POWHEG+PYTHIA
# =============================================================================
# infos_qcd_powheg = [
    # {
    #     "name": "Dijet_Powheg_Pythia_NoJEC_newFlav",
    #     "input": "Dijet_Powheg_Pythia_NoJEC_relPtHatCut5_jtptmin4/Dijet_Powheg_Pythia_NoJEC_newFlav/jaj_Dijet_Powheg_Pythia_NoJEC_newFlav_ak4pfchs_L1FastJet.root",
    #     "xsec": -1.,
    #     "output_dir": "Dijet_Powheg_Pythia_NoJEC_relPtHatCut5_jtptmin4_nbinsrelrsp_10k",
    #     "era_dir": PYTHIA_ERA_DIR,
    #     "nrefmax": QCD_NREFMAX+1,
    # },
# ]


all_algos = [
    "ak4pfchs:0.2",
    # "ak4puppi:0.2",
    # "ak8pfchs:0.4",
    # "ak8puppi:0.4"
][:]

flav_dict = {
    "12": "ud",
    "3": "s",
    "4": "c",
    "5": "b",
    "21": "g",
    "0": "all",  # use default JEC
}

ef_max = 0.8
# ef_max = 99


def create_condor_template_dict():
    template = {
        "executable": "run_prog.sh",
        "transfer_executable": "True",
        "universe": "vanilla",
        "output": "$(name)_$(Cluster).$(Process).out",
        "error": "$(name)_$(Cluster).$(Process).err",
        "log": "$(name)_$(Cluster).$(Process).log",
        "RequestMemory": "2G",
        "requirements": 'OpSysAndVer == "SL6"',
        "getenv": "True",
        "environment": "\"LD_LIBRARY_PATH_STORED="+os.environ.get('LD_LIBRARY_PATH')+"\"",
        "notification": "Error",
        "notify_user": "robin.aggleton@desy.de",
    }
    return template


def dict_to_condor_contents(input_dict):
    contents = ['%s=%s' % (k, str(v)) for k, v in input_dict.items()]
    return "\n".join(contents)


def float_to_str(num):
    return ("%g" % num).replace(".", "p")


job = dict_to_condor_contents(create_condor_template_dict())
job += "\n"
job += "JobBatchName=JCA\n"
arguments = ("jet_correction_analyzer_x $(inputf) "
    "-outputDir $(outputdir) -suffix $(suffix) -algs $(algos) "
    "-era $(era) -path $(mypath) -levels 2 "  # JEC set info
    "-doflavor $(doflav) -pdgid $(pdgid) -flavorDefinition HADRONPARTON "  # flav def/selection info
    "-xsection $(xsec) -luminosity 35900 -useweight $(weight) "  # reweighting info
    "-nrefmax $(nrefmax) -ptgenmin 10 -ptrawmin 4 -relpthatmax 3.5 -relrspmax 2 "  # cuts
    "-alphamax $(alpha) -pfCandIds $(pfpid) -pfCandPtMin $(pfpt) -pfCandDr $(pfdr) -efmax $(efmax) "  # more cuts
    "-findZ $(findz) -findGamma $(findgamma) "  # identify bosons and veto against them
    "-drmin $(drmin) "  # matching param for genjet-genjet
    "-drmax $(drmax)"  # matching param for gen-reco
)
job += '\narguments = "%s"\n\n' % arguments
job += "\nqueue\n"

hadd_job = dict_to_condor_contents(create_condor_template_dict())
hadd_job += "\n"
hadd_job += "JobBatchName=HaddJCA\n"
hadd_job += '\narguments = "hadd -f $(finalfile) $(inputfiles)"\n\n'
hadd_job += "\nqueue\n"


era_append = "_standardMedianErr_meanWhenSmall_rspRangeLarge_fitMin15_useFitRange"

ef_str = float_to_str(ef_max)

# append = "_relRspMax2_relPtHatMax3p5_ptGenMin10_jtnefLt%s_jtcefLt%s_jtmufLt%s_centralEFcuts_unscaleEF_absEta" % (ef_str, ef_str, ef_str)
append = "_relRspMax2_relPtHatMax3p5_ptGenMin10_absEta_noDPhiCut"

job_args = []
job_names = []

hadd_job_names = []
hadd_job_args = []
hadd_job_depends = []

for sample_dict in chain(infos_qcd_pythia, infos_qcd_herwig):

    if (("herwig" in sample_dict['input'].lower() and "herwig" not in sample_dict['era_dir'].lower())
        or (("herwig" not in sample_dict['input'].lower() and "herwig" in sample_dict['era_dir'].lower()))):
        raise RuntimeError("Mixing Herwig/Pythia dataset/jec!")

    if not os.path.isdir(sample_dict['output_dir']):
        os.makedirs(sample_dict['output_dir'])

    # pf = {
    #     "pf_PID": "2 3 4",  # 2 = e, 3 = mu, 4 = gamma
    #     "pf_pt": 5,
    #     "pf_dr": 0.4
    # }
    # sample_dict.update(pf)

    for algo in all_algos:
        algo_name, dr_max = algo.split(":")

        these_job_names = []
        component_files = []

        dr_min = 4*float(dr_max)

        this_append = append
        if sample_dict.get('alpha', 0) > 0:
            this_append += '_alpha' + float_to_str(sample_dict['alpha'])
        this_append += "_nrefmax%d" % sample_dict.get("nrefmax", 0)
        this_append += "_drmin" + float_to_str(dr_min)
        this_append += "_ptGenOverlap10"

        if sample_dict.get("findZ", False):
            this_append += "_findZ"

        if sample_dict.get("findGamma", False):
            this_append += "_findGamma"

        if sample_dict.get('pf_PID', DUMMY_PF_ID) != DUMMY_PF_ID:
            parts = ""
            if "2" in sample_dict['pf_PID']:
                parts += "e"
            if "3" in sample_dict['pf_PID']:
                parts += "mu"
            if "4" in sample_dict['pf_PID']:
                parts += "g"
            this_append += "_%sCandOverlapGt0p5" % parts
        else:
            sample_dict['pf_PID'] = DUMMY_PF_ID

        if "pf_dr" in sample_dict:
            sample_dict['pf_dr'] = 2*float(dr_max)

        for flav, flav_name in flav_dict.iteritems():

            args_dict = {
                "name": "JCA_"+sample_dict['name']+"_"+algo_name+"_"+flav_name,
                "outputdir": sample_dict['output_dir'],
                "xsec": "%.8f" % sample_dict.get('xsec', -1),
                "algos": algo_name+"l1",
                "drmax": dr_max,
                "weight": "true",  # ignored if xsec > 0
                "pdgid": flav,
                "doflav": "true" if flav != "0" else "false",
                "era": "Summer16_07Aug2017_V10%s_%s" % (era_append, flav_name),
                "mypath": sample_dict['era_dir'],
                "suffix": "_".join([sample_dict['name'], this_append, flav_name]),
                "nrefmax": sample_dict.get('nrefmax', 0),
                "drmin": dr_min,
                "alpha": sample_dict.get('alpha', 0),
                "pfpid": sample_dict.get('pf_PID', DUMMY_PF_ID),
                "pfpt": sample_dict.get('pf_pt', 5),
                "pfdr": sample_dict.get('pf_dr', 0.4),
                "efmax": 99,
                # "jetID": "",
                "findZ": str(sample_dict.get('findZ', False)).lower(),
                "findGamma": str(sample_dict.get('findGamma', False)).lower(),
            }
            args_dict = OrderedDict(args_dict)

            if flav_name == "all":
                args_dict['mypath'] = ORIGINAL_ERA_DIR
                args_dict['era'] = os.path.basename(ORIGINAL_ERA_DIR.rstrip("/"))

            # Setup input files, tricky as different options used depending on if single file or directory
            if sample_dict['input'].endswith(".root"):
                # if one ROOT file, then leave inputfilepath blank and put full path for inputfilename
                args_dict['inputf'] = "-inputFilename " + sample_dict['input']
            else:
                # if multiple files, the program will add *.root to inputfilename if you specify inputfilepath
                args_dict["inputf"] = "-inputFilename jaj*%s" % algo_name  # program does *.root for us
                args_dict["inputf"] += " -inputFilePath " + sample_dict['input']

            job_args.append(" ".join(['%s="%s"' % (k, v) for k,v in args_dict.items()]))
            these_job_names.append(args_dict['name'])
            component_files.append(os.path.join(args_dict['outputdir'], "Closure_%s_%s.root" % (args_dict['algos'], args_dict['suffix'])))

        job_names.extend(these_job_names)
        final_output_file = os.path.join(sample_dict['output_dir'], "Closure_%s_%s.root" % (args_dict['algos'], "_".join([sample_dict['name'], this_append]),))
        hadd_name = "HADD_%s_%s" % (name, algo)
        hadd_job_args.append('name="%s" finalfile="%s" inputfiles="%s"' % (hadd_name, final_output_file, " ".join(component_files)))
        hadd_job_depends.append(' '.join(these_job_names))
        hadd_job_names.append(hadd_name)


if len(job_names) == 0:
    raise RuntimeError("Didn't find any files to run over!")

htc_filename = "htc_do_jet_correction_analyzer_x_job.condor"
with open(htc_filename, 'w') as f:
    f.write(job)

# Add hadd jobs
hadd_htc_filename = "hadd_%s" % htc_filename
with open(hadd_htc_filename, 'w') as f:
    f.write(hadd_job)

for ind, (hname, harg, hdeps) in enumerate(zip(hadd_job_names, hadd_job_args, hadd_job_depends)):
    dag += "JOB {0} {1}\n".format(hname, hadd_htc_filename)
    dag += "VARS {0} {1}\n".format(hname, harg)
    dag += "PARENT {0} CHILD {1}\n".format(hdeps, hname)

# dag += "RETRY ALL_NODES 3\n"  # dont want this as l2 purposely fails when doing checkFormulaEvaluator
status_file = htc_filename.replace(".condor", ".dagstatus")
dag += "NODE_STATUS_FILE %s\n" % (status_file)

dag_filename = htc_filename.replace(".condor", ".dag")
with open(dag_filename, 'w') as f:
    f.write(dag)

print "Submitting", len(job_names), "jobs"
cmd = "condor_submit_dag -maxjobs 200 -maxidle 1000 -f %s" % dag_filename
subprocess.check_call(cmd, shell=True)
print "Check status with:"
print "DAGstatus", status_file
