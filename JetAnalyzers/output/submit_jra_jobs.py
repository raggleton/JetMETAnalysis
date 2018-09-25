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


flav = "s"
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
("QCD_Pt_15to30_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s/QCD_Pt_15to30_NoJEC_newFlav/" % (flav), 1837410000),
("QCD_Pt_30to50_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s/QCD_Pt_30to50_NoJEC_newFlav/" % (flav), 140932000),
("QCD_Pt_50to80_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s/QCD_Pt_50to80_NoJEC_newFlav/" % (flav), 19204300),
("QCD_Pt_80to120_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s/QCD_Pt_80to120_NoJEC_newFlav/" % (flav), 2762530),
("QCD_Pt_120to170_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s/QCD_Pt_120to170_NoJEC_newFlav/" % (flav), 471100),
("QCD_Pt_170to300_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s/QCD_Pt_170to300_NoJEC_newFlav/" % (flav), 117276),
("QCD_Pt_300to470_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s/QCD_Pt_300to470_NoJEC_newFlav/" % (flav), 7823),
("QCD_Pt_470to600_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s/QCD_Pt_470to600_NoJEC_newFlav/" % (flav), 648.2),
("QCD_Pt_600to800_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s/QCD_Pt_600to800_NoJEC_newFlav/" % (flav), 186.9),
("QCD_Pt_800to1000_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s/QCD_Pt_800to1000_NoJEC_newFlav/" % (flav), 32.293),
("QCD_Pt_1000to1400_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s/QCD_Pt_1000to1400_NoJEC_newFlav/" % (flav), 9.4183),
("QCD_Pt_1400to1800_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s/QCD_Pt_1400to1800_NoJEC_newFlav/" % (flav), 0.84265),
("QCD_Pt_1800to2400_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s/QCD_Pt_1800to2400_NoJEC_newFlav/" % (flav), 0.114943),
("QCD_Pt_2400to3200_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s/QCD_Pt_2400to3200_NoJEC_newFlav/" % (flav), 0.0068298),
("QCD_Pt_3200toInf_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s/QCD_Pt_3200toInf_NoJEC_newFlav/" % (flav), 0.0001654),

# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron/QCD_Pt_15to7000_Herwig_NoJEC_newFlav/", -1)

# ("GJets_Herwig_NoJEC_newFlav", "GJet_Herwig_NoJEC_relPtHatCut5_jtptmin4/GJets_Herwig_NoJEC_newFlav/", -1)

]


all_algos = [
    "ak4pfchs:0.2",
    # "ak4puppi:0.2",
    # "ak8pfchs:0.4",
    # "ak8puppi:0.4"
][:]

# output_dir = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4"
output_dir = "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s_nbinsrelrsp_10k" %(flav)
# output_dir = "QCD_Pt_withL1L2L3_Summer16_07Aug2017_V1_relPtHatCut5_jtptmin4"
# output_dir = "QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2%s_nbinsrelrsp_10k" % (flav)
# output_dir = "GJets_Herwig_NoJEC_relPtHatCut5_jtptmin4_nbinsrelrsp_10k"

if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

Nfiles = 5

job = dict_to_condor_contents(create_condor_template_dict())
job += "\n"
job += "JobBatchName=JRA\n"
arguments = ("jet_response_analyzer_x ../config/jra_flavour.config -input $(inputf) -output $(outputf) "
    "-algs $(algos) -flavorDefinition $(flavdef) "
    "-xsection $(xsec) -luminosity 35900 "
    "-jtptmin 4 -relpthatmax 2.5 "
    "-nbinsrelrsp 10000 -relrspmax 6 "
    "-useweight $(weight)"
)
job += "\narguments = %s\n\n" % arguments
job += "\nqueue\n"

job_args = []
job_names = []
for name, input_dir, xsec in infos:
    for algo in all_algos:
        algo_name, radius = algo.split(":")

        # Split files to avoid running out of disk space on workers
        pattern = os.path.join(input_dir, "*.root")

        for ind, group in enumerate(grouper(glob(pattern), Nfiles, "")):

            args_dict = {
                "name": "JRA_"+name+"_"+algo_name+"_"+str(ind),
                # "inputf": os.path.join(input_dir, "*%s*.root" % algo_name),
                "inputf":  " ".join(group).strip(),
                "outputf": "%s/jra_%s_%s_L1FastJet_rspRangeLarge_absEta_hadronParton_%d.root" % (output_dir, name, algo_name, ind),
                "xsec": "%.8f" % xsec,
                "algos": " ".join([algo, algo.replace(":", "l1l2l3:"), algo.replace(":", "l1:"), algo.replace(":", "l1l2:")]),
                # "flavdef": "hadron",
                "flavdef": "HADRONPARTON",
                "weight": "true",
            }
            # job += "\n".join(["%s=%s" % (k, v) for k,v in args_dict.items()])
            # job += "\nqueue\n\n"
            job_args.append(" ".join(['%s="%s"' % (k, v) for k,v in args_dict.items()]))
            job_names.append(args_dict['name'])

print job

if len(job_names) == 0:
    raise RuntimeError("Didn't find any files to run over!")

# job_filename = "do_jet_response_analyzer_x_job_%s.condor" % (flav)
# job_filename = "htc_do_jet_response_analyzer_x_job_2017a.condor"
job_filename = "htc_do_jet_response_analyzer_x_job_2016.condor"
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
print "Check status with:"
print "DAGstatus", status_file
