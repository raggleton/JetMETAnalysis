#!/usr/bin/env python

import os
import subprocess
from itertools import izip_longest
from glob import glob
from uuid import uuid1

from countNevents import get_cache, count_events_in_file, save_cache


def create_condor_template_dict():
    template = {
        "executable": "run_prog.sh",
        "transfer_executable": "True",
        "universe": "vanilla",
        "output": "$(Name)_$(Cluster).$(Process).out",
        "error": "$(Name)_$(Cluster).$(Process).err",
        "log": "$(Name)_$(Cluster).$(Process).log",
        "RequestMemory": "2G",
        "requirements": 'OpSysAndVer == "SL6"',
        "getenv": "True",
        "environment": '"LD_LIBRARY_PATH_STORED='+os.environ.get('LD_LIBRARY_PATH')+'"',
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


# flav = "s"
infos = [
# ("QCD_HT50to100", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT50to100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT50to100_mg-pythia_20_Nov_17_newGenJetFlav/171120_142448/0000/"),
# ("QCD_HT100to200", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT100to200_mg-pythia_20_Nov_17_newGenJetFlav/171120_142425/*/", 27990000.0000),
# ("QCD_HT200to300", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT200to300_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT200to300_mg-pythia_20_Nov_17_newGenJetFlav/171120_142510/0000/", 1712000.0000),
# ("QCD_HT300to500", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT300to500_mg-pythia_20_Nov_17_newGenJetFlav/171120_142447/*/", 347700.0000),
# ("QCD_HT500to700", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT500to700_mg-pythia_20_Nov_17_newGenJetFlav/171120_142510/0000/", 32100.0000),
# ("QCD_HT700to1000", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT700to1000_mg-pythia_20_Nov_17_newGenJetFlav/171120_142510/*/", 6831.0000),
# ("QCD_HT1000to1500", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT1000to1500_mg-pythia_20_Nov_17_newGenJetFlav/171120_142447/0000/", 1207.0000),
# ("QCD_HT1500to2000", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT1000to1500_mg-pythia_20_Nov_17_newGenJetFlav/171120_142447/0000/", 1207.0000),
# ("QCD_HT2000toInf", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT2000toInf_mg-pythia_20_Nov_17_newGenJetFlav/171120_142447/0000/", 25.2400),
# ("QCD_FLAT_NoJEC", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/crab_QCD_Pt-15to7000_pythia_21_Nov_17_newGenJetFlav_v2/171120_235503/0000/", 1),
# ("QCD_FLAT_HERWIG_NoJEC", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/crab_QCD_Pt-15to7000_herwig_28_Nov_17_newGenJetFlav_noJEC/*/0000/", 1),

# ("QCD_Pt_15to30_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_15to30_pythia_02_Mar_18_newGenJetFlav_noJEC/*/*/", 1837410000),
# ("QCD_Pt_30to50_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_30to50_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/", 140932000),
# ("QCD_Pt_50to80_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_50to80_pythia_02_Mar_18_newGenJetFlav_noJEC/*/*/", 19204300),
# ("QCD_Pt_80to120_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_80to120_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/", 2762530),
# ("QCD_Pt_120to170_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_120to170_pythia_02_Mar_18_newGenJetFlav_noJEC/*/*/", 471100),
# ("QCD_Pt_170to300_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_170to300_pythia_02_Mar_18_newGenJetFlav_noJEC/*/*/", 117276),
# ("QCD_Pt_300to470_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_300to470_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/", 7823),
# ("QCD_Pt_470to600_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_470to600_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/", 648.2),
# ("QCD_Pt_600to800_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_600to800_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/", 186.9),
# ("QCD_Pt_800to1000_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_800to1000_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/", 32.293),
# ("QCD_Pt_1000to1400_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1000to1400_pythia_02_Mar_18_newGenJetFlav_noJEC/*/*/", 9.4183),
# ("QCD_Pt_1400to1800_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1400to1800_pythia_02_Mar_18_newGenJetFlav_noJEC/*/*/", 0.84265),
# ("QCD_Pt_1800to2400_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1800to2400_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/", 0.114943),
# ("QCD_Pt_2400to3200_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_2400to3200_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/", 0.0068298),
# ("QCD_Pt_3200toInf_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_3200toInf_pythia_28_Feb_18_newGenJetFlav_noJEC/*/*/", 0.0001654),

# ("QCD_Pt_15to30_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_15to30_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/", 1837410000),
# ("QCD_Pt_30to50_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_30to50_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/", 140932000),
# ("QCD_Pt_50to80_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_50to80_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/", 19204300),
# ("QCD_Pt_80to120_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_80to120_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/", 2762530),
# ("QCD_Pt_120to170_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_120to170_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/", 471100),
# ("QCD_Pt_170to300_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_170to300_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/", 117276),
# ("QCD_Pt_300to470_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_300to470_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/", 7823),
# ("QCD_Pt_470to600_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_470to600_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/", 648.2),
# ("QCD_Pt_600to800_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_600to800_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/", 186.9),
# ("QCD_Pt_800to1000_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_800to1000_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav_3/*/*/", 32.293),
# ("QCD_Pt_1000to1400_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1000to1400_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/", 9.4183),
# ("QCD_Pt_1400to1800_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1400to1800_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/", 0.84265),
# ("QCD_Pt_1800to2400_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_1800to2400_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/", 0.114943),
# ("QCD_Pt_2400to3200_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_2400to3200_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/", 0.0068298),
# ("QCD_Pt_3200toInf_NoJEC_newFlav", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/crab_QCD_Pt_3200toInf_pythia_18_Jun_18_noJEC_storePFCand2_storePhysicsAlgoHadronFlav/*/*/", 0.0001654),


# for after doing jet_apply_jec_x
# 2016 samples with L1 JEC
# ("QCD_Pt_15to30_NoJEC_newFlav", "QCD_Pt_NoJEC_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC/QCD_Pt_15to30_NoJEC_newFlav/", 1837410000),
# ("QCD_Pt_30to50_NoJEC_newFlav", "QCD_Pt_NoJEC_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC/QCD_Pt_30to50_NoJEC_newFlav/", 140932000),
# ("QCD_Pt_50to80_NoJEC_newFlav", "QCD_Pt_NoJEC_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC/QCD_Pt_50to80_NoJEC_newFlav/", 19204300),
# ("QCD_Pt_80to120_NoJEC_newFlav", "QCD_Pt_NoJEC_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC/QCD_Pt_80to120_NoJEC_newFlav/", 2762530),
# ("QCD_Pt_120to170_NoJEC_newFlav", "QCD_Pt_NoJEC_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC/QCD_Pt_120to170_NoJEC_newFlav/", 471100),
# ("QCD_Pt_170to300_NoJEC_newFlav", "QCD_Pt_NoJEC_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC/QCD_Pt_170to300_NoJEC_newFlav/", 117276),
# ("QCD_Pt_300to470_NoJEC_newFlav", "QCD_Pt_NoJEC_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC/QCD_Pt_300to470_NoJEC_newFlav/", 7823),
# ("QCD_Pt_470to600_NoJEC_newFlav", "QCD_Pt_NoJEC_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC/QCD_Pt_470to600_NoJEC_newFlav/", 648.2),
# ("QCD_Pt_600to800_NoJEC_newFlav", "QCD_Pt_NoJEC_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC/QCD_Pt_600to800_NoJEC_newFlav/", 186.9),
# ("QCD_Pt_800to1000_NoJEC_newFlav", "QCD_Pt_NoJEC_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC/QCD_Pt_800to1000_NoJEC_newFlav/", 32.293),
# ("QCD_Pt_1000to1400_NoJEC_newFlav", "QCD_Pt_NoJEC_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC/QCD_Pt_1000to1400_NoJEC_newFlav/", 9.4183),
# ("QCD_Pt_1400to1800_NoJEC_newFlav", "QCD_Pt_NoJEC_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC/QCD_Pt_1400to1800_NoJEC_newFlav/", 0.84265),
# ("QCD_Pt_1800to2400_NoJEC_newFlav", "QCD_Pt_NoJEC_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC/QCD_Pt_1800to2400_NoJEC_newFlav/", 0.114943),
# ("QCD_Pt_2400to3200_NoJEC_newFlav", "QCD_Pt_NoJEC_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC/QCD_Pt_2400to3200_NoJEC_newFlav/", 0.0068298),
# ("QCD_Pt_3200toInf_NoJEC_newFlav", "QCD_Pt_NoJEC_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC/QCD_Pt_3200toInf_NoJEC_newFlav/", 0.0001654),

# 2018, only L1 JEC
# ("QCD_Pt_15to30_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJet_Autumn18_V3_MC/QCD_Pt_15to30_Pythia8_CP5_miniaod/", 1246000000),
# ("QCD_Pt_30to50_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJet_Autumn18_V3_MC/QCD_Pt_30to50_Pythia8_CP5_miniaod/", 106900000),
# ("QCD_Pt_50to80_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJet_Autumn18_V3_MC/QCD_Pt_50to80_Pythia8_CP5_miniaod/", 15710000),
# ("QCD_Pt_80to120_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJet_Autumn18_V3_MC/QCD_Pt_80to120_Pythia8_CP5_miniaod/", 2336000),
# ("QCD_Pt_120to170_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJet_Autumn18_V3_MC/QCD_Pt_120to170_Pythia8_CP5_miniaod/", 407300),
# ("QCD_Pt_170to300_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJet_Autumn18_V3_MC/QCD_Pt_170to300_Pythia8_CP5_miniaod/", 103500),
# ("QCD_Pt_300to470_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJet_Autumn18_V3_MC/QCD_Pt_300to470_Pythia8_CP5_miniaod/", 6830),
# ("QCD_Pt_470to600_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJet_Autumn18_V3_MC/QCD_Pt_470to600_Pythia8_CP5_miniaod/", 552.1),
# ("QCD_Pt_600to800_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJet_Autumn18_V3_MC/QCD_Pt_600to800_Pythia8_CP5_miniaod/", 156.5),
# ("QCD_Pt_800to1000_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJet_Autumn18_V3_MC/QCD_Pt_800to1000_Pythia8_CP5_miniaod/", 26.28),
# ("QCD_Pt_1000to1400_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJet_Autumn18_V3_MC/QCD_Pt_1000to1400_Pythia8_CP5_miniaod/", 7.47),
# ("QCD_Pt_1400to1800_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJet_Autumn18_V3_MC/QCD_Pt_1400to1800_Pythia8_CP5_miniaod/", 0.648),
# ("QCD_Pt_1800to2400_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJet_Autumn18_V3_MC/QCD_Pt_1800to2400_Pythia8_CP5_miniaod/", 0.08743),
# ("QCD_Pt_2400to3200_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJet_Autumn18_V3_MC/QCD_Pt_2400to3200_Pythia8_CP5_miniaod/", 0.005236),
# ("QCD_Pt_3200toInf_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJet_Autumn18_V3_MC/QCD_Pt_3200toInf_Pythia8_CP5_miniaod/", 0.0001357),

# 2018, L1+L2+L3 JEC
# ("QCD_Pt_15to30_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJetL2L3_Autumn18_V3_MC/QCD_Pt_15to30_Pythia8_CP5_miniaod/", 1246000000),
# ("QCD_Pt_30to50_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJetL2L3_Autumn18_V3_MC/QCD_Pt_30to50_Pythia8_CP5_miniaod/", 106900000),
# ("QCD_Pt_50to80_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJetL2L3_Autumn18_V3_MC/QCD_Pt_50to80_Pythia8_CP5_miniaod/", 15710000),
# ("QCD_Pt_80to120_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJetL2L3_Autumn18_V3_MC/QCD_Pt_80to120_Pythia8_CP5_miniaod/", 2336000),
# ("QCD_Pt_120to170_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJetL2L3_Autumn18_V3_MC/QCD_Pt_120to170_Pythia8_CP5_miniaod/", 407300),
# ("QCD_Pt_170to300_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJetL2L3_Autumn18_V3_MC/QCD_Pt_170to300_Pythia8_CP5_miniaod/", 103500),
# ("QCD_Pt_300to470_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJetL2L3_Autumn18_V3_MC/QCD_Pt_300to470_Pythia8_CP5_miniaod/", 6830),
# ("QCD_Pt_470to600_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJetL2L3_Autumn18_V3_MC/QCD_Pt_470to600_Pythia8_CP5_miniaod/", 552.1),
# ("QCD_Pt_600to800_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJetL2L3_Autumn18_V3_MC/QCD_Pt_600to800_Pythia8_CP5_miniaod/", 156.5),
# ("QCD_Pt_800to1000_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJetL2L3_Autumn18_V3_MC/QCD_Pt_800to1000_Pythia8_CP5_miniaod/", 26.28),
# ("QCD_Pt_1000to1400_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJetL2L3_Autumn18_V3_MC/QCD_Pt_1000to1400_Pythia8_CP5_miniaod/", 7.47),
# ("QCD_Pt_1400to1800_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJetL2L3_Autumn18_V3_MC/QCD_Pt_1400to1800_Pythia8_CP5_miniaod/", 0.648),
# ("QCD_Pt_1800to2400_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJetL2L3_Autumn18_V3_MC/QCD_Pt_1800to2400_Pythia8_CP5_miniaod/", 0.08743),
# ("QCD_Pt_2400to3200_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJetL2L3_Autumn18_V3_MC/QCD_Pt_2400to3200_Pythia8_CP5_miniaod/", 0.005236),
# ("QCD_Pt_3200toInf_NoJEC_newFlav", "QCD_Pt_Pythia8_CP5_miniaod_L1FastJetL2L3_Autumn18_V3_MC/QCD_Pt_3200toInf_Pythia8_CP5_miniaod/", 0.0001357),

# 2016 with L?
# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron/QCD_Pt_15to7000_Herwig_NoJEC_newFlav/", -1),

# 2017
# ("QCD_Pt_15to7000_Pythia8_CUETP8M1", "QCD_Pt_15to7000_Pythia8_CUETP8M1_Fall17_miniaod_L1FastJet_Fall17_17Nov2017_V32_MC/QCD_Pt_15to7000_Pythia8_CUETP8M1_Fall17_miniaod/", -1),
# ("QCD_Pt_15to7000_Pythia8_CP5", "QCD_Pt_15to7000_Pythia8_CP5_Fall17_miniaod_L1FastJet_Fall17_17Nov2017_V32_MC/QCD_Pt_15to7000_Pythia8_CP5_Fall17_miniaod", -1),


("QCD_Pt_15to7000_Herwig7_NoJEC_newFlav", "QCD_Pt_15to7000_Herwig7_miniaod_L1FastJet_Autumn18_V3_MC/QCD_Pt_15to7000_Herwig7_miniaod/", -1),
# ("QCD_Pt_15to7000_Herwigpp_NoJEC_newFlav", "QCD_Pt_15to7000_Herwigpp_miniaod_L1FastJet_Summer16_07Aug2017_V20_MC/QCD_Pt_15to7000_Herwigpp_miniaod_ext/", -1),

# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav_small", "QCD_Pt_Herwig_NoJEC_jtptmin4_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC/QCD_Pt_15to7000_Herwig_NoJEC_newFlav_small/", -1),
# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav_ext", "QCD_Pt_Herwig_NoJEC_jtptmin4_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_MC/QCD_Pt_15to7000_Herwig_NoJEC_newFlav_ext/", -1),

# ("QCD_Pt_15to7000_Herwig7_NoJEC_NoPU_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCH2_Flat_13TeV_herwig7/crab_QCD_Pt-15to7000_herwig7_noPU_02_Feb_19_Autumn18_noJEC_storeAllFlav_genEF_miniaod/190202_132418/0000/", -1),

# ("QCD_Pt_15to7000_Herwigpp_NoJEC_NoPU_miniaod", "/pnfs/desy.de/cms/tier2/store/user/raggleto/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/crab_QCD_Pt-15to7000_herwig_noPU_02_Feb_19_noJEC_storeAllFlav_genEF_miniaod/190202_134342/0000/", -1),

# ("GJets_Herwig_NoJEC_newFlav", "GJet_Herwig_NoJEC_relPtHatCut5_jtptmin4/GJets_Herwig_NoJEC_newFlav/", -1)

]


all_algos = [
    "ak4pfchs:0.2",
    # "ak4puppi:0.2",
    # "ak8pfchs:0.4",
    # "ak8puppi:0.4"
][:]

# output_dir = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4"
# output_dir = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s_nbinsrelrsp_10k" %(flav)
# output_dir = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V11_L1fix_MC_PhysicsAlgoHadron_applyL2%s_nbinsrelrsp_10k" %(flav)
# output_dir = "QCD_Pt_NoJEC_relPtHatCut2p5_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V11_L1fix_HadronParton_nbinsrelrsp_10k"
# output_dir = "QCD_Pt_NoJEC_relPtHatCut2p5_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_HadronParton_nbinsrelrsp_10k"
# output_dir = "QCD_Pt_withL1L2L3_Summer16_07Aug2017_V1_relPtHatCut5_jtptmin4"
# output_dir = "QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s_nbinsrelrsp_10k" % (flav)
# output_dir = "QCD_Pt_Herwig_NoJEC_relPtHatCut2p5_jtptmin4_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V11_L1fix_HadronParton_nbinsrelrsp_10k"
# output_dir = "QCD_Pt_Herwig_NoJEC_relPtHatCut2p5_jtptmin4_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_HadronParton_nbinsrelrsp_10k"
# output_dir = "GJets_Herwig_NoJEC_relPtHatCut5_jtptmin4_nbinsrelrsp_10k"
# output_dir = "QCD_Pt_Herwig7_NoJEC_NoPU_relPtHatCut2p5_jtptmin4_HadronParton_nbinsrelrsp_10k"
# output_dir = "QCD_Pt_Herwig7_NoJEC_relPtHatCut2p5_jtptmin4_HadronParton_nbinsrelrsp_10k"
# output_dir = "QCD_Pt_Herwigpp_NoJEC_NoPU_relPtHatCut2p5_jtptmin4_HadronParton_nbinsrelrsp_10k"
# output_dir = "QCD_Pt_Herwigpp_NoJEC_relPtHatCut2p5_jtptmin4_HadronParton_nbinsrelrsp_10k"
# output_dir = "QCD_Pt_Pythia8_CP5_NoJEC_relPtHatCut2p5_jtptmin4_HadronParton_nbinsrelrsp_10k_L1FastJetL2L3_Autumn18_V3_MC"
# output_dir = "QCD_Pt_Pythia8_CP5_NoJEC_relPtHatCut2p5_jtptmin4_HadronParton_nbinsrelrsp_10k_L1FastJetL2L3_Autumn18_V3_MC"
# output_dir = "QCD_PtFlat_Pythia8_CUETP8M1_NoJEC_relPtHatCut2p5_jtptmin4_HadronParton_nbinsrelrsp_10k_L1FastJet_Fall17_17Nov2017_V32_MC"
# output_dir = "QCD_PtFlat_Pythia8_CP5_NoJEC_relPtHatCut2p5_jtptmin4_HadronParton_nbinsrelrsp_10k_diffEtaBinnig_L1FastJet_Fall17_17Nov2017_V32_MC"

# output_dir = "QCD_Pt_Pythia8_CP5_NoJEC_genRelPtHatCut2_recoRelPtHatCut3_jtptmin4_HadronParton_nbinsrelrsp_10k_L1FastJet_Autumn18_V3_MC"
output_dir = "QCD_Pt_Herwig7_NoJEC_relPtHatCut2p5_jtptmin4_HadronParton_nbinsrelrsp_10k_L1FastJet_Autumn18_V3_MC"

if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

Nfiles = 15

job = dict_to_condor_contents(create_condor_template_dict())
job += "\n"
job += "JobBatchName=JRA\n"
arguments = ("jet_response_analyzer_x ../config/jra_flavour.config -input $(inputf) -output $(outputf) "
    "-algs $(algos) -flavorDefinition $(flavdef) "
    "-xsection $(xsec) -luminosity 35900 "
    "-jtptmin 4 -genrelpthatmax 2 -recorelpthatmax 3 "
    "-nbinspt 1000 "
    "-nbinsrelrsp 10000 -relrspmax 3 "
    "-useweight $(weight) -dorho true -dopudensity true "
)
job += "\narguments = %s\n\n" % arguments
job += "\nqueue\n"

job_args = []
job_names = []

hadd_job_names = []
hadd_job_args = []
hadd_job_depends = []

append = "{algo_name}_rspRangeLarge_absEta_hadronParton"
lim = '7000' if ("Herwig" in output_dir or "Flat" in output_dir) else "Inf"
final_file_template = "%s/jra_QCD_Pt_15to%s_NoJEC_newFlav_%s.root" % (output_dir, lim, append)

CACHE_FILENAME = "cache_nevents.csv"
NEVENTS_CACHE = get_cache(CACHE_FILENAME)


for algo in all_algos:
    algo_name, radius = algo.split(":")
    component_files = []
    these_job_names = []

    for name, input_dir, xsec in infos:

        # Split files to avoid running out of disk space on workers
        pattern = os.path.join(input_dir, "*.root")

        # To correctly weight for > 1 group, we need to scale the cross section
        # for each group of files by the fraction of events it contains
        # (otherwise it will be too large by a factor N groups)
        n_groups = len(list(grouper(glob(pattern), Nfiles, "")))
        do_rescale_xsec = n_groups > 1 and xsec > 0
        
        if do_rescale_xsec:
            print "Need to rescale xsecs, so need to check # events in each file...this could be slow..."
            all_input_files = glob(pattern)
            total_nevents = 0
            for ifile in all_input_files:
                abs_path = os.path.abspath(ifile)
                # update the global cache with the number of events in the files
                if abs_path not in NEVENTS_CACHE:
                    use_weight = True if ("flat" in input_dir.lower()) else False
                    this_nevents = count_events_in_file(input_file=abs_path,
                                                        dir_name=algo_name + "l1",
                                                        use_weight=use_weight)
                    NEVENTS_CACHE[abs_path] = this_nevents
                total_nevents += NEVENTS_CACHE[abs_path]

        # Now create a job for each group of files
        for ind, group in enumerate(grouper(glob(pattern), Nfiles, "")):
            group = [x for x in group if x]  # filter empties
            if do_rescale_xsec:
                # Get total number of events in this group of files
                this_nevents = sum(NEVENTS_CACHE[os.path.abspath(fname)] for fname in group)
                this_xsec_scaling = float(this_nevents) / float(total_nevents)
                print this_xsec_scaling
            else:
                this_xsec_scaling = 1

            args_dict = {
                "name": "JRA_"+name+"_"+algo_name+"_"+str(ind),
                # "inputf": os.path.join(input_dir, "*%s*.root" % algo_name),
                "inputf":  " ".join(group).strip(),
                "outputf": "%s/jra_%s_%s_%d.root" % (output_dir, name, append.format(algo_name=algo_name), ind),
                "xsec": "%.8f" % (xsec * this_xsec_scaling),  # scale xsec according to fraction of events in this group
                "algos": " ".join([algo, algo.replace(":", "l1l2l3:"), algo.replace(":", "l1:"), algo.replace(":", "l1l2:")]),
                # "flavdef": "hadron",
                "flavdef": "HADRONPARTON",
                "weight": "true" if xsec < 0 else "false",
            }
            job_args.append(" ".join(['%s="%s"' % (k, v) for k,v in args_dict.items()]))
            these_job_names.append(args_dict['name'])
            job_names.append(args_dict['name'])
            component_files.append(args_dict['outputf'])

    if len(component_files) > 1:
        final_output_file = final_file_template.format(algo_name=algo_name)
        hadd_name = "HADD_%s" % (algo.replace(":",'_').replace(".", "p"))
        hadd_job_args.append('name="%s" finalfile="%s" inputfiles="%s"' % (hadd_name, final_output_file, " ".join(component_files)))
        hadd_job_depends.append(' '.join(these_job_names))
        hadd_job_names.append(hadd_name)

if len(job_names) == 0:
    raise RuntimeError("Didn't find any files to run over!")

save_cache(NEVENTS_CACHE, CACHE_FILENAME)

job_filename = "htc_do_jet_response_analyzer_x_job_%s.condor" % (uuid1())
with open(job_filename, 'w') as f:
    f.write(job)

dag = ""
for ind, (job_name, job_args_entry) in enumerate(zip(job_names, job_args)):
    dag += "JOB {0} {1}\n".format(job_name, job_filename)
    dag += "VARS {0} {1}\n".format(job_name, job_args_entry)

# Add hadd jobs
hadd_job = dict_to_condor_contents(create_condor_template_dict())
hadd_job += "\n"
hadd_job += "JobBatchName=HaddJRA\n"
hadd_job += '\narguments = "hadd -f $(finalfile) $(inputfiles)"\n\n'
hadd_job += "\nqueue\n"

# if len(component_files) > 1:

#     hadd_htc_filename = "hadd_%s" % job_filename
#     with open(hadd_htc_filename, 'w') as f:
#         f.write(hadd_job)

#     dag += "JOB HADD {0}\n".format(hadd_htc_filename)
#     final_output_file = os.path.join(output_dir, "jra_%s_%s_rspRangeLarge_absEta_hadronParton.root" % (name, algo_name))
#     if os.path.isfile(final_output_file):
#         os.remove(final_output_file)
#     hadd_args = 'name="HADD" finalfile="%s" inputfiles="%s"' % (final_output_file, " ".join(component_files))
#     dag += "VARS HADD {0}\n".format(hadd_args)
#     dag += "PARENT {0} CHILD HADD\n".format(' '.join(job_names), hname)

 # Add hadd jobs
hadd_htc_filename = "HADD_%s" % job_filename
with open(hadd_htc_filename, 'w') as f:
    f.write(hadd_job)

for ind, (hname, harg, hdeps) in enumerate(zip(hadd_job_names, hadd_job_args, hadd_job_depends)):
    dag += "JOB {0} {1}\n".format(hname, hadd_htc_filename)
    dag += "VARS {0} {1}\n".format(hname, harg)
    dag += "PARENT {0} CHILD {1}\n".format(hdeps, hname)


dag += "RETRY ALL_NODES 3\n"
status_file = job_filename.replace(".condor", ".dagstatus")
dag += "NODE_STATUS_FILE %s\n" % (status_file)

dag_filename = job_filename.replace(".condor", ".dag")
with open(dag_filename, 'w') as f:
    f.write(dag)

print "Submitting", len(job_names), "jobs"
cmd = "condor_submit_dag -maxjobs 200 -maxidle 1000 -f %s" % dag_filename
subprocess.check_call(cmd, shell=True)
print "Check status with:"
print "DAGstatus", status_file
