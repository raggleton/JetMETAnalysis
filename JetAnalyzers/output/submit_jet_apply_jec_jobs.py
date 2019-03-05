#!/usr/bin/env python

import os
import subprocess
from itertools import izip_longest
from glob import glob
from uuid import uuid1


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
        "+MyProject": "af-cms",
    }
    return template


def dict_to_condor_contents(input_dict):
    contents = ['%s=%s' % (k, str(v)) for k, v in input_dict.items()]
    return "\n".join(contents)


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def construct_jec_name(jec_levels):
    name = ""
    if "1" in jec_levels:
        name += "L1FastJet"
    if "2" in jec_levels:
        name += "L2"
    if "3" in jec_levels:
        name += "L3"
    return name


infos = [
# name, outputdir, inputdir/path (with wildcards)

# ("QCD_Pt_15to30_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_15to30_pythia_02_Mar_18_newGenJetFlav_noJEC/*/*/"),
# ("QCD_Pt_30to50_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_30to50_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/"),
# ("QCD_Pt_50to80_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_50to80_pythia_02_Mar_18_newGenJetFlav_noJEC/*/*/"),
# ("QCD_Pt_80to120_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_80to120_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/"),
# ("QCD_Pt_120to170_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_120to170_pythia_02_Mar_18_newGenJetFlav_noJEC/*/*/"),
# ("QCD_Pt_170to300_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_170to300_pythia_02_Mar_18_newGenJetFlav_noJEC/*/*/"),
# ("QCD_Pt_300to470_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_300to470_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/"),
# ("QCD_Pt_470to600_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_470to600_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/"),
# ("QCD_Pt_600to800_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_600to800_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/"),
# ("QCD_Pt_800to1000_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_800to1000_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/"),
# ("QCD_Pt_1000to1400_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1000to1400_pythia_02_Mar_18_newGenJetFlav_noJEC/*/*/"),
# ("QCD_Pt_1400to1800_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1400to1800_pythia_02_Mar_18_newGenJetFlav_noJEC/*/*/"),
# ("QCD_Pt_1800to2400_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1800to2400_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/"),
# ("QCD_Pt_2400to3200_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_2400to3200_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/"),
# ("QCD_Pt_3200toInf_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_3200toInf_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/"),

# ("QCD_Pt_15to30_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_15to30_pythia_16_Apr_18_newFlav_noJEC_storePFCand/*/*/"),
# ("QCD_Pt_30to50_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_30to50_pythia_16_Apr_18_newFlav_noJEC_storePFCand/*/*/"),
# ("QCD_Pt_50to80_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_50to80_pythia_16_Apr_18_newFlav_noJEC_storePFCand/*/*/"),
# ("QCD_Pt_80to120_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_80to120_pythia_16_Apr_18_newFlav_noJEC_storePFCand/*/*/"),
# ("QCD_Pt_120to170_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_120to170_pythia_16_Apr_18_newFlav_noJEC_storePFCand2/*/*/"),
# ("QCD_Pt_170to300_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_170to300_pythia_16_Apr_18_newFlav_noJEC_storePFCand/*/*/"),
# ("QCD_Pt_300to470_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_300to470_pythia_16_Apr_18_newFlav_noJEC_storePFCand/*/*/"),
# ("QCD_Pt_470to600_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_470to600_pythia_16_Apr_18_newFlav_noJEC_storePFCand2/*/*/"),
# ("QCD_Pt_600to800_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_600to800_pythia_16_Apr_18_newFlav_noJEC_storePFCand/*/*/"),
# ("QCD_Pt_800to1000_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_800to1000_pythia_16_Apr_18_newFlav_noJEC_storePFCand/*/*/"),
# ("QCD_Pt_1000to1400_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1000to1400_pythia_16_Apr_18_newFlav_noJEC_storePFCand/*/*/"),
# ("QCD_Pt_1400to1800_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1400to1800_pythia_16_Apr_18_newFlav_noJEC_storePFCand/*/*/"),
# ("QCD_Pt_1800to2400_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1800to2400_pythia_16_Apr_18_newFlav_noJEC_storePFCand/*/*/"),
# ("QCD_Pt_2400to3200_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_2400to3200_pythia_16_Apr_18_newFlav_noJEC_storePFCand/*/*/"),
# ("QCD_Pt_3200toInf_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_3200toInf_pythia_16_Apr_18_newFlav_noJEC_storePFCand/*/*/"),

# ("QCD_Pt_15to30_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_15to30_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),
# ("QCD_Pt_30to50_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_30to50_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),
# ("QCD_Pt_50to80_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_50to80_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),
# ("QCD_Pt_80to120_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_80to120_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),
# ("QCD_Pt_120to170_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_120to170_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),
# ("QCD_Pt_170to300_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_170to300_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),
# ("QCD_Pt_300to470_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_300to470_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),
# ("QCD_Pt_470to600_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_470to600_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),
# ("QCD_Pt_600to800_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_600to800_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),
# ("QCD_Pt_800to1000_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_800to1000_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav_3/*/*/"),
# ("QCD_Pt_1000to1400_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1000to1400_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),
# ("QCD_Pt_1400to1800_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1400to1800_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),
# ("QCD_Pt_1800to2400_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1800to2400_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),
# ("QCD_Pt_2400to3200_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_2400to3200_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),
# ("QCD_Pt_3200toInf_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_3200toInf_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),

# apply L2 ontop of L1
# ("QCD_Pt_15to30_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL1/QCD_Pt_15to30_NoJEC_newFlav/"),
# ("QCD_Pt_30to50_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL1/QCD_Pt_30to50_NoJEC_newFlav/"),
# ("QCD_Pt_50to80_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL1/QCD_Pt_50to80_NoJEC_newFlav/"),
# ("QCD_Pt_80to120_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL1/QCD_Pt_80to120_NoJEC_newFlav/"),
# ("QCD_Pt_120to170_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL1/QCD_Pt_120to170_NoJEC_newFlav/"),
# ("QCD_Pt_170to300_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL1/QCD_Pt_170to300_NoJEC_newFlav/"),
# ("QCD_Pt_300to470_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL1/QCD_Pt_300to470_NoJEC_newFlav/"),
# ("QCD_Pt_470to600_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL1/QCD_Pt_470to600_NoJEC_newFlav/"),
# ("QCD_Pt_600to800_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL1/QCD_Pt_600to800_NoJEC_newFlav/"),
# ("QCD_Pt_800to1000_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL1/QCD_Pt_800to1000_NoJEC_newFlav/"),
# ("QCD_Pt_1000to1400_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL1/QCD_Pt_1000to1400_NoJEC_newFlav/"),
# ("QCD_Pt_1400to1800_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL1/QCD_Pt_1400to1800_NoJEC_newFlav/"),
# ("QCD_Pt_1800to2400_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL1/QCD_Pt_1800to2400_NoJEC_newFlav/"),
# ("QCD_Pt_2400to3200_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL1/QCD_Pt_2400to3200_NoJEC_newFlav/"),
# ("QCD_Pt_3200toInf_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL1/QCD_Pt_3200toInf_NoJEC_newFlav/"),


# ("QCD_HT50to100_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT50to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT50to100_mg-pythia_25_May_18_newFlav_noJEC_storePFCand2/*/*/"),
# ("QCD_HT100to200_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT100to200_mg-pythia_25_May_18_newFlav_noJEC_storePFCand2/*/*/"),
# ("QCD_HT200to300_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT200to300*_mg-pythia_25_May_18_newFlav_noJEC_storePFCand2/*/*/"),  # not on disk
# ("QCD_HT300to500_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT300to500*_mg-pythia_25_May_18_newFlav_noJEC_storePFCand2/*/*/"),
# ("QCD_HT500to700_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT500to700*_mg-pythia_25_May_18_newFlav_noJEC_storePFCand2/*/*/"),
# ("QCD_HT700to1000_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT700to1000_mg-pythia_25_May_18_newFlav_noJEC_storePFCand2/*/*/"),
# ("QCD_HT1000to1500_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT1000to1500*_mg-pythia_25_May_18_newFlav_noJEC_storePFCand2/*/*/"),
# ("QCD_HT1500to2000_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT1500to2000_mg-pythia_25_May_18_newFlav_noJEC_storePFCand2/*/*/"), # not on disk
# ("QCD_HT2000toInf_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT2000toInf*_mg-pythia_25_May_18_newFlav_noJEC_storePFCand2/*/*/"),

# ("DYJetsToLL_HT-70to100_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/DYJetsToLL_M-50_HT-70to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_HT-70to100_mg-pythia_16_Apr_18_newFlav_noJEC_storePFCand/*/*/"),
# ("DYJetsToLL_HT-100to200_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_HT-100to200_mg-pythia_16_Apr_18_newFlav_noJEC_storePFCand2/*/*/"),
# ("DYJetsToLL_HT-100to200_ext_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_HT-100to200_ext1_mg-pythia_16_Apr_18_newFlav_noJEC_storePFCand2/*/*/"),
# ("DYJetsToLL_HT-200to400_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_HT-200to400_mg-pythia_16_Apr_18_newFlav_noJEC_storePFCand2/*/*/"),
# ("DYJetsToLL_HT-200to400_ext_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/DYJetsToLL_M-50_HT-200to400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_HT-200to400_ext1_mg-pythia_16_Apr_18_newFlav_noJEC_storePFCand2/*/*/"),
# ("DYJetsToLL_HT-400to600_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_HT-400to600_mg-pythia_16_Apr_18_newFlav_noJEC_storePFCand2/*/*/"),
# ("DYJetsToLL_HT-400to600_ext_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/DYJetsToLL_M-50_HT-400to600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_HT-400to600_ext1_mg-pythia_16_Apr_18_newFlav_noJEC_storePFCand2/*/*/"),
# ("DYJetsToLL_HT-600to800_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/DYJetsToLL_M-50_HT-600to800_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_HT-600to800_mg-pythia_16_Apr_18_newFlav_noJEC_storePFCand2/*/*/"),
# ("DYJetsToLL_HT-800to1200_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/DYJetsToLL_M-50_HT-800to1200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_HT-800to1200_mg-pythia_16_Apr_18_newFlav_noJEC_storePFCand2/*/*/"),
# ("DYJetsToLL_HT-1200to2500_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/DYJetsToLL_M-50_HT-1200to2500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_HT-1200to2500_mg-pythia_16_Apr_18_newFlav_noJEC_storePFCand/*/*/"),
# ("DYJetsToLL_HT-2500toInf_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/DYJetsToLL_M-50_HT-2500toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_HT-2500toInf_mg-pythia_16_Apr_18_newFlav_noJEC_storePFCand2/*/*/"),

# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/crab_QCD_Pt-15to7000_herwig_16_Apr_18_newFlav_noJEC_storePFCand/180416_133226/0000/"),

# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav_small", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/crab_QCD_Pt-15to7000_herwig_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),

# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav_ext", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/crab_QCD_Pt-15to7000_ext1_herwig_22_Sep_18_noJEC_storePhysicsAlgoHadronFlav_v2/*/*/"),

# ("QCD_Pt_15to7000_Herwig7_NoJEC_NoPU_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCH2_Flat_13TeV_herwig7/crab_QCD_Pt-15to7000_herwig7_noPU_02_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/190202_132418/0000/"),
# ("QCD_Pt_15to7000_Herwigpp_NoJEC_NoPU_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/crab_QCD_Pt-15to7000_herwig_noPU_02_Feb_19_noJEC_storeAllFlav_genEF_miniaod/190202_134342/0000/"),

# ("QCD_Pt_15to7000_Herwigpp_miniaod_ext", "QCD_Pt_15to7000_Herwigpp_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/crab_QCD_Pt-15to7000_ext1_herwig_HS1_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/"),

# ("QCD_Pt_15to30_Pythia8_CUETP8M1_miniaod", "QCD_Pt_Pythia8_CUETP8M1_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_15to30_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/"),
# ("QCD_Pt_30to50_Pythia8_CUETP8M1_miniaod", "QCD_Pt_Pythia8_CUETP8M1_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_30to50_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/"),
# ("QCD_Pt_50to80_Pythia8_CUETP8M1_miniaod", "QCD_Pt_Pythia8_CUETP8M1_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_50to80_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/"),
# ("QCD_Pt_80to120_Pythia8_CUETP8M1_miniaod", "QCD_Pt_Pythia8_CUETP8M1_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_80to120_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/"),
# ("QCD_Pt_120to170_Pythia8_CUETP8M1_miniaod", "QCD_Pt_Pythia8_CUETP8M1_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_120to170_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/"),
# ("QCD_Pt_170to300_Pythia8_CUETP8M1_miniaod", "QCD_Pt_Pythia8_CUETP8M1_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_170to300_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/"),
# ("QCD_Pt_300to470_Pythia8_CUETP8M1_miniaod", "QCD_Pt_Pythia8_CUETP8M1_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_300to470_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/"),
# ("QCD_Pt_470to600_Pythia8_CUETP8M1_miniaod", "QCD_Pt_Pythia8_CUETP8M1_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_470to600_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/"),
# ("QCD_Pt_600to800_Pythia8_CUETP8M1_miniaod", "QCD_Pt_Pythia8_CUETP8M1_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_600to800_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/"),
# ("QCD_Pt_800to1000_Pythia8_CUETP8M1_miniaod", "QCD_Pt_Pythia8_CUETP8M1_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_800to1000_pythia_3_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/"),
# ("QCD_Pt_1000to1400_Pythia8_CUETP8M1_miniaod", "QCD_Pt_Pythia8_CUETP8M1_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1000to1400_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/"),
# ("QCD_Pt_1400to1800_Pythia8_CUETP8M1_miniaod", "QCD_Pt_Pythia8_CUETP8M1_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1400to1800_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/"),
# ("QCD_Pt_1800to2400_Pythia8_CUETP8M1_miniaod", "QCD_Pt_Pythia8_CUETP8M1_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1800to2400_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/"),
# ("QCD_Pt_2400to3200_Pythia8_CUETP8M1_miniaod", "QCD_Pt_Pythia8_CUETP8M1_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_2400to3200_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/"),
# ("QCD_Pt_3200toInf_Pythia8_CUETP8M1_miniaod", "QCD_Pt_Pythia8_CUETP8M1_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_3200toInf_pythia_05_Feb_19_Summer16_noJEC_storeAllFlav_genEF_miniaod_v2/*/*/"),

("QCD_Pt_15to7000_Herwig7_miniaod", "QCD_Pt_15to7000_Herwig7_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCH2_Flat_13TeV_herwig7/crab_QCD_Pt-15to7000_herwig7_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/"),

("QCD_Pt_15to30_Pythia8_CP5_miniaod", "QCD_Pt_Pythia8_CP5_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_15to30_TuneCP5_13TeV_pythia8/crab_QCD_Pt_15to30_ext1_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod//*/*/"),
("QCD_Pt_30to50_Pythia8_CP5_miniaod", "QCD_Pt_Pythia8_CP5_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_30to50_TuneCP5_13TeV_pythia8/crab_QCD_Pt_30to50_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/"),
("QCD_Pt_50to80_Pythia8_CP5_miniaod", "QCD_Pt_Pythia8_CP5_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_50to80_TuneCP5_13TeV_pythia8/crab_QCD_Pt_50to80_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/"),
("QCD_Pt_80to120_Pythia8_CP5_miniaod", "QCD_Pt_Pythia8_CP5_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_80to120_TuneCP5_13TeV_pythia8/crab_QCD_Pt_80to120_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/"),
("QCD_Pt_120to170_Pythia8_CP5_miniaod", "QCD_Pt_Pythia8_CP5_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_120to170_TuneCP5_13TeV_pythia8/crab_QCD_Pt_120to170_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/"),
("QCD_Pt_170to300_Pythia8_CP5_miniaod", "QCD_Pt_Pythia8_CP5_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/crab_QCD_Pt_170to300_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/"),
("QCD_Pt_300to470_Pythia8_CP5_miniaod", "QCD_Pt_Pythia8_CP5_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/crab_QCD_Pt_300to470_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/"),
("QCD_Pt_470to600_Pythia8_CP5_miniaod", "QCD_Pt_Pythia8_CP5_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/crab_QCD_Pt_470to600_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/"),
("QCD_Pt_600to800_Pythia8_CP5_miniaod", "QCD_Pt_Pythia8_CP5_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/crab_QCD_Pt_600to800_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/"),
("QCD_Pt_800to1000_Pythia8_CP5_miniaod", "QCD_Pt_Pythia8_CP5_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/crab_QCD_Pt_800to1000_ext1_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/"),
("QCD_Pt_1000to1400_Pythia8_CP5_miniaod", "QCD_Pt_Pythia8_CP5_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1000to1400_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/"),
("QCD_Pt_1400to1800_Pythia8_CP5_miniaod", "QCD_Pt_Pythia8_CP5_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1400to1800_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/"),
("QCD_Pt_1800to2400_Pythia8_CP5_miniaod", "QCD_Pt_Pythia8_CP5_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1800to2400_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/"),
("QCD_Pt_2400to3200_Pythia8_CP5_miniaod", "QCD_Pt_Pythia8_CP5_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/crab_QCD_Pt_2400to3200_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/"),
("QCD_Pt_3200toInf_Pythia8_CP5_miniaod", "QCD_Pt_Pythia8_CP5_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/crab_QCD_Pt_3200toInf_pythia_CP5_05_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/*/*/"),


]


