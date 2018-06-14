///////////////////////////////////////////////////////////////////
//
// jet_draw_energyfractions_x
// ------------------------
// use hists from jet_correction_analyzer
//
///////////////////////////////////////////////////////////////////

#include "JetMETAnalysis/JetAnalyzers/interface/Settings.h"
#include "JetMETAnalysis/JetUtilities/interface/CommandLine.h"
#include "JetMETAnalysis/JetUtilities/interface/ObjectLoader.h"
#include "JetMETAnalysis/JetUtilities/interface/Variables.hh"
#include "JetMETAnalysis/JetUtilities/interface/Style.h"
#include "JetMETAnalysis/JetUtilities/interface/JetInfo.hh"

#include "TROOT.h"
#include "TSystem.h"
#include "TStyle.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TH1.h"
#include "TH1F.h"
#include "TH1D.h"
#include "TH2.h"
#include "TH2F.h"
#include "TF1.h"
#include "THStack.h"
#include "TString.h"
#include "TPaveText.h"
#include "TLegend.h"
#include "TDirectoryFile.h"
#include "TKey.h"
#include "TUUID.h"

#include <fstream>
#include <string>
#include <stdio.h>
#include <stdarg.h>
#include <numeric>

using namespace std;


vector<TString> getAlgsFromFile(TFile * ifile) {
  // Get a list of algo dirs from the file
  vector<TString> algs;
  TIter nextDir(ifile->GetListOfKeys());
  TKey* dirKey(0);
  while ((dirKey=(TKey*)nextDir())) {
    if (strcmp(dirKey->GetClassName(),"TDirectoryFile")!=0) continue;
    algs.push_back(dirKey->GetName());
  }
  return algs;
}


class ComparisonPlotMaker {
public:
  ComparisonPlotMaker(TString outputDir_, TString prefix_):
    nVars(0),
    nObjects(0),
    rebin(1),
    leg(nullptr),
    canv(nullptr),
    pave(nullptr),
    outputDir(outputDir_),
    prefix(prefix_),
    logY(false)
  {

  };

  void setVariableNames(vector<TString> varNames_) {
    varNames = varNames_;
    nVars = varNames.size();
  }

  void setVariableLabels(vector<TString> varLabels_) {
    varLabels = varLabels_;
    if (nVars != varLabels.size()) {
      throw runtime_error("Diff sizes");
    }
  }

  void setVariableColours(vector<int> varColours_) {
    varColours = varColours_;
  }

  void setVariableMarkers(vector<int> varMarkers_) {
    varMarkers = varMarkers_;
  }

  void setupObjectLoaders(TDirectoryFile * idir) {
    if (objLoaders.size() != nVars) {
      objLoaders.resize(nVars);
    }
    for (uint vInd=0; vInd<varNames.size(); vInd++) {
      objLoaders.at(vInd).reset();
      objLoaders.at(vInd).load_objects(idir, string(varNames[vInd]+"VsRefPt:JetEta")); // TODO: generalise
    }
    nObjects = objLoaders.at(0).nobjects();
  }

  void setRebin(int rebin_) {
    rebin = rebin_;
  }

  void setTitle(TString title_) {
    title = title_;
  }

  void setJetInfoStr(TString infoStr_) {
    jetInfoStr = infoStr_;
  }

  void setXtitle(TString title_) {
    xTitle = title_;
  }

  void setYtitle(TString title_) {
    yTitle = title_;
  }

  void setXrange(float minimum, float maximum) {
    xMin = minimum;
    xMax = maximum;
  }

  void setYrange(float minimum, float maximum) {
    yMin = minimum;
    yMax = maximum;
  }

  void setLogY(bool logY_) {
    logY = logY_;
  }

  void setOutputFmts(vector<TString> fmts) {
    ofmts = fmts;
  }

  void setupLegend(float x1, float y1, float x2, float y2, int nColumns=1) {
    leg = tdrLeg(x1, y1, x2, y2);
    leg->SetFillStyle(1001);
    leg->SetFillColorAlpha(kWhite, 0.75);
    leg->SetNColumns(nColumns);
  }

