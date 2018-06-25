#!/usr/bin/env python

import os
import subprocess
from glob import glob


infos = [

# ("QCD_Pt_15toInf_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k/jra_QCD_Pt_15toInf_NoJEC_newFlav_ak4pfchs_L1FastJet_fineBinning_rspRangeLarge_absEta.root"),
# ("QCD_Pt_15toInf_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k/jra_QCD_Pt_15toInf_NoJEC_newFlav_ak4pfchs_L1FastJet_wideBinning_rspRangeLarge_absEta.root"),
# ("QCD_Pt_15toInf_NoJEC_newFlav", "QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_nbinsrelrsp_10k/jra_QCD_Pt_15toInf_NoJEC_newFlav_ak4pfchs_L1FastJet_wideBinning_rspRangeLarge_absEta_hadron.root"),

# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k/jra_QCD_Pt_15to7000_Herwig_NoJEC_newFlav_ak4pfchs_L1FastJet_fineBinning_rspRangeLarge_absEta.root")
# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_nbinsrelrsp_10k/jra_QCD_Pt_15to7000_Herwig_NoJEC_newFlav_ak4pfchs_L1FastJet_wideBinning_rspRangeLarge_absEta_hadron.root")
("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "QCD_Pt_Herwig_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron_nbinsrelrsp_10k/jra_QCD_Pt_15to7000_Herwig_NoJEC_newFlav_ak4pfchs_L1FastJet_wideBinning_rspRangeLarge_absEta_hadron.root")

]


all_algos = [
    "ak4pfchsl1",
    # "ak4puppil1",
    # "ak8pfchsl1",
    # "ak8puppil1"
][:]

flavours = [
    # "ud_",
    # "s_",
    "c_",
    "b_",
    # "g_",
    # "",
]

fit_min = 15

append = "_standardMedianErr_allMedian_rspRangeLarge_fitMin%d_useFitRange_wideBinning_absEta_hadron" % fit_min

for name, input_file in infos:
    input_dir = os.path.dirname(input_file)

    for algo in all_algos:
        for flav in flavours:
            flav_name = "all" if flav == "" else flav.rstrip("_")
            args_dict = {
                "input": input_file,
                "outputdir": input_dir,
                "outputfile": "l2%s_%s.root" % (append, flav_name),
                "algos": algo,
                "pdgid": flav,
                "era": "Summer16_07Aug2017_V10%s_%s" % (append, flav_name),
                "fitmin" : str(fit_min),
            }
            args_dict  = {k.upper(): v for k, v in args_dict.items()}
            cmd = 'jet_l2_correction_x -input "{INPUT}" -algs "{ALGOS}" -l2l3 true -histMet median -era "{ERA}" -outputDir "{OUTPUTDIR}" -output "{OUTPUTFILE}" -batch true -flavor "{PDGID}" -fitMin "{FITMIN}" -l2pffit standard'.format(**args_dict)
            print cmd
            subprocess.call(cmd, shell=True)
