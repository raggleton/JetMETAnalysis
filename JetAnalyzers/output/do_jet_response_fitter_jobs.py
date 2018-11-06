#!/usr/bin/env python

import os
import subprocess


infos = [
# ("QCD_Pt_15toInf_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_nbinsrelrsp_10k/jra_QCD_Pt_15toInf_NoJEC_newFlav_ak4pfchs_L1FastJet_wideBinning_rspRangeLarge_absEta_physicsParton.root"),

("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_nbinsrelrsp_10k/jra_QCD_Pt_15to7000_Herwig_NoJEC_newFlav_ak4pfchs_L1FastJet_wideBinning_rspRangeLarge_absEta_physicsParton.root"),
]


all_algos = [
    "ak4pfchsl1",
][:]

rebin = 50
append = "L1FastJet_wideBinning_rspRangeLarge_absEta_physicsParton_rebin%d.root" % (rebin)

for name, input_file in infos:
    output_dir = os.path.dirname(input_file)
    for algo in all_algos:
        output_filename = os.path.join(output_dir, "jrf_%s_%s_%s" % (name, algo, append))
        args_dict = {
            "inputf": input_file,
            "outputf": output_filename,
            "algos": algo,
            "rebin": str(rebin),
        }
        if os.path.isfile(output_filename):
            os.remove(output_filename)
        cmd = "jet_response_fitter_x -input {inputf} -output {outputf} -algs {algos} -doFlavor true -rebin {rebin}".format(**args_dict)
        subprocess.check_call(cmd, shell=True)
