#!/usr/bin/env python

import os
import subprocess

def create_condor_template_dict():
    template = {
        "executable": "",
        "transfer_executable": "True",
        "universe": "vanilla",
        "output": "$(Cluster)_$(Process).out",
        "error": "$(Cluster)_$(Process).err",
        "log": "$(Cluster)_$(Process).log",
        "RequestMemory": "2G",
        "RequestDisk": "2G",
        "requirements": 'OpSysAndVer == "SL6"',
        "initialdir": "",
        "getenv": "True",
        "environment": "LD_LIBRARY_PATH_STORED="+os.environ.get('LD_LIBRARY_PATH'),
        "notification": "e",
        "notify_user": "robin.aggleton@desy.de",
    }
    return template


def dict_to_condor_contents(input_dict):
    contents = ['%s="%s"' % (k, str(v)) for k, v in input_dict.items()]
    return "\n".join(contents)


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

# for after doing jet_apply_jec_x
("QCD_Pt_15to30_NoJEC_newFlav", "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output/QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/QCD_Pt_15to30_NoJEC_newFlav/", 1837410000),
("QCD_Pt_30to50_NoJEC_newFlav", "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output/QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/QCD_Pt_30to50_NoJEC_newFlav/", 140932000),
("QCD_Pt_50to80_NoJEC_newFlav", "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output/QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/QCD_Pt_50to80_NoJEC_newFlav/", 19204300),
("QCD_Pt_80to120_NoJEC_newFlav", "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output/QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/QCD_Pt_80to120_NoJEC_newFlav/", 2762530),
("QCD_Pt_120to170_NoJEC_newFlav", "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output/QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/QCD_Pt_120to170_NoJEC_newFlav/", 471100),
("QCD_Pt_170to300_NoJEC_newFlav", "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output/QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/QCD_Pt_170to300_NoJEC_newFlav/", 117276),
("QCD_Pt_300to470_NoJEC_newFlav", "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output/QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/QCD_Pt_300to470_NoJEC_newFlav/", 7823),
("QCD_Pt_470to600_NoJEC_newFlav", "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output/QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/QCD_Pt_470to600_NoJEC_newFlav/", 648.2),
("QCD_Pt_600to800_NoJEC_newFlav", "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output/QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/QCD_Pt_600to800_NoJEC_newFlav/", 186.9),
("QCD_Pt_800to1000_NoJEC_newFlav", "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output/QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/QCD_Pt_800to1000_NoJEC_newFlav/", 32.293),
("QCD_Pt_1000to1400_NoJEC_newFlav", "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output/QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/QCD_Pt_1000to1400_NoJEC_newFlav/", 9.4183),
("QCD_Pt_1400to1800_NoJEC_newFlav", "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output/QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/QCD_Pt_1400to1800_NoJEC_newFlav/", 0.84265),
("QCD_Pt_1800to2400_NoJEC_newFlav", "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output/QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/QCD_Pt_1800to2400_NoJEC_newFlav/", 0.114943),
("QCD_Pt_2400to3200_NoJEC_newFlav", "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output/QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/QCD_Pt_2400to3200_NoJEC_newFlav/", 0.0068298),
("QCD_Pt_3200toInf_NoJEC_newFlav", "/nfs/dust/cms/user/aggleton/JEC/CMSSW_8_0_28/src/JetMETAnalysis/JetAnalyzers/output/QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/QCD_Pt_3200toInf_NoJEC_newFlav/", 0.0001654),

("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10/QCD_Pt_15to7000_Herwig_NoJEC_newFlav/", -1)

# ("GJets_Herwig_NoJEC_newFlav", "GJet_Herwig_NoJEC_relPtHatCut5_jtptmin4/GJets_Herwig_NoJEC_newFlav/", -1)

]


all_algos = [
    "ak4pfchs:0.2",
    # "ak4puppi:0.2",
    # "ak8pfchs:0.4",
    # "ak8puppi:0.4"
][:]

# output_dir = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4"
output_dir = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k"
# output_dir = "QCD_Pt_withL1L2L3_Summer16_07Aug2017_V1_relPtHatCut5_jtptmin4"
# output_dir = "QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k"
# output_dir = "GJets_Herwig_NoJEC_relPtHatCut5_jtptmin4_nbinsrelrsp_10k"

if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

for name, input_dir, xsec in infos:
    for algo in all_algos:
        algo_name, radius = algo.split(":")
        args_dict = {
            "name": "JRA_"+name+"_"+algo_name, 
            "input": os.path.join(input_dir, "*%s*.root" % algo_name), 
            "output": "%s/jra_%s_%s_L1FastJet_wideBinning_rspRangeLarge_dummy.root" % (output_dir, name, algo_name),
            "xsec": "%.4f" % xsec, 
            "algos": " ".join([algo, algo.replace(":", "l1l2l3:"), algo.replace(":", "l1:")]),
            "flavdef": "NEW",
            "weight": "true",
        }

        # cmd = "condor_qsub -N {name} -v JRAINPUT='{input}',JRAOUTPUT={output},XSEC={xsec},ALGOS='{algos}',FLAVDEF={flavdef},WEIGHT={weight} do_jet_response_analyzer_x_job.sh".format(**args_dict)
        # print cmd
        # subprocess.check_call(cmd, shell=True)
        cmd = 'jet_response_analyzer_x ../config/jra_flavour.config -input {input} -output {output} -algs {algos} -flavorDefinition {flavdef} -xsection {xsec} -luminosity 35900 -jtptmin 4 -relpthatmax 5 -nbinsrelrsp 10000  -relrspmax 6 -useweight {weight}'.format(**args_dict)
        print cmd
        condor_dict = create_condor_template_dict()
        condor_dict['output'] = args_dict['name'] + "_" + condor_dict['output']
        condor_dict['error'] = args_dict['name'] + "_" + condor_dict['error']
        condor_dict['log'] = args_dict['name'] + "_" + condor_dict['log']
        condor_dict['executable'] = "run_prog.sh"
        # print dict_to_condor_contents(condor_dict)

