#!/usr/bin/env python

import os
import subprocess
from itertools import izip_longest
from glob import glob

def create_condor_template_dict():
    template = {
        "executable": "run_prog.sh",
        "transfer_executable": "True",
        "universe": "vanilla",
        "output": "$(name)_$(Cluster)_$(Process).out",
        "error": "$(name)_$(Cluster)_$(Process).err",
        "log": "$(name)_$(Cluster)_$(Process).log",
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


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


infos = [

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
("QCD_Pt_800to1000_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_800to1000_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav_3/*/*/"),
# ("QCD_Pt_1000to1400_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1000to1400_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),
# ("QCD_Pt_1400to1800_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1400to1800_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),
# ("QCD_Pt_1800to2400_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1800to2400_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),
# ("QCD_Pt_2400to3200_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_2400to3200_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),
# ("QCD_Pt_3200toInf_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_3200toInf_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),


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

# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/crab_QCD_Pt-15to7000_herwig_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/"),

# ("GJets_Herwig_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/GJet_Pt-15To6000_TuneCUETHS1-Flat_13TeV_herwigpp/crab_GJet_Pt-15To6000_TuneCUETHS1-Flat_13TeV_herwigpp_herwig_16_Apr_18_newFlav_noJEC_storePFCand/180416_133255/0000/"),

# ("TT_Herwig_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/TT_TuneEE5C_13TeV-powheg-herwigpp/crab_TT_TuneEE5C_13TeV-powheg-herwigpp_ext_powheg-herwig_16_Apr_18_newFlav_noJEC_storePFCand/180416_133156/0000/"),

# ("TT_Pythia_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_16_Apr_18_newFlav_noJEC_storePFCand2/*/0000/"),

# ("Dijet_Powheg_Pythia_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/Dijet_NNPDF30_powheg_pythia8_TuneCUETP8M1_13TeV_bornktmin150/crab_Dijet_NNPDF30_powheg_pythia_04_Apr_18_newGenJetFlav_noJEC_fixAK8matching/180404_151523/0000/"),

# ('GJets_HT-40To100_NoJEC_newFlav', '/pnfs/desy.de/cms/tier2/store/user/raggleto/GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT-40To100_mg-pythia_28_Apr_18_newFlav_noJEC_storePFCand2/180428_143606/0000'),
# ('GJets_HT-40To100_ext_NoJEC_newFlav', '/pnfs/desy.de/cms/tier2/store/user/raggleto/GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT-40To100_ext1_mg-pythia_28_Apr_18_newFlav_noJEC_storePFCand2/180428_143623/0000'),
# ('GJets_HT-100To200_NoJEC_newFlav', '/pnfs/desy.de/cms/tier2/store/user/raggleto/GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT-100To200_mg-pythia_28_Apr_18_newFlav_noJEC_storePFCand2/180428_143253/0000'),
# ('GJets_HT-100To200_ext_NoJEC_newFlav', '/pnfs/desy.de/cms/tier2/store/user/raggleto/GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT-100To200_ext1_mg-pythia_28_Apr_18_newFlav_noJEC_storePFCand2/180428_143330/0000'),
# ('GJets_HT-200To400_NoJEC_newFlav', '/pnfs/desy.de/cms/tier2/store/user/raggleto/GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT-200To400_mg-pythia_28_Apr_18_newFlav_noJEC_storePFCand2/180428_143408/0000'),
# ('GJets_HT-200To400_ext_NoJEC_newFlav', '/pnfs/desy.de/cms/tier2/store/user/raggleto/GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT-200To400_ext1_mg-pythia_28_Apr_18_newFlav_noJEC_storePFCand2/180428_143441/0000'),
# ('GJets_HT-400To600_NoJEC_newFlav', '/pnfs/desy.de/cms/tier2/store/user/raggleto/GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT-400To600_mg-pythia_28_Apr_18_newFlav_noJEC_storePFCand2/180428_143515/0000'),
# ('GJets_HT-400To600_ext_NoJEC_newFlav', '/pnfs/desy.de/cms/tier2/store/user/raggleto/GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT-400To600_ext1_mg-pythia_28_Apr_18_newFlav_noJEC_storePFCand2/180428_143532/0000'),
# ('GJets_HT-600ToInf_NoJEC_newFlav', '/pnfs/desy.de/cms/tier2/store/user/raggleto/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT-600ToInf_mg-pythia_28_Apr_18_newFlav_noJEC_storePFCand2/180428_143640/0000'),
# ('GJets_HT-600ToInf_ext_NoJEC_newFlav', '/pnfs/desy.de/cms/tier2/store/user/raggleto/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_GJets_HT-600ToInf_ext1_mg-pythia_28_Apr_18_newFlav_noJEC_storePFCand2/180428_143714/0000'),

# ('DYJetsToLL_MG_Herwig_NoJEC_newFlav', '/pnfs/desy.de/cms/tier2/store/user/raggleto/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-herwigpp_30M/crab_DYJetsToLL_M-50_mg-herwig-proper_28_Apr_18_newFlav_noJEC_storePFCand2/180428_143731/*')

# ('DYJetsToLL_Herwig_NoJEC_newFlav', '/pnfs/desy.de/cms/tier2/store/user/raggleto/DYJetsToLL_M-50_TuneCUETHS1_13TeV-madgraphMLM-herwigpp/crab_DYJetsToLL_M-50_herwig_25_May_18_newFlav_noJEC_storePFCand2/180525_085501/*')
]


all_algos = [
    "ak4pfchs",
    # "ak4puppi",
    # "ak8pfchs",
    # "ak8puppi"
][:]

# output_dir = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF"
# output_dir = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10"
output_dir = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron"
# output_dir = "QCD_HT_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10"
# output_dir = "QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron"
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

jec_path = "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JECDatabase/textFiles/Summer16_07Aug2017_V10_MC"

jec_era = "Summer16_07Aug2017_V10_MC"

jec_levels = "1"

# keep this small as cannot handle long lists of files (9993 char limit?)
Nfiles = 25

job = dict_to_condor_contents(create_condor_template_dict())
job += "\n"
job += "JobBatchName=JAJ\n"
job += "jecpath=%s\n" % jec_path
job += "era=%s\n" % jec_era
arguments = "jet_apply_jec_x -input $(inputf) -output $(outputf) -algs $(algos) -levels 1 -era $(era) -jecpath $(jecpath) -L1FastJet true -saveitree false"
job += "\narguments = %s\n\n" % arguments
# print job

for name, input_dir in infos:
    # Put all files from given sample in own directory to make future steps easier
    this_output_dir = os.path.join(output_dir, name)
    if not os.path.isdir(this_output_dir):
        os.makedirs(this_output_dir)

    # Split files to avoid running out of disk space on workers
    pattern = os.path.join(input_dir, "JRA*.root")

    for ind, group in enumerate(grouper(glob(pattern), Nfiles, "")):

        for algo in all_algos:
            args_dict = {
                "name": "JAJ_"+name+"_"+algo.split(":")[0]+"_"+str(ind), 
                "inputf": " ".join(group).strip(),
                "outputf": os.path.join(this_output_dir, "jaj_%s_%s_L1FastJet_%d.root" % (name, algo.split(":")[0], ind)),
                "algos": algo,
            }
            job += "\n".join(["%s=%s" % (k, v) for k,v in args_dict.items()])
            job += "\nqueue\n\n"

print job

job_filename = "do_jet_apply_jec_x_job.condor"
with open(job_filename, 'w') as f:
    f.write(job)

cmd = "condor_submit %s" % job_filename
subprocess.check_call(cmd, shell=True)
