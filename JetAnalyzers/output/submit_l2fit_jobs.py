#!/usr/bin/env python


"""Submit jet_l2_correction_x jobs to HTCondor to do different flav fitting in parallel"""


import os
import subprocess
from glob import glob
from itertools import izip_longest


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

job = dict_to_condor_contents(create_condor_template_dict())
job += "\n"
job += "JobBatchName=JL2C\n"
arguments = ('jet_l2_correction_x '
    '-input $(inputf) -algs $(algos) -useLastFitParams true '
    '-minRelCorErr 0.01 -l2l3 true -histMet median -era $(era) '
    '-outputDir $(outputdir) -output $(outputfile) -batch true '
    '-flavor $(pdgid) -fitMin $(fitmin) -l2pffit $(fitfunc)'
)
job += '\narguments = "%s"\n\n' % arguments
job += "\nqueue\n"

infos = [

# ("QCD_Pt_15toInf_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k/jra_QCD_Pt_15toInf_NoJEC_newFlav_ak4pfchs_L1FastJet_fineBinning_rspRangeLarge_absEta.root"),
# ("QCD_Pt_15toInf_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k/jra_QCD_Pt_15toInf_NoJEC_newFlav_ak4pfchs_L1FastJet_wideBinning_rspRangeLarge_absEta.root"),
# ("QCD_Pt_15toInf_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_nbinsrelrsp_10k/jra_QCD_Pt_15toInf_NoJEC_newFlav_ak4pfchs_L1FastJet_wideBinning_rspRangeLarge_absEta_hadron.root"),
# ("QCD_Pt_15toInf_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut2p5_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_HadronParton_nbinsrelrsp_10k/jra_QCD_Pt_15toInf_NoJEC_newFlav_ak4pfchs_L1FastJet_rspRangeLarge_absEta_hadronParton.root"),
("QCD_Pt_15toInf_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut2p5_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_HadronParton_nbinsrelrsp_10k_fineBinning_etaPlusMinus/jra_QCD_Pt_15toInf_NoJEC_newFlav_ak4pfchs_L1FastJet_rspRangeLarge_hadronParton.root"),
# ("QCD_Pt_15toInf_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut2p5_jtptmin4_withPF_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_parton_nbinsrelrsp_10k_fineBinning_etaPlusMinus/jra_QCD_Pt_15toInf_NoJEC_newFlav_ak4pfchs_L1FastJet_rspRangeLarge_physicsparton.root"),

# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k/jra_QCD_Pt_15to7000_Herwig_NoJEC_newFlav_ak4pfchs_L1FastJet_fineBinning_rspRangeLarge_absEta.root"),
# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k/jra_QCD_Pt_15to7000_Herwig_NoJEC_newFlav_ak4pfchs_L1FastJet_wideBinning_rspRangeLarge_absEta_hadron.root"),
# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_nbinsrelrsp_10k/jra_QCD_Pt_15to7000_Herwig_NoJEC_newFlav_ak4pfchs_L1FastJet_wideBinning_rspRangeLarge_absEta_hadron.root"),
# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V11_L1fix_HadronParton_nbinsrelrsp_10k/jra_QCD_Pt_15to7000_Herwig_NoJEC_newFlav_ak4pfchs_L1FastJet_rspRangeLarge_absEta_hadronParton.root"),
# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "QCD_Pt_Herwig_NoJEC_relPtHatCut2p5_jtptmin4_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_HadronParton_nbinsrelrsp_10k/jra_QCD_Pt_15to7000_Herwig_NoJEC_newFlav_ext_ak4pfchs_L1FastJet_rspRangeLarge_absEta_hadronParton.root"),
("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "QCD_Pt_Herwig_NoJEC_relPtHatCut2p5_jtptmin4_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_HadronParton_nbinsrelrsp_10k_fineBinning_etaPlusMinus/jra_QCD_Pt_15to7000_Herwig_NoJEC_newFlav_ak4pfchs_L1FastJet_rspRangeLarge_hadronParton.root"),
# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "QCD_Pt_Herwig_NoJEC_relPtHatCut2p5_jtptmin4_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_parton_nbinsrelrsp_10k_fineBinning_etaPlusMinus/jra_QCD_Pt_15to7000_Herwig_NoJEC_newFlav_ak4pfchs_L1FastJet_rspRangeLarge_physicsparton.root"),

]


all_algos = [
    "ak4pfchsl1",
    # "ak4puppil1",
    # "ak8pfchsl1",
    # "ak8puppil1"
][:]

flavours = [
    # "ud_",
    "s_",
    "c_",
    "b_",
    "g_",
    "",
]

fit_min = 15
fit_func = "standard"
# fit_func = "powerlaw"

append = "_standardMedianErr_allMedian_rspRangeLarge_fitMin%d_fitFunc%s_HadronParton_useLastFitParams_minRelCorErr0p01" % (fit_min, fit_func)

job_args = []
job_names = []

for name, input_file in infos:
    input_dir = os.path.dirname(input_file)

    for algo in all_algos:
        for flav in flavours:
            flav_name = "all" if flav == "" else flav.rstrip("_")
            args_dict = {
                "name": "JL2_"+name+"_"+algo+"_"+flav_name,
                "inputf": input_file,
                "outputdir": input_dir,
                "outputfile": "l2%s_%s.root" % (append, flav_name),
                "algos": algo,
                "pdgid": flav,
                "era": "Summer16_07Aug2017_V15_%s_%s" % (append, flav_name),
                "fitmin" : str(fit_min),
                "fitfunc": fit_func,
            }
            job_args.append(" ".join(['%s="%s"' % (k, v) for k,v in args_dict.items()]))
            job_names.append(args_dict['name'])


if len(job_names) == 0:
    raise RuntimeError("Didn't find any files to run over!")

job_filename = "htc_do_jet_l2_correction_x_job.condor"
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