  void loopOverEtaBins(vector<int> binIndices={}) {
    if (binIndices.size() == 0) {
      // generate list of integers for indices if the user hasn't provided them
      binIndices.resize(nObjects);
      std::iota(binIndices.begin(), binIndices.end(), 0);
    }
    
    vector<TH2F*> hvars(nVars);

    for (uint objInd : binIndices) {
      double etaMin = objLoaders.at(0).minimum(0, objInd);
      double etaMax = objLoaders.at(0).maximum(0, objInd);
      cout << "Doing eta bin " << etaMin << " - " << etaMax << endl;
      TString etaBinStr = Form("%s%sto%s", objLoaders.at(0).variable(0).c_str(), eta_boundaries[objInd], eta_boundaries[objInd+1]);

      TString thisOutputDir = outputDir + etaBinStr;
      if(!gSystem->OpenDirectory(thisOutputDir)) gSystem->mkdir(thisOutputDir);
      // TDirectory* hdir = odir->mkdir("Histograms_JetEta");

      for (uint varInd=0; varInd<nVars; varInd++) {
        // Get the hist for each variable
        hvars.at(varInd) = objLoaders.at(varInd).object(objInd);
        cout << hvars.at(varInd)->GetName() << endl;
      }


      // loop over each ptbin, do 1D projection for each variable, create stacked plot
      for(int ibin=1; ibin<=hvars.at(0)->GetNbinsX(); ibin++) {

        vector<TH1D*> hContributions(nVars);

        TString ptBinStr = Form("RefPt%sto%s", Pt[ibin-1], Pt[ibin]);
        TString stackName = Form("%s_%s", etaBinStr.Data(), ptBinStr.Data());
        TH2F * hvar(nullptr);

        leg->Clear();
        
        // get projection, style, add to legend
        // float ymin(999);
        float ymax(0);
        
        for (uint varInd=0; varInd<nVars; varInd++) {
          hvar = hvars.at(varInd);
          TString name = Form("%s_%s", hvar->GetName(), ptBinStr.Data());
          hContributions.at(varInd) = hvar->ProjectionY(name, ibin, ibin, "e");
          TH1D * thisHist = hContributions.at(varInd);
          // thisHist->Sumw2();
          if (rebin > 1) thisHist->Rebin(rebin);
          thisHist->SetLineColor(varColours.at(varInd));
          thisHist->SetMarkerColor(varColours.at(varInd));
          thisHist->SetMarkerStyle(varMarkers.at(varInd));
          thisHist->Scale(1./thisHist->Integral());

          leg->AddEntry(thisHist, varLabels.at(varInd), "LP");

          // float thisYmin = thisHist->GetMinimum(0);
          // if (thisYmin < ymin) ymin = thisYmin;
          float thisYmax = thisHist->GetMaximum();
          if (thisYmax > ymax) ymax = thisYmax;

        }

        if (ymax == 0) continue;
        // Do drawing to canvas
        // Don't use a THstack - it doesn't play well with the frame
        frame = new TH1D();

        frame->GetXaxis()->SetTitle(xTitle);
        frame->GetXaxis()->SetLimits(xMin, xMax); // DO NOT USE SET RANGE USER!!!

        // frame->GetYaxis()->SetMoreLogLabels();
        frame->GetYaxis()->SetNoExponent();
        frame->GetYaxis()->SetTitle(yTitle);
        frame->GetYaxis()->SetRangeUser(yMin, yMax);

        canv = tdrCanvas(stackName, frame, 14, 11, true);
        for (auto & hItr : hContributions) {
          hItr->Draw("HISTE SAME");
        }
        if (logY) canv->SetLogy();

        pave = tdrText(0.5, 0.7, 0.93, 1-gPad->GetTopMargin()-0.045*(1-gPad->GetTopMargin()-gPad->GetBottomMargin()), 31);
        pave->AddText(title);
        pave->AddText(jetInfoStr);
        TString etaBinText = Form("%s < |#eta| < %s", eta_boundaries[objInd], eta_boundaries[objInd+1]);
        pave->AddText(etaBinText);
        TString ptBinText = Form("%s < p_{T}^{Ref} < %s GeV", Pt[ibin-1], Pt[ibin]);
        pave->AddText(ptBinText);

        pave->Draw("same");
        leg->Draw("same");

        for(auto & fmt : ofmts) {
          TString outputPlotname = Form(thisOutputDir + "/"+prefix+stackName+fmt);
          canv->SaveAs(outputPlotname);
        }

        delete pave;
        delete frame;
        delete canv;
      } // end loop over pt bins
    } // end loop over eta bins

  }


private:
  vector<TString> varNames, varLabels, ofmts;
  uint nVars;
  vector<int> varColours;
  vector<int> varMarkers;
  vector<ObjectLoader<TH2F>> objLoaders;
  int nObjects, rebin;
  TLegend * leg;
  TCanvas * canv;
  TPaveText * pave;
  TH1D * frame;
  TString title, xTitle, yTitle, outputDir, prefix, jetInfoStr;
  float xMin, xMax, yMin, yMax;
  bool logY;
};