all_algos = [
    "ak4pfchs",
    # "ak4pfchsl1",
    # "ak4puppi",
    # "ak8pfchs",
    # "ak8puppi"
][:]

flav = "All"

# output_dir = "QCD_Pt_NoJEC_jtptmin4_withPF_PhysicsAlgoHadron"
# output_dir = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10"
# output_dir = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2"+flav
# output_dir = "QCD_HT_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10"
# output_dir = "QCD_Pt_Herwig_NoJEC_jtptmin4_PhysicsAlgoHadron"
# output_dir = "QCD_Pt_15to7000_Herwig7_NoJEC_NoPU_miniaod_Autumn18_V1_MC"

# output_dir = "QCD_Pt_15to7000_Herwigpp_NoPU_miniaod"

# output_dir = "DYJets_HT_NoJEC_relPtHatCut5_jtptmin4"
# output_dir = "DYJets_HT_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10"
# output_dir = "GJet_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF"
# output_dir = "GJet_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10"
# output_dir = "TT_Herwig_NoJEC_relPtHatCut5_jtptmin4"
# output_dir = "TT_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF"
# output_dir = "TT_Pythia_NoJEC_relPtHatCut5_jtptmin4"
# output_dir = "TT_Pythia_NoJEC_relPtHatCut5_jtptmin4_withPF"
# output_dir = "Dijet_Powheg_Pythia_NoJEC_relPtHatCut5_jtptmin4"
# output_dir = "GJet_HT_NoJEC_relPtHatCut5_jtptmin4_withPF"
# output_dir = "GJet_HT_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10"
# output_dir = "DYJets_MG_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10"
# output_dir = "DYJets_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10"

