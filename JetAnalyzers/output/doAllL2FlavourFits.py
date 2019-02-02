#!/usr/bin/env python

import os
import subprocess
from glob import glob


def float2str(num):
    return str(num).replace(".", "p")


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
# ("QCD_Pt_15to7000_Herwig_NoJEC_newFlav", "QCD_Pt_Herwig_NoJEC_relPtHatCut2p5_jtptmin4_PhysicsAlgoHadron_L1FastJet_Summer16_07Aug2017_V15_HadronParton_nbinsrelrsp_10k_fineBinning_etaPlusMinus/jra_QCD_Pt_15to7000_Herwig_NoJEC_newFlav_ak4pfchs_L1FastJet_rspRangeLarge_hadronParton.root"),
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
    # "s_",
    # "c_",
    # "b_",
    # "g_",
    "",
]

fit_min = 10
fit_func = "standard"
# fit_func = "powerlaw"
min_rel_cor_err = 0.01

append = "_standardMedianErr_allMedian_rspRangeLarge_fitMin%d_fitFunc%s_HadronParton_minRelCorErr0p01" % (fit_min, fit_func)
append = "_standardMedianErr_allMedian_rspRangeLarge_fitMin%d_fitFunc%s_HadronParton_minRelCorErr%s_setFitMinTurnoverPlusOne_plateauBelowRangeMin" % (fit_min, fit_func, float2str(min_rel_cor_err))

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
                "era": "Summer16_07Aug2017_V15_%s_%s" % (append, flav_name),
                "fitmin" : str(fit_min),
                "fitfunc": fit_func,
                "minrelcorerr": float2str(min_rel_cor_err),
            }
            args_dict  = {k.upper(): v for k, v in args_dict.items()}
            cmd = 'jet_l2_correction_x -input "{INPUT}" -algs "{ALGOS}" -useLastFitParams false -chooseByMaxDiff true -setFitMinTurnover true -plateauBelowRangeMin true -minRelCorErr {MINRELCORERR} -l2l3 true -histMet median -era "{ERA}" -outputDir "{OUTPUTDIR}" -output "{OUTPUTFILE}" -batch true -flavor "{PDGID}" -fitMin "{FITMIN}" -l2pffit "{FITFUNC}"'.format(**args_dict)
            print cmd
            subprocess.call(cmd, shell=True)
