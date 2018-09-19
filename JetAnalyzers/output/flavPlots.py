#!/usr/bin/env python

import numpy as np
import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(1)
ROOT.TH1.SetDefaultSumw2()
ROOT.gStyle.SetOptStat(0)

ROOT.gStyle.SetPaintTextFormat(".3g")


chain = ROOT.TChain("ak4pfchsl1/t")
chain.Add("QCD_Pt_NoJEC_relPtHatCut5_jtptmin4_withPF_Summer16_07Aug2017_V10_PhysicsAlgoHadron/QCD_Pt_120to170_NoJEC_newFlav/jaj_QCD_Pt_120to170_NoJEC_newFlav_ak4pfchs_L1FastJet_*.root")


def th2_to_arr(h):
    """Convert TH2 to 2D numpy array"""
    arr = np.zeros((h.GetNbinsX(), h.GetNbinsY()))
    for x_ind in xrange(1, h.GetNbinsX() + 1):
        for y_ind in xrange(1, h.GetNbinsY() + 1):
            arr[x_ind-1][y_ind-1] = h.GetBinContent(x_ind, y_ind)
    return arr


def make_normalised_TH2(hist, norm_axis, recolour=True):
    norm_axis = norm_axis.upper()
    possible_opts = ['X', 'Y']
    if norm_axis not in possible_opts:
        raise RuntimeError("norm_axis must be one of %s" % possible_opts)
    norm_axis = norm_axis.upper()

    # easiest way to cope with x or y is to just get a 2D matrix of values,
    # can then do transpose if necessary
    arr = th2_to_arr(hist)

    if norm_axis == 'Y':
        arr = arr.T
    if recolour:
        # can set so the maximum in each bin is the same,
        # scale other bins accordingly
        # this retain the colour scheme for each set of bins
        for ind, xbin in enumerate(arr):
            if xbin.max() > 0:
                arr[ind] = xbin / xbin.max()
    else:
        # alternatively, can rescale so sum over bins = 1
        for ind, xbin in enumerate(arr):
            if xbin.sum() != 0:
                arr[ind] = xbin / xbin.sum()

    if norm_axis == 'Y':
        arr = arr.T

    # Create new hist object - MUST do it this way to get Z range correct
    new_histname = hist.GetName() + "_norm" + norm_axis
    # hnew = ROOT.TH2F(hist)  # TODO: determine if TH2F, TH2D...
    if type(hist) == ROOT.TH2F:
        hnew = ROOT.TH2F(hist)  # TODO: determine if TH2F, TH2D...
    elif type(hist) == ROOT.TH2D:
        hnew = ROOT.TH2D(hist)  # TODO: determine if TH2F, TH2D...
    else:
        raise RuntimeError("Unknown 2D hist type")
    hnew.SetName(new_histname)
    for x_ind, x_arr in enumerate(arr, 1):
        for y_ind, val in enumerate(x_arr, 1):
            hnew.SetBinContent(x_ind, y_ind, val)
#     hnew.SetAxisRange(0.5, 1., 'Z')
    return hnew


def do_flav_correlation_plot(cuts, output_filename, title=""):
    canv = ROOT.TCanvas("canv"+ROOT.TUUID().AsString(), "", 800, 800)
    canv.SetLogz()
    hname = "corr"+ROOT.TUUID().AsString()
    h_corr = ROOT.TH2D(hname, title+";physics parton flavour;hadron flavour", 22, -0.5, 21.5, 6, -0.5, 5.5)
    chain.Draw("refpdgid_hadron:refpdgid_parton_physics>>"+hname, cuts, "COLZ TEXT")
    # h_corr.SetMarkerSize()
    h_corr_norm = make_normalised_TH2(h_corr, "y", False)
    h_corr_norm.Draw("COLZ TEXT89")
    canv.SaveAs(output_filename)


# do_flav_correlation_plot("refpt>120 && refpt<170 && TMath::Abs(refeta) < 0.7 && refpt/pthat < 2.5", "flavCorrPlots/flavCorr_pt120to170_eta0to0p7.pdf", "120 < p_{T} < 170 GeV, |#eta| < 0.7")

colours = [
ROOT.kRed,
ROOT.kBlue,
ROOT.kGreen+1,
ROOT.kMagenta-4,
ROOT.kOrange-3,
]

def do_response_plot(selections, labels, output_filename, title):
    if isinstance(selections, str):
        selections = [selections]
    canv = ROOT.TCanvas("canv"+ROOT.TUUID().AsString(), "", 800, 800)
    hst = ROOT.THStack("hst"+ROOT.TUUID().AsString(), title+";Response (p_{T}^{Reco}/p_{T}^{Gen});p.d.f")
    hists = []
    leg = ROOT.TLegend(0.6, 0.6, 0.88, 0.88)
    leg.SetBorderSize(0)
    for ind, (cut, label) in enumerate(zip(selections, labels)):
        print cut, label
        hname = "h"+str(ind)+ROOT.TUUID().AsString()
        h = ROOT.TH1D(hname, title+";Response (p_{T}^{Reco}/p_{T}^{Gen});p.d.f", 25, 0.5, 1.5)
        chain.Draw("jtpt/refpt>>"+hname, cut)
        h.SetLineColor(colours[ind])
        h.SetLineWidth(2)
        h.Scale(1./h.Integral())
        hists.append(h)
        hst.Add(h)
        leg.AddEntry(h, label, "L")
    hst.Draw("HISTE NOSTACK")
    leg.Draw()
    canv.SaveAs(output_filename)


do_response_plot(
[
    "TMath::Abs(refpdgid_parton_physics)!=5 && TMath::Abs(refpdgid_hadron)==5 && refpt>120 && refpt<170 && TMath::Abs(refeta) < 0.7 && refpt/pthat < 2.5",
    "TMath::Abs(refpdgid_parton_physics)==5 && TMath::Abs(refpdgid_hadron)!=5 && refpt>120 && refpt<170 && TMath::Abs(refeta) < 0.7 && refpt/pthat < 2.5",
    "TMath::Abs(refpdgid_parton_physics)==5 && refpt>120 && refpt<170 && TMath::Abs(refeta) < 0.7 && refpt/pthat < 2.5",
    "TMath::Abs(refpdgid_hadron)==5 && refpt>120 && refpt<170 && TMath::Abs(refeta) < 0.7 && refpt/pthat < 2.5",
    "TMath::Abs(refpdgid_parton_physics)==5 && TMath::Abs(refpdgid_hadron)==5 && refpt>120 && refpt<170 && TMath::Abs(refeta) < 0.7 && refpt/pthat < 2.5",
],
[
    "parton != 5, hadron = 5",
    "parton = 5, hadron != 5",
    "parton = 5",
    "hadron = 5",
    "parton = 5, hadron = 5",
],
"flavCorrPlots/response_pt120to170_eta0to0p7.pdf",
 "120 < p_{T} < 170 GeV, |#eta| < 0.7"
)
