#!/usr/bin/env python

import os
import subprocess


infos = [
# ("QCD_Pt_15toInf_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_nbinsrelrsp_10k/jrf_QCD_Pt_15toInf_NoJEC_newFlav_ak4pfchsl1_L1FastJet_wideBinning_rspRangeLarge_absEta_physicsParton_rebin50.root"),
("QCD_Pt_15toInf_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2All_nbinsrelrsp_10k/jrf_QCD_Pt_15toInf_NoJEC_newFlav_ak4pfchsl1l2_L1FastJet_wideBinning_rspRangeLarge_absEta_physicsParton_rebin50.root"),
# ("QCD_Pt_15toInf_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2g_nbinsrelrsp_10k/jrf_QCD_Pt_15toInf_NoJEC_newFlav_ak4pfchsl1l2_L1FastJet_wideBinning_rspRangeLarge_absEta_physicsParton_rebin50.root"),
# ("QCD_Pt_15toInf_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_applyL2ud_nbinsrelrsp_10k/jrf_QCD_Pt_15toInf_NoJEC_newFlav_ak4pfchsl1l2_L1FastJet_wideBinning_rspRangeLarge_absEta_physicsParton_rebin50.root"),

# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_nbinsrelrsp_10k/jrf_QCD_Pt_15to7000_Herwig_NoJEC_newFlav_ak4pfchsl1_L1FastJet_wideBinning_rspRangeLarge_absEta_physicsParton_rebin50.root"),
]


all_algos = [
    # "ak4pfchsl1",
    "ak4pfchsl1l2",
][:]

metric = "fitMean"
append = "L1FastJet_wideBinning_rspRangeLarge_absEta_physicsParton_rebin50_%s.root" % (metric)

for name, input_file in infos:
    output_dir = os.path.dirname(input_file)
    for algo in all_algos:
        args_dict = {
            "inputf": input_file,
            "outputf": os.path.join(output_dir, "jrar_%s_%s_%s" % (name, algo, append)),
            "algos": algo,
            "metric": metric
        }
        cmd = "jet_response_and_resolution_x -input {inputf} -output {outputf} -algs {algos} -flavors all -metric {metric} -fitres false ".format(**args_dict)
        subprocess.check_call(cmd, shell=True)