useAlgLevel = "true"
if flav == "All":
    # jec_era = "Autumn18_V1_MC"  # Autumn18
    jec_era = "Autumn18_V3_MC"  # Autumn18
    # jec_era = "Summer16_07Aug2017_V20_MC"  # summer16
    jec_path = "/nfs/dust/cms/user/aggleton/JEC/CMSSW_10_2_6/src/JetMETAnalysis/JECDatabase/textFiles/"+jec_era
    useAlgLevel = "false"
else:
    jec_path = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k"
    jec_era = "Summer16_07Aug2017_V10_standardMedianErr_meanWhenSmall_rspRangeLarge_fitMin15_useFitRange_"+flav

jec_levels = "1"
jec_name = construct_jec_name(jec_levels)

# keep this small as cannot handle long lists of files (9993 char limit?)
Nfiles = 25

job = dict_to_condor_contents(create_condor_template_dict())
job += "\n\n"
job += "JobBatchName=JAJ\n"
job += "jecpath=%s\n" % jec_path
job += "era=%s\n" % jec_era
arguments = ("jet_apply_jec_x -input $(inputf) -output $(outputf) -algs $(algos) "
    "-levels " + jec_levels + " -era $(era) -jecpath $(jecpath) "
    "-L1FastJet true -saveitree false -useAlgLevel " + useAlgLevel
)
job += "\narguments = %s\n\n" % arguments
job += "\nqueue\n"
# print job

