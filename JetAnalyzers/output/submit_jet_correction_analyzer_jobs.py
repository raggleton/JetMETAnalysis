#!/usr/bin/env python

import os
import subprocess
from glob import glob
from collections import OrderedDict
from uuid import uuid1
from itertools import chain

from countNevents import get_cache, count_events_in_file, save_cache


# ORIGINAL_ERA_DIR = "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JECDatabase/textFiles/Summer16_07Aug2017_V10_MC"

PYTHIA_ERA_DIR = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k"
HERWIG_ERA_DIR = "QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k"

# QCD_PT_INPUT_DIR = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF"
# QCD_PT_INPUT_DIR = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10"
QCD_PT_INPUT_DIR = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron"
DY_INPUT_DIR = "DYJets_HT_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10"
GJETS_HT_INPUT_DIR = "GJet_HT_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10"

# QCD_PT_OUTPUT_DIR = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k"
QCD_PT_OUTPUT_DIR = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_nbinsrelrsp_10k"
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


def construct_jec_name(jec_levels):
    name = ""
    if "1" in jec_levels:
        name += "L1FastJet"
    if "2" in jec_levels:
        name += "L2"
    if "3" in jec_levels:
        name += "L3"
    return name


JEC_LEVELS = "1 2 3"
JEC_LEVELS = "1"
JEC_NAME = construct_jec_name(JEC_LEVELS)


