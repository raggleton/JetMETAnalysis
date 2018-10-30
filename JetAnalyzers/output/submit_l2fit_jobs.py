#!/usr/bin/env python


"""Submit jet_l2_correction_x jobs to HTCondor to do different flav fitting in parallel"""


import os
import subprocess
from glob import glob
from itertools import izip_longest


def float2str(num):
    return str(num).replace(".", "p")


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
    '-input $(inputf) -algs $(algos) -useLastFitParams false '
    '-minRelCorErr $(minrelcorerr) -l2l3 true -histMet median -era $(era) '
    '-outputDir $(outputdir) -output $(outputfile) -batch true '
    '-flavor $(pdgid) -fitMin $(fitmin) -l2pffit $(fitfunc) '
    '-setFitMinTurnover true -plateauBelowRangeMin true '
    '-chooseByMaxDiff true'
)
job += '\narguments = "%s"\n\n' % arguments
job += "\nqueue\n"


hadd_job = dict_to_condor_contents(create_condor_template_dict())
hadd_job += "\n"
hadd_job += "JobBatchName=HaddL2\n"
hadd_job += '\narguments = "hadd -f $(finalfile) $(inputfiles)"\n\n'
hadd_job += "\nqueue\n"


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
    "ud_",
    "s_",
    "c_",
    "b_",
    "g_",
    # "",
]

fit_min = 10
fit_func = "standard"
# fit_func = "powerlaw"
min_rel_cor_err = 0.005

append = "_standardMedianErr_allMedian_rspRangeLarge_fitMin%d_fitFunc%s_HadronParton_minRelCorErr%s_setFitMinTurnoverPlusOne_plateauBelowRangeMin_minRelCorErrMaxRelDiffCompete" % (fit_min, fit_func, float2str(min_rel_cor_err))

job_args = []
job_names = []

hadd_job_names = []
hadd_job_args = []
hadd_job_depends = []

for name, input_file in infos:
    input_dir = os.path.dirname(input_file)

    for algo in all_algos:
        these_job_names = []
        component_files = []

        for flav in flavours:
            flav_name = "all" if flav == "" else flav.rstrip("_")
            args_dict = {
                "name": "JL2_"+name+"_"+algo+"_"+flav_name,
                "inputf": input_file,
                "outputdir": input_dir,
                "outputfile": "l2%s_%s.root" % (append, flav_name),
                "algos": algo,
                "pdgid": flav if flav != "" else '\"\"',
                "era": "Summer16_07Aug2017_V15_%s_%s" % (append, flav_name),
                "fitmin" : str(fit_min),
                "fitfunc": fit_func,
                "minrelcorerr": str(min_rel_cor_err),
            }
            job_args.append(" ".join(['%s="%s"' % (k, v) for k,v in args_dict.items()]))
            these_job_names.append(args_dict['name'])
            component_files.append(os.path.join(args_dict['outputdir'], args_dict['outputfile']))

        job_names.extend(these_job_names)
        final_output_file = os.path.join(input_dir, "l2%s.root" % append)
        hadd_name = "HADD_%s_%s" % (name, algo)
        hadd_job_args.append('name="%s" finalfile="%s" inputfiles="%s"' % (hadd_name, final_output_file, " ".join(component_files)))
        hadd_job_depends.append(' '.join(these_job_names))
        hadd_job_names.append(hadd_name)


if len(job_names) == 0:
    raise RuntimeError("Didn't find any files to run over!")

htc_filename = "htc_do_jet_l2_correction_x_job.condor"
with open(htc_filename, 'w') as f:
    f.write(job)

dag = ""
for ind, (job_name, job_args_entry) in enumerate(zip(job_names, job_args)):
    dag += "JOB {0} {1}\n".format(job_name, htc_filename)
    dag += "VARS {0} {1}\n".format(job_name, job_args_entry)

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