job_args = []
job_names = []

for name, output_dir, input_dir in infos:
    if flav == "All":
        output_dir += "_"+jec_name+"_"+jec_era

    # Put all files from given sample in own directory to make future steps easier
    this_output_dir = os.path.join(output_dir, name)
    if not os.path.isdir(this_output_dir):
        os.makedirs(this_output_dir)

    # Split files to avoid running out of disk space on workers
    pattern = os.path.join(input_dir, "JRA*.root")  # straight ntuples
    # pattern = os.path.join(input_dir, "jaj*.root")  # if already had JAJ applied once

    for ind, group in enumerate(grouper(glob(pattern), Nfiles, "")):

        for algo in all_algos:
            args_dict = {
                "name": "JAJ_"+name+"_"+jec_name+"_"+algo.split(":")[0]+"_"+str(ind),
                "inputf": " ".join(group).strip(),
                "outputf": os.path.join(this_output_dir, "jaj_%s_%s_%s_%d.root" % (name, algo.split(":")[0], jec_name, ind)),
                "algos": algo,
            }
            # job += "\n".join(["%s=%s" % (k, v) for k,v in args_dict.items()])
            # job += "\nqueue\n\n"
            job_args.append(" ".join(['%s="%s"' % (k, v) for k,v in args_dict.items()]))
            job_names.append(args_dict['name'])

print job

if len(job_names) == 0:
    raise RuntimeError("Didn't find any files to run over!")

job_filename = "htc_do_jet_apply_jec_x_job_%s_%s.condor" % (flav, uuid1())
with open(job_filename, 'w') as f:
    f.write(job)


dag = ""
for ind, (job_name, job_args_entry) in enumerate(zip(job_names, job_args)):
    dag += "JOB {0} {1}\n".format(job_name, job_filename)
    dag += "VARS {0} {1}\n".format(job_name, job_args_entry)

dag += "RETRY ALL_NODES 3\n"
status_file = job_filename.replace(".condor", ".dagstatus")
dag += "NODE_STATUS_FILE %s\n" % (status_file)

dag_filename = job_filename.replace(".condor", ".dag")
with open(dag_filename, 'w') as f:
    f.write(dag)

print "Submitting", len(job_names), "jobs"
cmd = "condor_submit_dag -maxjobs 200 -maxidle 1000 -f %s" % dag_filename
subprocess.check_call(cmd, shell=True)
print "Check status with"
print "DAGstatus", status_file