//______________________________________________________________________________
int main(int argc,char**argv)
{
  gROOT->SetStyle("Plain");
  gStyle->SetOptStat(0);

  gSystem->Load("libFWCoreFWLite.so");

  //
  // evaluate command-line / configuration file options
  //
  CommandLine cl;
  if (!cl.parse(argc,argv)) return 0;

  TString filename               = cl.getValue<TString>  ("filename");
  vector<TString> algs           = cl.getVector<TString> ("algs",            "");
  TString title                  = cl.getValue<TString>  ("title",           "");
  TString outputDir              = cl.getValue<TString>  ("outputDir",       "./");
  TString outputFilename         = cl.getValue<TString>  ("outputFilename",  "EFPlots");
  vector<TString> outputFormat   = cl.getVector<TString> ("outputFormat",    ".pdf");

  if (!cl.check()) return 1;
  cl.print();

  vector<TString> efVarNames = {"Jtchf", "Jtnhf", "Jtcef", "Jtnef", "Jtmuf", "Jthfhf", "Jthfef"};
  vector<TString> efVarLabels = {"CHF", "NHF", "CEF", "NEF", "MUF", "HFHF", "HFEF"};
  vector<int> efVarColours = {kBlack, kRed, kBlue, kGreen+2, kOrange-3, kMagenta, kAzure+9};
  vector<int> efVarMarkers = {20, 21, 22, 23, 29, 33, 34};

  vector<TString> multVarNames = {"Jtchmult", "Jtnmult"};
  vector<TString> multVarLabels = {"CH MULT", "N MULT"};
  vector<int> multVarColours = {kBlack, kRed};
  vector<int> multVarMarkers = {20, 21};

  TFile *inf = new TFile(filename, "READ");

  //
  // Open/create the output directory and file
  //
  if(!outputDir.EndsWith("/")) outputDir+="/";
  if(!gSystem->OpenDirectory(outputDir)) gSystem->mkdir(outputDir);
  TString ofname = Form("%s/EFPlots.root",outputDir.Data());
  if(!outputFilename.IsNull()) ofname = Form("%s/%s",outputDir.Data(),outputFilename.Data());
  TFile *ofile = TFile::Open(ofname, "RECREATE");

  //
  // Loop over algorithms
  //
  if (algs.size() == 0) {
    algs = getAlgsFromFile(inf);
  }
  if (algs.size() == 0) {
    cout << "0 algorithms found in input file" << endl;
    exit(2);
  }

  ComparisonPlotMaker efPlotter(outputDir, "EF_");
  efPlotter.setVariableNames(efVarNames);
  efPlotter.setVariableLabels(efVarLabels);
  efPlotter.setVariableMarkers(efVarMarkers);
  efPlotter.setVariableColours(efVarColours);
  efPlotter.setRebin(5);
  efPlotter.setYrange(0.001, 10);
  efPlotter.setXrange(0, 1);
  efPlotter.setXtitle("Energy fraction");
  efPlotter.setYtitle("p.d.f.");
  efPlotter.setLogY(true);
  efPlotter.setTitle(title);
  efPlotter.setOutputFmts(outputFormat);
  efPlotter.setupLegend(0.6, 0.56, 0.9, 0.7, 2);

  ComparisonPlotMaker multPlotter(outputDir, "Mult_");
  multPlotter.setVariableNames(multVarNames);
  multPlotter.setVariableLabels(multVarLabels);
  multPlotter.setVariableMarkers(multVarMarkers);
  multPlotter.setVariableColours(multVarColours);
  multPlotter.setYrange(0, 0.5);
  multPlotter.setXrange(0, 50);
  multPlotter.setXtitle("Multiplicity");
  multPlotter.setYtitle("p.d.f.");
  // multPlotter.setLogY(true);
  multPlotter.setTitle(title);
  multPlotter.setOutputFmts(outputFormat);
  multPlotter.setupLegend(0.6, 0.56, 0.9, 0.7, 1);

  TDirectoryFile* odir(nullptr);

  for(const auto & alg : algs) {
    TDirectoryFile* idir = (TDirectoryFile*) inf->Get(alg);
    cout << alg << " ... " << endl;

    odir = (TDirectoryFile*)ofile->mkdir(alg.Data());
    odir->cd();

    efPlotter.setJetInfoStr(JetInfo::get_legend_title(string(alg)).c_str());
    efPlotter.setupObjectLoaders(idir);
    // efPlotter.loopOverEtaBins({0, 11, 12, 13, 14, 15});
    // efPlotter.loopOverEtaBins({18, 29, 30, 31, 32, 33});
    efPlotter.loopOverEtaBins();

    multPlotter.setJetInfoStr(JetInfo::get_legend_title(string(alg)).c_str());
    multPlotter.setupObjectLoaders(idir);
    // multPlotter.loopOverEtaBins({0, 11, 12, 13, 14, 15});
    // multPlotter.loopOverEtaBins({18, 29, 30, 31, 32, 33});
    multPlotter.loopOverEtaBins();
    
  }
  ofile->Close();
  inf->Close();
}