ERA_DIR = "/nfs/dust/cms/user/aggleton/JEC/CMSSW_10_2_6/src/JetMETAnalysis/JECDatabase/textFiles/"
ERA_16 = "Summer16_07Aug2017_V20_MC"
ERA_18 = "Autumn18_V3_MC"
infos_herwig7_nopu = {
    "name": "QCD_Pt_15to7000_Herwig7_NoPU_NoJEC_newFlav",
    "infos": [{
        "name": "QCD_Pt_15to7000_Herwig7_NoJEC_NoPU_miniaod",
        # "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCH2_Flat_13TeV_herwig7/crab_QCD_Pt-15to7000_herwig7_noPU_02_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/190202_132418/0000/",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCH2_Flat_13TeV_herwig7/crab_QCD_Pt-15to7000_herwig7_CH2_noPU_21_Mar_19_Autumn18_noJEC_constitInfo_miniaod_withPF/190321_100540/0000/",
        "xsec": -1.,
        "output_dir": "QCD_Pt_Herwig7_NoJEC_NoPU_relPtHatCut2p5_jtptmin4_PhysicsParton_nbinsrelrsp_10k_%s_%s" % (ERA_18, JEC_NAME),
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    ]
}
infos_herwigpp_nopu = {
    "name": "QCD_Pt_15to7000_Herwigpp_NoPU_NoJEC_newFlav",
    "infos": [{
            "name": "QCD_Pt_15to7000_Herwigpp_NoJEC_NoPU_miniaod",
            "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/crab_QCD_Pt-15to7000_herwig_HS1_noPU_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/0000/",
            "xsec": -1.,
            "output_dir": "QCD_Pt_Herwigpp_NoJEC_NoPU_relPtHatCut2p5_jtptmin4_PhysicsParton_nbinsrelrsp_10k_%s_%s" % (ERA_18, JEC_NAME),
            "era_dir": os.path.join(ERA_DIR, ERA_16),
            "era": ERA_16,
            "nrefmax": QCD_NREFMAX,
    },]
}

infos_herwig7 = {
    "name": "QCD_Pt_15to7000_Herwig7_NoJEC_newFlav",
    "infos": [
        {
                "name": "QCD_Pt_15to7000_Herwig7_NoJEC_miniaod",
                "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCH2_Flat_13TeV_herwig7/crab_QCD_Pt-15to7000_herwig7_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/190205_061202/0000/",
                # "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCH2_Flat_13TeV_herwig7/crab_QCD_Pt-15to7000_herwig7_CH2_21_Mar_19_Autumn18_noJEC_constitInfo_miniaod_withPF/190321_100532/0000/",
                "xsec": -1.,
                "output_dir": "QCD_Pt_Herwig7_NoJEC_relPtHatCut2p5_jtptmin4_HadronParton_nbinsrelrsp_10k_%s_%s" % (ERA_18, JEC_NAME),
                "era_dir": os.path.join(ERA_DIR, ERA_18),
                "era": ERA_18,
                "nrefmax": QCD_NREFMAX,
        },
    ]
}

infos_herwigpp = {
    "name": "QCD_Pt_15to7000_Herwigpp_NoJEC_newFlav",
    "infos": [
        {
                "name": "QCD_Pt_15to7000_Herwigpp_ext_NoJEC_miniaod",
                "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/crab_QCD_Pt-15to7000_ext1_herwig_HS1_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/0000/",
                "xsec": -1.,
                "output_dir": "QCD_Pt_Herwigpp_NoJEC_relPtHatCut2p5_jtptmin4_PhysicsParton_nbinsrelrsp_10k_%s_%s" % (ERA_16, JEC_NAME),
                "era_dir": os.path.join(ERA_DIR, ERA_16),
                "era": ERA_16,
                "nrefmax": QCD_NREFMAX,
        },
    ]
}


QCD_PT_16_OUTPUT_DIR = "QCD_Pt_16_NoJEC_relPtHatCut2p5_jtptmin4_PhysicsParton_nbinsrelrsp_10k_%s_%s" % (ERA_16, JEC_NAME)
QCD_PT_18_OUTPUT_DIR = "QCD_Pt_18_NoJEC_relPtHatCut2p5_jtptmin4_PhysicsParton_nbinsrelrsp_10k_%s_%s" % (ERA_18, JEC_NAME)
QCD_PT_18_OUTPUT_DIR = "QCD_Pt_18_NoJEC_relPtHatCut2p5_jtptmin4_HadronParton_nbinsrelrsp_10k_%s_%s" % (ERA_18, JEC_NAME)
QCD_PT_NOPU_18_OUTPUT_DIR = "QCD_Pt_18_NoPU_NoJEC_relPtHatCut2p5_jtptmin4_PhysicsParton_nbinsrelrsp_10k_%s_%s" % (ERA_18, JEC_NAME)
infos_qcdpy8_16 = {
    "name": "QCD_Pt_15toInf_Py8_P8M1_NoJEC_newFlav",
    "infos": [
        {
            "name": "QCD_Pt_15to30_NoJEC_newFlav",
            "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_15to30_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/",
            "xsec": 1837410000,
            "output_dir": QCD_PT_16_OUTPUT_DIR,
            "era_dir": os.path.join(ERA_DIR, ERA_16),
            "era": ERA_16,
            "nrefmax": QCD_NREFMAX,
        },
        {
            "name": "QCD_Pt_30to50_NoJEC_newFlav",
            "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_30to50_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/",
            "xsec": 140932000,
            "output_dir": QCD_PT_16_OUTPUT_DIR,
            "era_dir": os.path.join(ERA_DIR, ERA_16),
            "era": ERA_16,
            "nrefmax": QCD_NREFMAX,
        },
        {
            "name": "QCD_Pt_50to80_NoJEC_newFlav",
            "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_50to80_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/",
            "xsec": 19204300,
            "output_dir": QCD_PT_16_OUTPUT_DIR,
            "era_dir": os.path.join(ERA_DIR, ERA_16),
            "era": ERA_16,
            "nrefmax": QCD_NREFMAX,
        },
        {
            "name": "QCD_Pt_80to120_NoJEC_newFlav",
            "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_80to120_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/",
            "xsec": 2762530,
            "output_dir": QCD_PT_16_OUTPUT_DIR,
            "era_dir": os.path.join(ERA_DIR, ERA_16),
            "era": ERA_16,
            "nrefmax": QCD_NREFMAX,
        },
        {
            "name": "QCD_Pt_120to170_NoJEC_newFlav",
            "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_120to170_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/",
            "xsec": 471100,
            "output_dir": QCD_PT_16_OUTPUT_DIR,
            "era_dir": os.path.join(ERA_DIR, ERA_16),
            "era": ERA_16,
            "nrefmax": QCD_NREFMAX,
        },
        {
            "name": "QCD_Pt_170to300_NoJEC_newFlav",
            "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_170to300_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/",
            "xsec": 117276,
            "output_dir": QCD_PT_16_OUTPUT_DIR,
            "era_dir": os.path.join(ERA_DIR, ERA_16),
            "era": ERA_16,
            "nrefmax": QCD_NREFMAX,
        },
        {
            "name": "QCD_Pt_300to470_NoJEC_newFlav",
            "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_300to470_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/",
            "xsec": 7823,
            "output_dir": QCD_PT_16_OUTPUT_DIR,
            "era_dir": os.path.join(ERA_DIR, ERA_16),
            "era": ERA_16,
            "nrefmax": QCD_NREFMAX,
        },
        {
            "name": "QCD_Pt_470to600_NoJEC_newFlav",
            "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_470to600_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/",
            "xsec": 648.2,
            "output_dir": QCD_PT_16_OUTPUT_DIR,
            "era_dir": os.path.join(ERA_DIR, ERA_16),
            "era": ERA_16,
            "nrefmax": QCD_NREFMAX,
        },
        {
            "name": "QCD_Pt_600to800_NoJEC_newFlav",
            "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_600to800_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/",
            "xsec": 186.9,
            "output_dir": QCD_PT_16_OUTPUT_DIR,
            "era_dir": os.path.join(ERA_DIR, ERA_16),
            "era": ERA_16,
            "nrefmax": QCD_NREFMAX,
        },
        {
            "name": "QCD_Pt_800to1000_NoJEC_newFlav",
            "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_800to1000_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/",
            "xsec": 32.293,
            "output_dir": QCD_PT_16_OUTPUT_DIR,
            "era_dir": os.path.join(ERA_DIR, ERA_16),
            "era": ERA_16,
            "nrefmax": QCD_NREFMAX,
        },
        {
            "name": "QCD_Pt_1000to1400_NoJEC_newFlav",
            "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1000to1400_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/",
            "xsec": 9.4183,
            "output_dir": QCD_PT_16_OUTPUT_DIR,
            "era_dir": os.path.join(ERA_DIR, ERA_16),
            "era": ERA_16,
            "nrefmax": QCD_NREFMAX,
        },
        {
            "name": "QCD_Pt_1400to1800_NoJEC_newFlav",
            "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1400to1800_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/",
            "xsec": 0.84265,
            "output_dir": QCD_PT_16_OUTPUT_DIR,
            "era_dir": os.path.join(ERA_DIR, ERA_16),
            "era": ERA_16,
            "nrefmax": QCD_NREFMAX,
        },
        {
            "name": "QCD_Pt_1800to2400_NoJEC_newFlav",
            "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1800to2400_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/",
            "xsec": 0.114943,
            "output_dir": QCD_PT_16_OUTPUT_DIR,
            "era_dir": os.path.join(ERA_DIR, ERA_16),
            "era": ERA_16,
            "nrefmax": QCD_NREFMAX,
        },
        {
            "name": "QCD_Pt_2400to3200_NoJEC_newFlav",
            "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_2400to3200_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/",
            "xsec": 0.0068298,
            "output_dir": QCD_PT_16_OUTPUT_DIR,
            "era_dir": os.path.join(ERA_DIR, ERA_16),
            "era": ERA_16,
            "nrefmax": QCD_NREFMAX,
        },
        {
            "name": "QCD_Pt_3200toInf_NoJEC_newFlav",
            "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_3200toInf_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/",
            "xsec": 0.0001654,
            "output_dir": QCD_PT_16_OUTPUT_DIR,
            "era_dir": os.path.join(ERA_DIR, ERA_16),
            "era": ERA_16,
            "nrefmax": QCD_NREFMAX,
        },
    ]
}

infos_qcdpy8_18 = {
    "name": "QCD_Pt_15toInf_Py8_CP5_NoJEC_newFlav",
    "infos": [
    {
        "name": "QCD_Pt_15to30_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_15to30_TuneCP5_13TeV_pythia8/crab_QCD_Pt_15to30_ext1_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
        "xsec": 1246000000.0,
        "output_dir": QCD_PT_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_30to50_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_30to50_TuneCP5_13TeV_pythia8/crab_QCD_Pt_30to50_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
        "xsec": 106900000.0,
        "output_dir": QCD_PT_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_50to80_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_50to80_TuneCP5_13TeV_pythia8/crab_QCD_Pt_50to80_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
        "xsec": 15710000.0,
        "output_dir": QCD_PT_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_80to120_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_80to120_TuneCP5_13TeV_pythia8/crab_QCD_Pt_80to120_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
        "xsec": 2336000.0,
        "output_dir": QCD_PT_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_120to170_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_120to170_TuneCP5_13TeV_pythia8/crab_QCD_Pt_120to170_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
        "xsec": 407300.0,
        "output_dir": QCD_PT_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_170to300_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/crab_QCD_Pt_170to300_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
        "xsec": 103500.0,
        "output_dir": QCD_PT_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_300to470_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/crab_QCD_Pt_300to470_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
        "xsec": 6830.0,
        "output_dir": QCD_PT_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_470to600_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/crab_QCD_Pt_470to600_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
        "xsec": 552.1,
        "output_dir": QCD_PT_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_600to800_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/crab_QCD_Pt_600to800_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
        "xsec": 156.5,
        "output_dir": QCD_PT_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_800to1000_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/crab_QCD_Pt_800to1000_ext1_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
        "xsec": 26.28,
        "output_dir": QCD_PT_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_1000to1400_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1000to1400_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
        "xsec": 7.47,
        "output_dir": QCD_PT_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_1400to1800_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1400to1800_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
        "xsec": 0.6484,
        "output_dir": QCD_PT_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_1800to2400_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1800to2400_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
        "xsec": 0.08743,
        "output_dir": QCD_PT_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_2400to3200_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/crab_QCD_Pt_2400to3200_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
        "xsec": 0.005236,
        "output_dir": QCD_PT_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_3200toInf_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/crab_QCD_Pt_3200toInf_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
        "xsec": 0.0001357,
        "output_dir": QCD_PT_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },

    ]
}

infos_qcdpy8_18_nopu = {
    "name": "QCD_Pt_15toInf_Py8_CP5_NoPU_NoJEC_newFlav",
    "infos": [
    # {
    #     "name": "QCD_Pt_15to30_NoJEC_newFlav",
    #     "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_15to30_TuneCP5_13TeV_pythia8/crab_QCD_Pt_15to30_ext1_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
    #     "xsec": 1246000000.0,
    #     "output_dir": QCD_PT_NOPU_18_OUTPUT_DIR,
    #     "era_dir": os.path.join(ERA_DIR, ERA_18),
    #     "era": ERA_18,
    #     "nrefmax": QCD_NREFMAX,
    # },
    # {
    #     "name": "QCD_Pt_30to50_NoJEC_newFlav",
    #     "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_30to50_TuneCP5_13TeV_pythia8/crab_QCD_Pt_30to50_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
    #     "xsec": 106900000.0,
    #     "output_dir": QCD_PT_NOPU_18_OUTPUT_DIR,
    #     "era_dir": os.path.join(ERA_DIR, ERA_18),
    #     "era": ERA_18,
    #     "nrefmax": QCD_NREFMAX,
    # },
    # {
    #     "name": "QCD_Pt_50to80_NoJEC_newFlav",
    #     "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_50to80_TuneCP5_13TeV_pythia8/crab_QCD_Pt_50to80_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
    #     "xsec": 15710000.0,
    #     "output_dir": QCD_PT_NOPU_18_OUTPUT_DIR,
    #     "era_dir": os.path.join(ERA_DIR, ERA_18),
    #     "era": ERA_18,
    #     "nrefmax": QCD_NREFMAX,
    # },
    # {
    #     "name": "QCD_Pt_80to120_NoJEC_newFlav",
    #     "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_80to120_TuneCP5_13TeV_pythia8/crab_QCD_Pt_80to120_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
    #     "xsec": 2336000.0,
    #     "output_dir": QCD_PT_NOPU_18_OUTPUT_DIR,
    #     "era_dir": os.path.join(ERA_DIR, ERA_18),
    #     "era": ERA_18,
    #     "nrefmax": QCD_NREFMAX,
    # },
    # {
    #     "name": "QCD_Pt_120to170_NoJEC_newFlav",
    #     "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_120to170_TuneCP5_13TeV_pythia8/crab_QCD_Pt_120to170_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
    #     "xsec": 407300.0,
    #     "output_dir": QCD_PT_NOPU_18_OUTPUT_DIR,
    #     "era_dir": os.path.join(ERA_DIR, ERA_18),
    #     "era": ERA_18,
    #     "nrefmax": QCD_NREFMAX,
    # },
    # {
    #     "name": "QCD_Pt_170to300_NoJEC_newFlav",
    #     "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/crab_QCD_Pt_170to300_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
    #     "xsec": 103500.0,
    #     "output_dir": QCD_PT_NOPU_18_OUTPUT_DIR,
    #     "era_dir": os.path.join(ERA_DIR, ERA_18),
    #     "era": ERA_18,
    #     "nrefmax": QCD_NREFMAX,
    # },
    # {
    #     "name": "QCD_Pt_300to470_NoJEC_newFlav",
    #     "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/crab_QCD_Pt_300to470_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/",
    #     "xsec": 6830.0,
    #     "output_dir": QCD_PT_NOPU_18_OUTPUT_DIR,
    #     "era_dir": os.path.join(ERA_DIR, ERA_18),
    #     "era": ERA_18,
    #     "nrefmax": QCD_NREFMAX,
    # },
    {
        "name": "QCD_Pt_470to600_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/crab_QCD_Pt_470to600_ext1_pythia_CP5_noPU_15_Apr_19_Autumn18_noJEC_constitInfo_miniaod_withPF/*/*/",
        "xsec": 552.1,
        "output_dir": QCD_PT_NOPU_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_600to800_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/crab_QCD_Pt_600to800_pythia_CP5_noPU_15_Apr_19_Autumn18_noJEC_constitInfo_miniaod_withPF/*/*/",
        "xsec": 156.5,
        "output_dir": QCD_PT_NOPU_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_800to1000_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/crab_QCD_Pt_800to1000_ext1_pythia_CP5_noPU_15_Apr_19_Autumn18_noJEC_constitInfo_miniaod_withPF/*/*/",
        "xsec": 26.28,
        "output_dir": QCD_PT_NOPU_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_1000to1400_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1000to1400_pythia_CP5_noPU_15_Apr_19_Autumn18_noJEC_constitInfo_miniaod_withPF/*/*/",
        "xsec": 7.47,
        "output_dir": QCD_PT_NOPU_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_1400to1800_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1400to1800_*pythia_CP5_noPU_15_Apr_19_Autumn18_noJEC_constitInfo_miniaod_withPF/*/*/",
        "xsec": 0.6484,
        "output_dir": QCD_PT_NOPU_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_1800to2400_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1800to2400*pythia_CP5_noPU_15_Apr_19_Autumn18_noJEC_constitInfo_miniaod_withPF/*/*/",
        "xsec": 0.08743,
        "output_dir": QCD_PT_NOPU_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_2400to3200_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/crab_QCD_Pt_2400to3200*pythia_CP5_noPU_15_Apr_19_Autumn18_noJEC_constitInfo_miniaod_withPF/*/*/",
        "xsec": 0.005236,
        "output_dir": QCD_PT_NOPU_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },
    {
        "name": "QCD_Pt_3200toInf_NoJEC_newFlav",
        "input": "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/crab_QCD_Pt_3200toInf*pythia_CP5_noPU_15_Apr_19_Autumn18_noJEC_constitInfo_miniaod_withPF/*/*/",
        "xsec": 0.0001357,
        "output_dir": QCD_PT_NOPU_18_OUTPUT_DIR,
        "era_dir": os.path.join(ERA_DIR, ERA_18),
        "era": ERA_18,
        "nrefmax": QCD_NREFMAX,
    },

    ]
}

all_algos = [
    "ak4pfchs:0.2",
    # "ak4pf:0.2",
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
ptgen_min = 750
ptgen_max = 10000
ptgen_min = 0
arguments = ("jet_correction_analyzer_x $(inputf) "
    "-outputDir $(odir) -suffix $(suffix) -algs $(algos) "
    "-era $(era) -path $(mypath) $(levels) " # -levels 2"  # JEC set info
    "-doflavor $(doflav) -pdgid $(pdgid) -flavorDefinition HADRONPARTON "  # flav def/selection info
    "-xsection $(xsec) -luminosity 35900 -useweight $(weight) "  # reweighting info
    # "-nrefmax $(nrefmax) -ptgenmin {ptgen_min} -ptgenmax {ptgen_max} -ptrawmin 4 -relpthatmax 2.5 -relrspmax 2 "  # cuts
    "-nrefmax $(nrefmax) -ptgenmin {ptgen_min} -ptrawmin 4 -relpthatmax 2 -relrspmax 2 "  # cuts
    "-alphamax $(alpha) -pfCandIds $(pfpid) -pfCandPtMin $(pfpt) -pfCandDr $(pfdr) -efmax $(efmax) "  # more cuts
    "-findZ $(findz) -findGamma $(findgamma) "  # identify bosons and veto against them
    "-drmin $(drmin) "  # matching param for genjet-genjet
    "-drmax $(drmax) "  # matching param for gen-reco
    "-reduceHistograms true "
).format(ptgen_min=ptgen_min, ptgen_max=ptgen_max)

job += '\narguments = "%s"\n\n' % arguments
job += "\nqueue\n"


hadd_job = dict_to_condor_contents(create_condor_template_dict())
hadd_job += "\n"
hadd_job += "JobBatchName=HaddJCA\n"
hadd_job += '\narguments = "hadd -f $(finalfile) $(inputfiles)"\n\n'
hadd_job += "\nqueue\n"


era_append = ""

append = "_relRspMax2_relPtHatMax2_ptGenMin%d_ptGenMax%d" % (ptgen_min, ptgen_max)


job_args = []
job_names = []

hadd_job_names = []
hadd_job_args = []
hadd_job_depends = []

CACHE_FILENAME = "cache_nevents.csv"
NEVENTS_CACHE = get_cache(CACHE_FILENAME)

for algo in all_algos:
    algo_name, dr_max = algo.split(":")

    for flav, flav_name in flav_dict.iteritems():

        # for info_dict in [infos_herwig7, infos_herwigpp, infos_qcdpy8_18, infos_qcdpy8_16]:
        # for info_dict in [infos_herwig7, infos_herwig7_nopu]:
        # for info_dict in [infos_herwig7_nopu]:
        # for info_dict in [infos_qcdpy8_18_nopu]:
        # for info_dict in [infos_qcdpy8_18, infos_qcdpy8_16]:
        # for info_dict in [infos_qcdpy8_18, infos_herwig7]:
        for info_dict in [infos_qcdpy8_18]:
        # for info_dict in [infos_herwig7]:
        # for info_dict in [infos_herwig7, infos_herwigpp]:
        # for info_dict in [infos_qcdpy8_16]:
        # for info_dict in [infos_herwig7_nopu, infos_herwigpp_nopu]:

            # Do it in this nested order, so that we can hadd all the samples from
            # a given list of info dicts for a specific flavour and jet algo
            these_job_names = []
            component_files = []

            for sample_dict in info_dict['infos']:

                if not os.path.isdir(sample_dict['output_dir']):
                    os.makedirs(sample_dict['output_dir'])

                # if (("herwig" in sample_dict['input'].lower() and "herwig" not in sample_dict['era_dir'].lower())
                #     or (("herwig" not in sample_dict['input'].lower() and "herwig" in sample_dict['era_dir'].lower()))):
                #     raise RuntimeError("Mixing Herwig/Pythia dataset/jec!")


                # pf = {
                #     "pf_PID": "2 3 4",  # 2 = e, 3 = mu, 4 = gamma
                #     "pf_pt": 5,
                #     "pf_dr": 0.4
                # }
                # sample_dict.update(pf)

                n_inputs = len(glob(sample_dict['input']))
                if (n_inputs == 0):
                    raise RuntimeError("0 inputs for %d in %s" % (sample_dict['name'], info_dict['name']))

                print sample_dict['name'], "queuing %d jobs" % (n_inputs)

                # Need to split up by input directory as TChain doesn't do "proper" globbing
                # so you have to run over each directory as a separate job
                for ind, this_input in enumerate(glob(sample_dict['input'])):

                    this_append = append
                    if sample_dict.get('alpha', 0) > 0:
                        this_append += '_alpha' + float_to_str(sample_dict['alpha'])
                    this_append += "_nrefmax%d" % sample_dict.get("nrefmax", 0)

                    dr_min = 4*float(dr_max)
                    dr_min = -1
                    if dr_min > 0:
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


                    args_dict = {
                        "name": "_".join(["JCA", info_dict['name'], sample_dict['name'], algo_name, flav_name, JEC_NAME, str(ind)]),
                        "odir": sample_dict['output_dir'],
                        "xsec": "%.8f" % sample_dict.get('xsec', -1),
                        # "algos": algo_name+"l1",
                        "algos": algo_name,
                        "drmax": dr_max,
                        "weight": "false" if sample_dict.get('xsec', -1) > 0 else "true",  # ignored if xsec > 0
                        "pdgid": flav,
                        "doflav": "true" if flav != "0" else "false",
                        "era": sample_dict['era'],
                        # "levels": "" if "nopu" in sample_dict['name'].lower() else "-levels %s" % JEC_LEVELS,
                        "levels": "-levels %s" % JEC_LEVELS,
                        "mypath": sample_dict['era_dir'],
                        "suffix": "_".join([sample_dict['name'], this_append, flav_name, str(ind)]),
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

                    if this_input.endswith(".root"):
                        # if one ROOT file, then leave inputfilepath blank and put full path for inputfilename
                        args_dict['inputf'] = "-inputFilename " + this_input
                    else:
                        # if multiple files, the program will add *.root to inputfilename if you specify inputfilepath
                        # args_dict["inputf"] = "-inputFilename jaj*%s" % algo_name  # program does *.root for us
                        args_dict["inputf"] = "-inputFilename JRA*"  # program does *.root for us
                        args_dict["inputf"] += ' -inputFilePath ' + this_input

                    job_args.append(" ".join(['%s="%s"' % (k, v) for k,v in args_dict.items()]))
                    these_job_names.append(args_dict['name'])
                    component_files.append(os.path.join(args_dict['odir'], "Closure_%s%s.root" % (args_dict['algos'], args_dict['suffix'])))

            job_names.extend(these_job_names)
            if len(component_files) > 1:
                final_output_file = os.path.join(sample_dict['output_dir'], "Closure_%s_%s_%s.root" % (args_dict['algos'], "_".join([info_dict['name'], this_append]), flav_name))
                if os.path.isfile(final_output_file):
                    os.remove(final_output_file)
                hadd_name = "HADD_%s_%s_%s" % (info_dict['name'], algo_name, flav_name)
                hadd_job_args.append('name="%s" finalfile="%s" inputfiles="%s"' % (hadd_name, final_output_file, " ".join(component_files)))
                hadd_job_depends.append(' '.join(these_job_names))
                hadd_job_names.append(hadd_name)


if len(job_names) == 0:
    raise RuntimeError("Didn't find any files to run over!")

htc_filename = "htc_do_jet_correction_analyzer_x_job_%s.condor" % (uuid1())
with open(htc_filename, 'w') as f:
    f.write(job)

dag = ""
for ind, (job_name, job_args_entry) in enumerate(zip(job_names, job_args)):
    dag += "JOB {0} {1}\n".format(job_name, htc_filename)
    dag += "VARS {0} {1}\n".format(job_name, job_args_entry)

# Add hadd jobs
hadd_htc_filename = "HADD_%s" % htc_filename
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

