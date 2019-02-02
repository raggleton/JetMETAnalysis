///////////////////////////////////////////////////////////////////
//
// jet_bhadron_plots_x.cc
// -------------------------
//
//            Make ROOT file with plots to debug B jet oddity
///////////////////////////////////////////////////////////////////

#include "JetMETAnalysis/JetAnalyzers/interface/VectorWrapper.h"
#include "JetMETAnalysis/JetAnalyzers/interface/VectorWrapper2D.h"
#include "JetMETAnalysis/JetUtilities/interface/TProfileMDF.h"
#include "JetMETAnalysis/JetUtilities/interface/CommandLine.h"
#include "JetMETAnalysis/JetUtilities/interface/JetInfo.hh"
#include "JetMETAnalysis/JetUtilities/interface/JRAEvent.h"
#include "JetMETAnalysis/JetUtilities/interface/ProgressBar.hh"

#include "DataFormats/Math/interface/deltaR.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"
#if __has_include("xrootd/XrdCl/XrdClFileSystem.hh")
#include "xrootd/XrdCl/XrdClFileSystem.hh"
#define has_xrdcl 1
#else
#define has_xrdcl 0
#endif

#include "TROOT.h"
#include "TSystem.h"
#include "TEnv.h"
#include <TObjectTable.h>
#include "TFile.h"
#include "TFileCollection.h"
#include "TTree.h"
#include "TChain.h"
#include "TH1.h"
#include "TH1F.h"
#include "TH1D.h"
#include "TH2.h"
#include "TH2F.h"
#include "TH3D.h"
#include "TF1.h"
#include "TString.h"
#include "TMath.h"
#include "TFitResult.h"
#include "TProfile.h"
#include "TProfile2D.h"
#include "TProfile3D.h"
#include "TBenchmark.h"
#include "TEventList.h"

#include <iostream>
#include <string>
#include <vector>
#include <stdio.h>
#include <stdarg.h>
#include <cstring>
#include <limits.h>

using namespace std;

////////////////////////////////////////////////////////////////////////////////
// define local functions
////////////////////////////////////////////////////////////////////////////////

/// get the bin number for a specific ptgen according to the vector of bin edges
int getBin(double x, const double boundaries[], int length);

/// get the flavor name used in initializing the JetCorrectorParameters
string get_flavor_name(int pdgid);

/// returns the postfix associated with a specific level and algorithm
string getPostfix(vector<string> postfix, string alg, int level);

// for sorting TLorentzVectors by pt
bool sort_by_pt(const TLorentzVector & a, const TLorentzVector & b);

// for division when b could be 0, in which case return infinity
float safe_divide(float a, float b);


enum class FlavDef {
   Physics,
   Algo,
   Hadron,
   HadronParton
};

////////////////////////////////////////////////////////////////////////////////
// main
////////////////////////////////////////////////////////////////////////////////

//______________________________________________________________________________
int main(int argc,char**argv)
{
   gROOT->ProcessLine("#include<vector>");
   gSystem->Load("libFWCoreFWLite.so");
   gEnv->SetValue("TFile.AsyncPrefetching", 1);

   //
   // evaluate command-line / configuration file options
   //
   CommandLine cl;
   if (!cl.parse(argc,argv)) return 10;

   vector<string>  algs              = cl.getVector<string>      ("algs");
   string          path              = cl.getValue<string>       ("path",                 "");
   string          era               = cl.getValue<string>       ("era",                  "");
   string          inputFilename     = cl.getValue<string>       ("inputFilename");
   string          inputFilePath     = cl.getValue<string>       ("inputFilePath",        "");
   string          fileList          = cl.getValue<string>       ("fileList",             "");
   string          url_string        = cl.getValue<string>       ("url_string",           "");
   TString         outputDir         = cl.getValue<TString>      ("outputDir",            "");
   TString         suffix            = cl.getValue<TString>      ("suffix",               "");
   vector<int>     levels            = cl.getVector<int>         ("levels",               "");
   bool            useTags           = cl.getValue<bool>         ("useTags",            true);
   bool            L1FastJet         = cl.getValue<bool>         ("L1FastJet",          true);
   vector<string>  postfix           = cl.getVector<string>      ("postfix",              "");
   bool            doflavor          = cl.getValue<bool>         ("doflavor",          false);
   int             pdgid             = cl.getValue<int>          ("pdgid",                 0);
   TString         flavorDefinition  = cl.getValue<TString>      ("flavorDefinition", "physics");
   bool            useweight         = cl.getValue<bool>         ("useweight",         false);
   float           pThatReweight     = cl.getValue<float>        ("pThatReweight",     -9999);
   float           relpthatmax       = cl.getValue<float>        ("relpthatmax",                10);
   float           xsection          = cl.getValue<float>        ("xsection",            0.0);
   float           luminosity        = cl.getValue<float>        ("luminosity",          1.0);
   vector<string>  presel            = cl.getVector<string>      ("presel",                     "");
   vector<double>  drmax             = cl.getVector<double>      ("drmax",                "");
   double          ptmin             = cl.getValue<double>       ("ptmin",                 0);
   double          ptgenmin          = cl.getValue<double>       ("ptgenmin",              0);
   double          ptgenmax          = cl.getValue<double>       ("ptgenmax",          99999);
   double          ptrawmin          = cl.getValue<double>       ("ptrawmin",              0);
   float           pthatmin          = cl.getValue<float>        ("pthatmin",            0.0);
   float           pthatmax          = cl.getValue<float>        ("pthatmax",           -1.0);
   double          etamax            = cl.getValue<double>       ("etamax",                0);
   double          dphimin           = cl.getValue<double>       ("dphimin",               0);
   unsigned int    nrefmax           = cl.getValue<unsigned int> ("nrefmax",               0);
   int             nbinsrelrsp       = cl.getValue<int>          ("nbinsrelrsp",         200);
   float           relrspmin         = cl.getValue<float>        ("relrspmin",           0.0);
   float           relrspmax         = cl.getValue<float>        ("relrspmax",           2.0);
   unsigned int    evtmax            = cl.getValue<unsigned int> ("evtmax",                0);
   TString         weightfilename    = cl.getValue<TString>      ("weightfilename",       "");
   TString         MCPUReWeighting   = cl.getValue<TString>      ("MCPUReWeighting",      "");
   TString         DataPUReWeighting = cl.getValue<TString>      ("DataPUReWeighting",    "");
   TString         readRespVsPileup  = cl.getValue<TString>      ("readRespVsPileup",     "");
   bool            verbose           = cl.getValue<bool>         ("verbose",           false);
   bool            debug             = cl.getValue<bool>         ("debug",             false);

   if (!cl.check()) return 100;
   cl.print();

   TBenchmark* m_benchmark = new TBenchmark();
   m_benchmark->Reset();
   m_benchmark->Start("event");

   //
   // Do some additional check
   //

   // Check that if pThatReweight is set then useweight is also set
   if(pThatReweight!=-9999 && useweight==false) {
      cout << "ERROR::jet_correction_analyzer_x Can't reweight the pThat spectrum without first using the existing"
           << " weights to return to an unmodified spectrum. Set the \"useweight\" option to true." << endl;
           return -1;
   }

   // Check that the size of the drmax values matches that of the algs
   if(drmax.size()>0 && algs.size()!=drmax.size()) {
      cout << "ERROR::jet_correction_analyzer_x The size of the drmax vector must match the size of the algs vector" << endl;
      return 101;
   }

   FlavDef flavorDef = FlavDef::Physics;

   flavorDefinition.ToUpper();
   if (flavorDefinition.CompareTo("PHYSICS")==0)
      flavorDef = FlavDef::Physics;
   else if (flavorDefinition.CompareTo("ALGO")==0)
      flavorDef = FlavDef::Algo;
   else if (flavorDefinition.CompareTo("HADRON")==0)
      flavorDef = FlavDef::Hadron;
   else if (flavorDefinition.CompareTo("HADRONPARTON")==0)
      flavorDef = FlavDef::HadronParton;
   else
      throw std::runtime_error("Unknown flavorDefinition: must be PHYSICS, ALGO, HADRON, or HADRONPARTON");

   //
   // Some useful quantities
   //
   double vresp[nbinsrelrsp+1];
   double vcorr[nbinsrelrsp+1];
   for(int i=0; i<=nbinsrelrsp; i++) {
      vresp[i] = (i*((relrspmax-relrspmin)/(double)nbinsrelrsp));
      vcorr[i] = (i*((CorrHigh-CorrLow)/(double)nbinsrelrsp));
   }

   edm::LumiReWeighting LumiWeights_;
   if(!MCPUReWeighting.IsNull() && !DataPUReWeighting.IsNull()) {
      LumiWeights_ = edm::LumiReWeighting(string(MCPUReWeighting),string(DataPUReWeighting),"pileup","pileup");
   }

   if(!outputDir.IsNull() && !outputDir.EndsWith("/")) outputDir += "/";
   TFile *outf = TFile::Open(outputDir+"BHadron_"+JetInfo::ListToString(algs,string("_"))+suffix+".root","RECREATE");


   //
   // Define our own binnings
   //
   const int NPtBins = 4;
   const char Pt[NPtBins+1][10] = {"57", "90", "600", "750", "1000"};
   const double vpt[NPtBins+1] = {57, 90, 600, 750, 1000};

   const int NETA = 1;
   const char eta_boundaries[NETA+1][10] = {"0", "0.783"};
   const double veta[NETA+1] = {0, 0.783};

   //
   // Loop over the algorithms
   //
   for(unsigned int a=0; a<algs.size(); a++) {
      TFile *weightFile(nullptr);
      TH2D *weightHist(nullptr);
      if(!weightfilename.IsNull()) {
         weightFile = TFile::Open(weightfilename,"READ");
         if (!weightFile->IsOpen()) { cout<<"Can't open "<<weightfilename<<endl; }
         cout << "Getting the weight histogram all_ ... " << flush;
         weightHist = (TH2D*)weightFile->Get((algs[a]+"/all_").c_str());
         if(weightHist==nullptr) { cout<<"FAIL!"<<endl<<"Histogram of weights named \"all_\" was not in file "<<weightfilename<<endl; return 102; }
         cout << "DONE" << endl;
      }

      JetInfo jetInfo(TString(algs[a]));

      //
      // setup the tree for reading
      //
      int file_count(0);
      TChain* chain;
      if(!inputFilename.empty() && inputFilePath.empty()) {
         TFile *inf = TFile::Open(inputFilename.c_str());
         TDirectoryFile *idir = (TDirectoryFile*)inf->Get(algs[a].c_str());
         if (idir)
            cout << "The directory is " << idir->GetName() << endl;
         else {
            cout << "ERROR::Directory " << algs[a] <<" could not be found in file " << inf->GetName() << endl;
            cout << " SKIPPING ALGO " << algs[a] << endl;
            continue;
         }
         chain = (TChain*)idir->Get("t");
         file_count = 1;
      }
      else if(!fileList.empty()) {
         cout<<"\tAdding files from the list " << inputFilePath << "/" << fileList<<endl;
         chain = new TChain((algs[a]+"/t").c_str());
         TFileCollection fc("fc","",(inputFilePath+"/"+fileList).c_str());
         chain->AddFileInfoList((TCollection*)fc.GetList());
         if(chain->GetListOfFiles()->GetEntries()!=fc.GetNFiles()) {
            cout << "ERROR::DelphesNtupleToJRANtuple_x::main Something went wrong and the number of files in the filesList doesn't equal the number of files in the chain." << endl;
            return -1;
         }
         file_count = chain->GetListOfFiles()->GetEntries();
      }
      #if(has_xrdcl)
         else if(!url_string.empty()) {
            chain = new TChain((algs[a]+"/t").c_str());
            XrdCl::DirectoryList *response;
            XrdCl::DirListFlags::Flags flags = XrdCl::DirListFlags::None;
            XrdCl::URL url(url_string);
            XrdCl::FileSystem fs(url);
            fs.DirList(inputFilePath,flags,response);
            for(auto iresp=response->Begin(); iresp!=response->End(); iresp++) {
               if((*iresp)->GetName().find(".root")!=std::string::npos) {
                  cout << "\tAdding " << url_string << inputFilePath << (*iresp)->GetName() << endl;
                  file_count = chain->Add((url_string+inputFilePath+(*iresp)->GetName()).c_str());
               }
            }
         }
      #endif
      else {
         cout<<"\tAdding "<<inputFilePath+"/"+inputFilename+"*.root"<<endl;
         chain = new TChain((algs[a]+"/t").c_str());
         file_count = chain->Add((inputFilePath+"/"+inputFilename+"*.root").c_str());
      }
      if (file_count==0){
         cout << "\tNo files found!  Aborting.\n";
         return 103;
      }
      if (0==chain) { cout<<"no tree/chain found."<<endl; continue; }
      bool useCandidates_ = false;
      bool isPFJet_ = true;
      bool isCaloJet_ = false;
      bool doComposition_ = true;
      bool doBalancing_ = false;
      bool doFlavor_ = true;
      bool doHLT_ = false;
      int flag_int = (useCandidates_*pow(2,7)) + (isPFJet_*pow(2,6)) +
                   (isCaloJet_*pow(2,5)) + (doComposition_*pow(2,4)) +
                   (doBalancing_*pow(2,3)) + (doFlavor_*pow(2,2)) +
                   (doHLT_*pow(2,1)) + (1);
      bitset<8> flags(flag_int);
      JRAEvent* JRAEvt = new JRAEvent(chain,flags);
      chain->SetBranchStatus("*",0);
      vector<string> branch_names = {"nref","refpt","refeta","refphi",
                                     "jtpt","jteta","jtphi","jtarea", "jte",
                                     "bxns","npus","tnpus","sumpt_lowpt","refdrjt",
                                     "jtchf", "jtnhf", "jtnef", "jtcef", "jtmuf", "jthfhf", "jthfef",
                                     "jtchmult", "jtnmult",
                                     "refpdgid_parton_physics", "refpdgid_parton_algo", "refpdgid_hadron",
                                     "ref_hadron_pt", "ref_hadron_eta", "ref_hadron_phi", "ref_hadron_pdgid",
                                     "ref_hadron_vx", "ref_hadron_vy", "ref_hadron_vz",
                                     "ref_hadron_ndecay", "ref_hadron_sldecay", "ref_nhadron",
                                     "ref_hadron_decay_pt", "ref_hadron_decay_eta", "ref_hadron_decay_phi", "ref_hadron_decay_pdgid",
                                     "refchf", "refnhf", "refnef", "refcef", "refmuf", "refchmult", "refnmult",
                                     "npv","rho","rho_hlt","pthat","weight"};
      if (useCandidates_) {
         vector<string> pf_branch_names = {"pfcand_pt", "pfcand_eta", "pfcand_phi", "pfcand_id", "pfcand_e"};
         branch_names.insert(branch_names.end(), pf_branch_names.begin(), pf_branch_names.end());
      }
      for(auto n : branch_names) {
         if(n=="rho_hlt" && 0==chain->GetBranch("rho_hlt")) continue;
         if(n=="weight") {
            if (xsection>0.0) {
                useweight = false;
            }
            if (useweight) {
                if (0==chain->GetBranch(n.c_str()))
                    cout<<"branch 'weight' not found, events will NOT be weighted!"<<endl;
                else
                    chain->SetBranchStatus(n.c_str(),1);
            }
            continue;
         }
         chain->SetBranchStatus(n.c_str(),1);
      }

      //
      // move to the output directory
      //
      TDirectoryFile* odir = (TDirectoryFile*)outf->mkdir(algs[a].c_str());
      odir->cd();

      int j,k;
      char name[1024];

      TH1F *pThatDistribution(nullptr);
      vector<TH2F*> RelRspVsRefPt;
      TH2F *RelRspVsJetEta[NPtBins];
      vector<TH2F*> JtchfVsRefPt;
      vector<TH2F*> JtnhfVsRefPt;
      vector<TH2F*> JtnefVsRefPt;
      vector<TH2F*> JtcefVsRefPt;
      vector<TH2F*> JtmufVsRefPt;
      vector<TH2F*> JtchmultVsRefPt;
      vector<TH2F*> JtnmultVsRefPt;

      vector<TH2F*> RefchfVsRefPt;
      vector<TH2F*> RefnhfVsRefPt;
      vector<TH2F*> RefnefVsRefPt;
      vector<TH2F*> RefcefVsRefPt;
      vector<TH2F*> RefmufVsRefPt;
      vector<TH2F*> RefchmultVsRefPt;
      vector<TH2F*> RefnmultVsRefPt;

      vector<TH2F*> RelRspVsJtchf;
      vector<TH2F*> RelRspVsJtnhf;
      vector<TH2F*> RelRspVsJtnef;
      vector<TH2F*> RelRspVsJtcef;
      vector<TH2F*> RelRspVsJtmuf;
      vector<TH2F*> RelRspVsJtchmult;
      vector<TH2F*> RelRspVsJtnmult;

      vector<TH2F*> RelRspVsRefchf;
      vector<TH2F*> RelRspVsRefnhf;
      vector<TH2F*> RelRspVsRefnef;
      vector<TH2F*> RelRspVsRefcef;
      vector<TH2F*> RelRspVsRefmuf;
      vector<TH2F*> RelRspVsRefchmult;
      vector<TH2F*> RelRspVsRefnmult;

      vector<TH2F*> JtchfVsRefchf;
      vector<TH2F*> JtnhfVsRefnhf;
      vector<TH2F*> JtnefVsRefnef;
      vector<TH2F*> JtcefVsRefcef;
      vector<TH2F*> JtmufVsRefmuf;
      vector<TH2F*> JtchmultVsRefchmult;
      vector<TH2F*> JtnmultVsRefnmult;

      vector<TH2F*> JtchfVsRefchf_LowRsp;
      vector<TH2F*> JtnhfVsRefnhf_LowRsp;
      vector<TH2F*> JtnefVsRefnef_LowRsp;
      vector<TH2F*> JtcefVsRefcef_LowRsp;
      vector<TH2F*> JtmufVsRefmuf_LowRsp;
      vector<TH2F*> JtchmultVsRefchmult_LowRsp;
      vector<TH2F*> JtnmultVsRefnmult_LowRsp;

      vector<TH2F*> JtchfVsRefchf_HighRsp;
      vector<TH2F*> JtnhfVsRefnhf_HighRsp;
      vector<TH2F*> JtnefVsRefnef_HighRsp;
      vector<TH2F*> JtcefVsRefcef_HighRsp;
      vector<TH2F*> JtmufVsRefmuf_HighRsp;
      vector<TH2F*> JtchmultVsRefchmult_HighRsp;
      vector<TH2F*> JtnmultVsRefnmult_HighRsp;

      vector<TH2F*> RelRspVsJtchfRefchfRatio;
      vector<TH2F*> RelRspVsJtnhfRefnhfRatio;
      vector<TH2F*> RelRspVsJtnefRefnefRatio;
      vector<TH2F*> RelRspVsJtcefRefcefRatio;
      vector<TH2F*> RelRspVsJtmufRefmufRatio;
      vector<TH2F*> RelRspVsJtchmultRefchmultRatio;
      vector<TH2F*> RelRspVsJtnmultRefnmultRatio;

      vector<TH2F*> NHadronsVsRefPt;

      vector<TH2F*> RelRspVsJtArea;

      // if only 1 hadron
      vector<TH2F*> RelRspVsRefPt_SingleHadron;
      vector<TH2F*> RelRspVsRefPt_SingleHadron_SLDecay;
      vector<TH2F*> RelRspVsRefPt_SingleHadron_HadDecay;
      vector<TH2F*> RelRspVsBJetRefInd_SingleHadron;
      vector<TH2F*> BJetRefIndVsRefPt_SingleHadron;
      vector<TH2F*> RefHadronPtRatioVsRefPt_SingleHadron;
      vector<TH2F*> RefHadronPtRatioVsDeltaRRef_SingleHadron;
      vector<TH2F*> RelRspVsRefHadronPtRatio_SingleHadron;
      vector<TH2F*> RelRspVsRefHadronDeltaRRef_SingleHadron;
      vector<TH2F*> RelRspVsRefHadronPdgid_SingleHadron;
      vector<TH2F*> RefHadronPdgidVsRefPt_SingleHadron;
      vector<TH2F*> RefHadronNdecayVsRefPt_SingleHadron;
      vector<TH2F*> RefHadronSldecayVsRefPt_SingleHadron; //semileptonic decay
      vector<TH2F*> RefHadronDecayPtRatioVsRefPt_SingleHadron;
      vector<TH2F*> RefHadronDecayPtRatioJetVsRefPt_SingleHadron;
      vector<TH2F*> RefHadronDecayPdgidVsRefPt_SingleHadron;
      vector<TH2F*> RefHadronDecayPtRatioVsRefPt_SingleHadron_Lepton;
      vector<TH2F*> RefHadronDecayPtRatioJetVsRefPt_SingleHadron_Lepton;
      vector<TH2F*> RefHadronDecayPdgidVsRefPt_SingleHadron_Lepton;
      vector<TH2F*> RefHadronDecayPtRatioVsRefPt_SingleHadron_Neutrino;
      vector<TH2F*> RefHadronDecayPtRatioJetVsRefPt_SingleHadron_Neutrino;
      vector<TH2F*> RefHadronDecayPdgidVsRefPt_SingleHadron_Neutrino;
      vector<TH2F*> RelRspVsRefHadronDecayPtRatioJet_SingleHadron_Lepton;
      vector<TH2F*> RelRspVsRefHadronDecayPtRatioJet_SingleHadron_Neutrino;
      vector<TH2F*> RelRspVsRefHadronNDecay_SingleHadron;
      vector<TH2F*> RelRspVsRefHadronVx_SingleHadron;
      vector<TH2F*> RelRspVsRefHadronVy_SingleHadron;
      vector<TH2F*> RelRspVsRefHadronVz_SingleHadron;

      // if 2+ hadrons
      vector<TH2F*> RelRspVsRefPt_AtLeast2Hadron;
      vector<TH2F*> RelRspVsRefPt_AtLeast2Hadron_SLDecay;
      vector<TH2F*> RelRspVsRefPt_AtLeast2Hadron_HadDecay;
      vector<TH2F*> BJetRefIndVsRefPt_AtLeast2Hadron;
      vector<TH2F*> RefHadronPtRatioVsRefPt_FirstHadron;
      vector<TH2F*> RefHadronPtRatioVsDeltaRRef_FirstHadron;
      vector<TH2F*> RelRspVsRefHadronPtRatio_FirstHadron;
      vector<TH2F*> RelRspVsRefHadronDeltaRRef_FirstHadron;
      vector<TH2F*> RefHadronPdgidVsRefPt_FirstHadron;
      vector<TH2F*> RefHadronNdecayVsRefPt_FirstHadron;
      vector<TH2F*> RefHadronSldecayVsRefPt_FirstHadron;
      vector<TH2F*> RefHadronDecayPtRatioVsRefPt_FirstHadron;
      vector<TH2F*> RefHadronDecayPdgidVsRefPt_FirstHadron;
      vector<TH2F*> RefHadronDecayPtRatioVsRefPt_FirstHadron_Lepton;
      vector<TH2F*> RefHadronDecayPdgidVsRefPt_FirstHadron_Lepton;
      vector<TH2F*> RefHadronDecayPtRatioVsRefPt_FirstHadron_Neutrino;
      vector<TH2F*> RefHadronDecayPdgidVsRefPt_FirstHadron_Neutrino;

      vector<TH2F*> RefHadronPtRatioVsRefPt_SecondHadron;
      vector<TH2F*> RefHadronPtRatioVsDeltaRRef_SecondHadron;
      vector<TH2F*> RelRspVsRefHadronPtRatio_SecondHadron;
      vector<TH2F*> RelRspVsRefHadronDeltaRRef_SecondHadron;
      vector<TH2F*> RefHadronPdgidVsRefPt_SecondHadron;
      vector<TH2F*> RefHadronNdecayVsRefPt_SecondHadron;
      vector<TH2F*> RefHadronSldecayVsRefPt_SecondHadron;
      vector<TH2F*> RefHadronDecayPtRatioVsRefPt_SecondHadron;
      vector<TH2F*> RefHadronDecayPdgidVsRefPt_SecondHadron;
      vector<TH2F*> RefHadronDecayPtRatioVsRefPt_SecondHadron_Lepton;
      vector<TH2F*> RefHadronDecayPdgidVsRefPt_SecondHadron_Lepton;
      vector<TH2F*> RefHadronDecayPtRatioVsRefPt_SecondHadron_Neutrino;
      vector<TH2F*> RefHadronDecayPdgidVsRefPt_SecondHadron_Neutrino;

      TH3F *RespVsEtaVsPt(nullptr);
      TH3F *ScaleVsEtaVsPt(nullptr);

      //
      // Get the corrections from the text files
      //
      bool exclude(false);
      for (unsigned int i=0;i<levels.size();i++) {
         stringstream sslvl; sslvl<<"l"<<levels[i];
         if (algs[a].find(sslvl.str())!=string::npos) exclude=true;
      }
      if (exclude) {
         cout<<"exclude "<<algs[a]<<endl;
         continue;
      }
      string algName = algs[a];
      if (!doflavor) {
         auto loc = algName.find("l");
         if (loc != string::npos) {
            algName = algName.substr(0, loc);
            cout << "algName: " << algName << endl;
         } else {
            cout << "Couldn't find l" << endl;
         }
         for(unsigned int ilevel=0; ilevel<levels.size(); ilevel++) {
            cout << getPostfix(postfix,algName,levels[ilevel]) << endl;
         }
      }

      cout<<"jet algorithm: "<<algs[a]<<endl;
      cout<<"correction level: "<<JetInfo::get_correction_levels(levels,L1FastJet)<<endl;
      cout<<"correction tag: "<<JetInfo::get_correction_tags(era,algName,levels,path,L1FastJet)<<endl;

      cout << "Setting up the FactorizedJetCorrector ... " << flush;
      FactorizedJetCorrector *JetCorrector;
      if(levels.size()>0 && useTags) {
         JetCorrector = new FactorizedJetCorrector(JetInfo::get_correction_levels(levels,L1FastJet),
                                                   JetInfo::get_correction_tags(era,algName,levels,path,L1FastJet));
      }
      else if(levels.size()>0) {
         //
         // Make sure the levels are in the correct order (lowest level to highest)
         //
         sort (levels.begin(),levels.end());
         vector<JetCorrectorParameters> vPar;
         for(unsigned int ilevel=0; ilevel<levels.size(); ilevel++) {
            cout << "Looking for JEC file " << string(path + era + JetInfo::get_level_tag(levels[ilevel],L1FastJet) +
                                                      jetInfo.getAlias() + getPostfix(postfix,algName,levels[ilevel]) + ".txt") << endl;
            vPar.push_back(JetCorrectorParameters(string(path + era + JetInfo::get_level_tag(levels[ilevel],L1FastJet) +
                                                         jetInfo.getAlias() + getPostfix(postfix,algName,levels[ilevel]) + ".txt")));
         }
         JetCorrector = new FactorizedJetCorrector(vPar);
      }
      else {
         JetCorrector = nullptr;
      }
      cout << "DONE" << endl;

      //
      // book histograms
      //
      pThatDistribution = new TH1F("pThat","pThat",(int)vpt[NPtBins]/10.0,vpt[0],vpt[NPtBins]);
      pThatDistribution->Sumw2();
      for(int ieta=0; ieta<NETA; ieta++) {
         TString hname = Form("RelRspVsRefPt_JetEta%sto%s",eta_boundaries[ieta],eta_boundaries[ieta+1]);
         RelRspVsRefPt.push_back(new TH2F(hname,hname,NPtBins,vpt,nbinsrelrsp,relrspmin,relrspmax));
         RelRspVsRefPt.back()->Sumw2();

         int NEfBins = 100;
         hname = Form("JtchfVsRefPt_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtchfVsRefPt.push_back(new TH2F(hname, hname, NPtBins, vpt, NEfBins, 0, 1));
         JtchfVsRefPt.back()->Sumw2();

         hname = Form("JtnhfVsRefPt_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtnhfVsRefPt.push_back(new TH2F(hname, hname, NPtBins, vpt, NEfBins, 0, 1));
         JtnhfVsRefPt.back()->Sumw2();

         hname = Form("JtnefVsRefPt_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtnefVsRefPt.push_back(new TH2F(hname, hname, NPtBins, vpt, NEfBins, 0, 1));
         JtnefVsRefPt.back()->Sumw2();

         hname = Form("JtcefVsRefPt_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtcefVsRefPt.push_back(new TH2F(hname, hname, NPtBins, vpt, NEfBins, 0, 1));
         JtcefVsRefPt.back()->Sumw2();

         hname = Form("JtmufVsRefPt_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtmufVsRefPt.push_back(new TH2F(hname, hname, NPtBins, vpt, NEfBins, 0, 1));
         JtmufVsRefPt.back()->Sumw2();

         int NMultBins = 100;
         hname = Form("JtchmultVsRefPt_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtchmultVsRefPt.push_back(new TH2F(hname, hname, NPtBins, vpt, NMultBins, 0, NMultBins));
         JtchmultVsRefPt.back()->Sumw2();

         hname = Form("JtnmultVsRefPt_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtnmultVsRefPt.push_back(new TH2F(hname, hname, NPtBins, vpt, NMultBins, 0, NMultBins));
         JtnmultVsRefPt.back()->Sumw2();

         hname = Form("RefchfVsRefPt_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefchfVsRefPt.push_back(new TH2F(hname, hname, NPtBins, vpt, NEfBins, 0, 1));
         RefchfVsRefPt.back()->Sumw2();

         hname = Form("RefnhfVsRefPt_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefnhfVsRefPt.push_back(new TH2F(hname, hname, NPtBins, vpt, NEfBins, 0, 1));
         RefnhfVsRefPt.back()->Sumw2();

         hname = Form("RefnefVsRefPt_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefnefVsRefPt.push_back(new TH2F(hname, hname, NPtBins, vpt, NEfBins, 0, 1));
         RefnefVsRefPt.back()->Sumw2();

         hname = Form("RefcefVsRefPt_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefcefVsRefPt.push_back(new TH2F(hname, hname, NPtBins, vpt, NEfBins, 0, 1));
         RefcefVsRefPt.back()->Sumw2();

         hname = Form("RefmufVsRefPt_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefmufVsRefPt.push_back(new TH2F(hname, hname, NPtBins, vpt, NEfBins, 0, 1));
         RefmufVsRefPt.back()->Sumw2();

         hname = Form("RefchmultVsRefPt_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefchmultVsRefPt.push_back(new TH2F(hname, hname, NPtBins, vpt, NMultBins, 0, NMultBins));
         RefchmultVsRefPt.back()->Sumw2();

         hname = Form("RefnmultVsRefPt_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefnmultVsRefPt.push_back(new TH2F(hname, hname, NPtBins, vpt, NMultBins, 0, NMultBins));
         RefnmultVsRefPt.back()->Sumw2();

         // Rsp vs Reco EF, mult
         hname = Form("RelRspVsJtchf_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsJtchf.push_back(new TH2F(hname, hname, NEfBins, 0, 1, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsJtchf.back()->Sumw2();

         hname = Form("RelRspVsJtnhf_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsJtnhf.push_back(new TH2F(hname, hname, NEfBins, 0, 1, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsJtnhf.back()->Sumw2();

         hname = Form("RelRspVsJtnef_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsJtnef.push_back(new TH2F(hname, hname, NEfBins, 0, 1, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsJtnef.back()->Sumw2();

         hname = Form("RelRspVsJtcef_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsJtcef.push_back(new TH2F(hname, hname, NEfBins, 0, 1, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsJtcef.back()->Sumw2();

         hname = Form("RelRspVsJtmuf_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsJtmuf.push_back(new TH2F(hname, hname, NEfBins, 0, 1, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsJtmuf.back()->Sumw2();

         hname = Form("RelRspVsJtchmult_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsJtchmult.push_back(new TH2F(hname, hname, NMultBins, 0, NMultBins, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsJtchmult.back()->Sumw2();

         hname = Form("RelRspVsJtnmult_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsJtnmult.push_back(new TH2F(hname, hname, NMultBins, 0, NMultBins, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsJtnmult.back()->Sumw2();

         // rsp vs gen EF, mult
         hname = Form("RelRspVsRefchf_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefchf.push_back(new TH2F(hname, hname, NEfBins, 0, 1, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsRefchf.back()->Sumw2();

         hname = Form("RelRspVsRefnhf_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefnhf.push_back(new TH2F(hname, hname, NEfBins, 0, 1, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsRefnhf.back()->Sumw2();

         hname = Form("RelRspVsRefnef_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefnef.push_back(new TH2F(hname, hname, NEfBins, 0, 1, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsRefnef.back()->Sumw2();

         hname = Form("RelRspVsRefcef_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefcef.push_back(new TH2F(hname, hname, NEfBins, 0, 1, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsRefcef.back()->Sumw2();

         hname = Form("RelRspVsRefmuf_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefmuf.push_back(new TH2F(hname, hname, NEfBins, 0, 1, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsRefmuf.back()->Sumw2();

         hname = Form("RelRspVsRefchmult_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefchmult.push_back(new TH2F(hname, hname, NMultBins, 0, NMultBins, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsRefchmult.back()->Sumw2();

         hname = Form("RelRspVsRefnmult_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefnmult.push_back(new TH2F(hname, hname, NMultBins, 0, NMultBins, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsRefnmult.back()->Sumw2();

         // reco vs gen EF, mult
         hname = Form("JtchfVsRefchf_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtchfVsRefchf.push_back(new TH2F(hname, hname, NEfBins, 0, 1, NEfBins, 0, 1));
         JtchfVsRefchf.back()->Sumw2();

         hname = Form("JtnhfVsRefnhf_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtnhfVsRefnhf.push_back(new TH2F(hname, hname, NEfBins, 0, 1, NEfBins, 0, 1));
         JtnhfVsRefnhf.back()->Sumw2();

         hname = Form("JtnefVsRefnef_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtnefVsRefnef.push_back(new TH2F(hname, hname, NEfBins, 0, 1, NEfBins, 0, 1));
         JtnefVsRefnef.back()->Sumw2();

         hname = Form("JtcefVsRefcef_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtcefVsRefcef.push_back(new TH2F(hname, hname, NEfBins, 0, 1, NEfBins, 0, 1));
         JtcefVsRefcef.back()->Sumw2();

         hname = Form("JtmufVsRefmuf_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtmufVsRefmuf.push_back(new TH2F(hname, hname, NEfBins, 0, 1, NEfBins, 0, 1));
         JtmufVsRefmuf.back()->Sumw2();

         hname = Form("JtchmultVsRefchmult_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtchmultVsRefchmult.push_back(new TH2F(hname, hname, NMultBins, 0, NMultBins, NMultBins, 0, NMultBins));
         JtchmultVsRefchmult.back()->Sumw2();

         hname = Form("JtnmultVsRefnmult_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtnmultVsRefnmult.push_back(new TH2F(hname, hname, NMultBins, 0, NMultBins, NMultBins, 0, NMultBins));
         JtnmultVsRefnmult.back()->Sumw2();

         // lower rsp only
         hname = Form("JtchfVsRefchf_LowRsp_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtchfVsRefchf_LowRsp.push_back(new TH2F(hname, hname, NEfBins, 0, 1, NEfBins, 0, 1));
         JtchfVsRefchf_LowRsp.back()->Sumw2();

         hname = Form("JtnhfVsRefnhf_LowRsp_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtnhfVsRefnhf_LowRsp.push_back(new TH2F(hname, hname, NEfBins, 0, 1, NEfBins, 0, 1));
         JtnhfVsRefnhf_LowRsp.back()->Sumw2();

         hname = Form("JtnefVsRefnef_LowRsp_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtnefVsRefnef_LowRsp.push_back(new TH2F(hname, hname, NEfBins, 0, 1, NEfBins, 0, 1));
         JtnefVsRefnef_LowRsp.back()->Sumw2();

         hname = Form("JtcefVsRefcef_LowRsp_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtcefVsRefcef_LowRsp.push_back(new TH2F(hname, hname, NEfBins, 0, 1, NEfBins, 0, 1));
         JtcefVsRefcef_LowRsp.back()->Sumw2();

         hname = Form("JtmufVsRefmuf_LowRsp_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtmufVsRefmuf_LowRsp.push_back(new TH2F(hname, hname, NEfBins, 0, 1, NEfBins, 0, 1));
         JtmufVsRefmuf_LowRsp.back()->Sumw2();

         hname = Form("JtchmultVsRefchmult_LowRsp_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtchmultVsRefchmult_LowRsp.push_back(new TH2F(hname, hname, NMultBins, 0, NMultBins, NMultBins, 0, NMultBins));
         JtchmultVsRefchmult_LowRsp.back()->Sumw2();

         hname = Form("JtnmultVsRefnmult_LowRsp_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtnmultVsRefnmult_LowRsp.push_back(new TH2F(hname, hname, NMultBins, 0, NMultBins, NMultBins, 0, NMultBins));
         JtnmultVsRefnmult_LowRsp.back()->Sumw2();

         // higher rsp only
         hname = Form("JtchfVsRefchf_HighRsp_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtchfVsRefchf_HighRsp.push_back(new TH2F(hname, hname, NEfBins, 0, 1, NEfBins, 0, 1));
         JtchfVsRefchf_HighRsp.back()->Sumw2();

         hname = Form("JtnhfVsRefnhf_HighRsp_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtnhfVsRefnhf_HighRsp.push_back(new TH2F(hname, hname, NEfBins, 0, 1, NEfBins, 0, 1));
         JtnhfVsRefnhf_HighRsp.back()->Sumw2();

         hname = Form("JtnefVsRefnef_HighRsp_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtnefVsRefnef_HighRsp.push_back(new TH2F(hname, hname, NEfBins, 0, 1, NEfBins, 0, 1));
         JtnefVsRefnef_HighRsp.back()->Sumw2();

         hname = Form("JtcefVsRefcef_HighRsp_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtcefVsRefcef_HighRsp.push_back(new TH2F(hname, hname, NEfBins, 0, 1, NEfBins, 0, 1));
         JtcefVsRefcef_HighRsp.back()->Sumw2();

         hname = Form("JtmufVsRefmuf_HighRsp_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtmufVsRefmuf_HighRsp.push_back(new TH2F(hname, hname, NEfBins, 0, 1, NEfBins, 0, 1));
         JtmufVsRefmuf_HighRsp.back()->Sumw2();

         hname = Form("JtchmultVsRefchmult_HighRsp_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtchmultVsRefchmult_HighRsp.push_back(new TH2F(hname, hname, NMultBins, 0, NMultBins, NMultBins, 0, NMultBins));
         JtchmultVsRefchmult_HighRsp.back()->Sumw2();

         hname = Form("JtnmultVsRefnmult_HighRsp_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         JtnmultVsRefnmult_HighRsp.push_back(new TH2F(hname, hname, NMultBins, 0, NMultBins, NMultBins, 0, NMultBins));
         JtnmultVsRefnmult_HighRsp.back()->Sumw2();

         // rsp vs EF ratio
         float efRatioMax = 5;
         hname = Form("RelRspVsJtchfRefchfRatio_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsJtchfRefchfRatio.push_back(new TH2F(hname, hname, NEfBins, 0, efRatioMax, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsJtchfRefchfRatio.back()->Sumw2();

         hname = Form("RelRspVsJtnhfRefnhfRatio_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsJtnhfRefnhfRatio.push_back(new TH2F(hname, hname, NEfBins, 0, efRatioMax, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsJtnhfRefnhfRatio.back()->Sumw2();

         hname = Form("RelRspVsJtnefRefnefRatio_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsJtnefRefnefRatio.push_back(new TH2F(hname, hname, NEfBins, 0, efRatioMax, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsJtnefRefnefRatio.back()->Sumw2();

         hname = Form("RelRspVsJtcefRefcefRatio_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsJtcefRefcefRatio.push_back(new TH2F(hname, hname, NEfBins, 0, efRatioMax, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsJtcefRefcefRatio.back()->Sumw2();

         hname = Form("RelRspVsJtmufRefmufRatio_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsJtmufRefmufRatio.push_back(new TH2F(hname, hname, NEfBins, 0, efRatioMax, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsJtmufRefmufRatio.back()->Sumw2();

         hname = Form("RelRspVsJtchmultRefchmultRatio_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsJtchmultRefchmultRatio.push_back(new TH2F(hname, hname, NMultBins, 0, efRatioMax, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsJtchmultRefchmultRatio.back()->Sumw2();

         hname = Form("RelRspVsJtnmultRefnmultRatio_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsJtnmultRefnmultRatio.push_back(new TH2F(hname, hname, NMultBins, 0, efRatioMax, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsJtnmultRefnmultRatio.back()->Sumw2();


         hname = Form("NHadronsVsRefPt_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         int nhadrons = 6;
         NHadronsVsRefPt.push_back(new TH2F(hname, hname, NPtBins, vpt, nhadrons, 0, nhadrons));
         NHadronsVsRefPt.back()->Sumw2();

         hname = Form("RelRspVsJtArea_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         int nbinsarea = 100;
         float areamax = 1.;
         RelRspVsJtArea.push_back(new TH2F(hname, hname, nbinsarea, 0, areamax, nbinsrelrsp, relrspmin, relrspmax));
         RelRspVsJtArea.back()->Sumw2();

         // if 1 hadron
         hname = Form("RelRspVsRefPt_SingleHadron_JetEta%sto%s",eta_boundaries[ieta],eta_boundaries[ieta+1]);
         RelRspVsRefPt_SingleHadron.push_back(new TH2F(hname,hname,NPtBins,vpt,nbinsrelrsp,relrspmin,relrspmax));
         RelRspVsRefPt_SingleHadron.back()->Sumw2();

         hname = Form("RelRspVsRefPt_SingleHadron_SLDecay_JetEta%sto%s",eta_boundaries[ieta],eta_boundaries[ieta+1]);
         RelRspVsRefPt_SingleHadron_SLDecay.push_back(new TH2F(hname,hname,NPtBins,vpt,nbinsrelrsp,relrspmin,relrspmax));
         RelRspVsRefPt_SingleHadron_SLDecay.back()->Sumw2();

         hname = Form("RelRspVsRefPt_SingleHadron_HadDecay_JetEta%sto%s",eta_boundaries[ieta],eta_boundaries[ieta+1]);
         RelRspVsRefPt_SingleHadron_HadDecay.push_back(new TH2F(hname,hname,NPtBins,vpt,nbinsrelrsp,relrspmin,relrspmax));
         RelRspVsRefPt_SingleHadron_HadDecay.back()->Sumw2();

         int nbinsRef = 10;
         hname = Form("RelRspVsBJetRefInd_SingleHadron_JetEta%sto%s",eta_boundaries[ieta],eta_boundaries[ieta+1]);
         RelRspVsBJetRefInd_SingleHadron.push_back(new TH2F(hname,hname,nbinsRef, 0, nbinsRef, nbinsrelrsp,relrspmin,relrspmax));
         RelRspVsBJetRefInd_SingleHadron.back()->Sumw2();

         hname = Form("BJetRefIndVsRefPt_SingleHadron_JetEta%sto%s",eta_boundaries[ieta],eta_boundaries[ieta+1]);
         BJetRefIndVsRefPt_SingleHadron.push_back(new TH2F(hname,hname,NPtBins,vpt,nbinsRef, 0, nbinsRef));
         BJetRefIndVsRefPt_SingleHadron.back()->Sumw2();

         int nbinsRatio = 150;
         float ratioMin(0), ratioMax(1.5);
         hname = Form("RefHadronPtRatioVsRefPt_SingleHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronPtRatioVsRefPt_SingleHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsRatio, ratioMin, ratioMax));
         RefHadronPtRatioVsRefPt_SingleHadron.back()->Sumw2();

         int nbinsDeltaR = 100;
         float drMin(0.), drMax(2.);
         hname = Form("RefHadronPtRatioVsDeltaRRef_SingleHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronPtRatioVsDeltaRRef_SingleHadron.push_back(new TH2F(hname, hname, nbinsDeltaR, drMin, drMax, nbinsRatio, ratioMin, ratioMax));
         RefHadronPtRatioVsDeltaRRef_SingleHadron.back()->Sumw2();

         hname = Form("RelRspVsRefHadronPtRatio_SingleHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefHadronPtRatio_SingleHadron.push_back(new TH2F(hname, hname, nbinsRatio, ratioMin, ratioMax, nbinsrelrsp,relrspmin,relrspmax));
         RelRspVsRefHadronPtRatio_SingleHadron.back()->Sumw2();

         hname = Form("RelRspVsRefHadronDeltaRRef_SingleHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefHadronDeltaRRef_SingleHadron.push_back(new TH2F(hname, hname, nbinsDeltaR, drMin, drMax, nbinsrelrsp,relrspmin,relrspmax));
         RelRspVsRefHadronDeltaRRef_SingleHadron.back()->Sumw2();

         int nbinsPDGID = 6000;
         float pdgidMin(0), pdgidMax(6000);
         hname = Form("RelRspVsRefHadronPdgid_SingleHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefHadronPdgid_SingleHadron.push_back(new TH2F(hname, hname, nbinsPDGID, pdgidMin, pdgidMax, nbinsrelrsp,relrspmin,relrspmax));
         RelRspVsRefHadronPdgid_SingleHadron.back()->Sumw2();

         hname = Form("RefHadronPdgidVsRefPt_SingleHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronPdgidVsRefPt_SingleHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsPDGID, pdgidMin, pdgidMax));
         RefHadronPdgidVsRefPt_SingleHadron.back()->Sumw2();

         hname = Form("RefHadronNdecayVsRefPt_SingleHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronNdecayVsRefPt_SingleHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, nhadrons, 0, nhadrons));
         RefHadronNdecayVsRefPt_SingleHadron.back()->Sumw2();

         hname = Form("RefHadronSldecayVsRefPt_SingleHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronSldecayVsRefPt_SingleHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, 2, 0, 2));
         RefHadronSldecayVsRefPt_SingleHadron.back()->Sumw2();

         hname = Form("RefHadronDecayPtRatioVsRefPt_SingleHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPtRatioVsRefPt_SingleHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsRatio, ratioMin, ratioMax));
         RefHadronDecayPtRatioVsRefPt_SingleHadron.back()->Sumw2();

         hname = Form("RefHadronDecayPtRatioJetVsRefPt_SingleHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPtRatioJetVsRefPt_SingleHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsRatio, ratioMin, ratioMax));
         RefHadronDecayPtRatioJetVsRefPt_SingleHadron.back()->Sumw2();

         hname = Form("RefHadronDecayPdgidVsRefPt_SingleHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPdgidVsRefPt_SingleHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsPDGID, pdgidMin, pdgidMax ));
         RefHadronDecayPdgidVsRefPt_SingleHadron.back()->Sumw2();

         hname = Form("RefHadronDecayPtRatioVsRefPt_SingleHadron_Lepton_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPtRatioVsRefPt_SingleHadron_Lepton.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsRatio, ratioMin, ratioMax));
         RefHadronDecayPtRatioVsRefPt_SingleHadron_Lepton.back()->Sumw2();

         hname = Form("RefHadronDecayPtRatioJetVsRefPt_SingleHadron_Lepton_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPtRatioJetVsRefPt_SingleHadron_Lepton.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsRatio, ratioMin, ratioMax));
         RefHadronDecayPtRatioJetVsRefPt_SingleHadron_Lepton.back()->Sumw2();

         int nbinsLeptonIDs = 7;
         float leptonIdMin(10), leptonIdMax(17);
         hname = Form("RefHadronDecayPdgidVsRefPt_SingleHadron_Lepton_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPdgidVsRefPt_SingleHadron_Lepton.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsLeptonIDs, leptonIdMin, leptonIdMax));
         RefHadronDecayPdgidVsRefPt_SingleHadron_Lepton.back()->Sumw2();

         hname = Form("RefHadronDecayPtRatioVsRefPt_SingleHadron_Neutrino_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPtRatioVsRefPt_SingleHadron_Neutrino.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsRatio, ratioMin, ratioMax));
         RefHadronDecayPtRatioVsRefPt_SingleHadron_Neutrino.back()->Sumw2();

         hname = Form("RefHadronDecayPtRatioJetVsRefPt_SingleHadron_Neutrino_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPtRatioJetVsRefPt_SingleHadron_Neutrino.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsRatio, ratioMin, ratioMax));
         RefHadronDecayPtRatioJetVsRefPt_SingleHadron_Neutrino.back()->Sumw2();

         hname = Form("RefHadronDecayPdgidVsRefPt_SingleHadron_Neutrino_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPdgidVsRefPt_SingleHadron_Neutrino.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsLeptonIDs, leptonIdMin, leptonIdMax));
         RefHadronDecayPdgidVsRefPt_SingleHadron_Neutrino.back()->Sumw2();

         hname = Form("RelRspVsRefHadronDecayPtRatioJet_SingleHadron_Lepton_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefHadronDecayPtRatioJet_SingleHadron_Lepton.push_back(new TH2F(hname, hname, nbinsRatio, ratioMin, ratioMax, nbinsrelrsp,relrspmin,relrspmax));
         RelRspVsRefHadronDecayPtRatioJet_SingleHadron_Lepton.back()->Sumw2();

         hname = Form("RelRspVsRefHadronDecayPtRatioJet_SingleHadron_Neutrino_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefHadronDecayPtRatioJet_SingleHadron_Neutrino.push_back(new TH2F(hname, hname, nbinsRatio, ratioMin, ratioMax, nbinsrelrsp,relrspmin,relrspmax));
         RelRspVsRefHadronDecayPtRatioJet_SingleHadron_Neutrino.back()->Sumw2();

         hname = Form("RelRspVsRefHadronNDecay_SingleHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefHadronNDecay_SingleHadron.push_back(new TH2F(hname, hname, nhadrons, 0, nhadrons, nbinsrelrsp,relrspmin,relrspmax));
         RelRspVsRefHadronNDecay_SingleHadron.back()->Sumw2();

         int nbinsV = 200;
         hname = Form("RelRspVsRefHadronVx_SingleHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefHadronVx_SingleHadron.push_back(new TH2F(hname, hname, nbinsV, 0.08, 0.12, nbinsrelrsp,relrspmin,relrspmax));
         RelRspVsRefHadronVx_SingleHadron.back()->Sumw2();

         hname = Form("RelRspVsRefHadronVy_SingleHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefHadronVy_SingleHadron.push_back(new TH2F(hname, hname, nbinsV, 0.15, 0.2, nbinsrelrsp,relrspmin,relrspmax));
         RelRspVsRefHadronVy_SingleHadron.back()->Sumw2();

         hname = Form("RelRspVsRefHadronVz_SingleHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefHadronVz_SingleHadron.push_back(new TH2F(hname, hname, nbinsV, -25, 25, nbinsrelrsp,relrspmin,relrspmax));
         RelRspVsRefHadronVz_SingleHadron.back()->Sumw2();

         // if >1 b hadron
         // leading hadron
         hname = Form("RelRspVsRefPt_AtLeast2Hadron_JetEta%sto%s",eta_boundaries[ieta],eta_boundaries[ieta+1]);
         RelRspVsRefPt_AtLeast2Hadron.push_back(new TH2F(hname,hname,NPtBins,vpt,nbinsrelrsp,relrspmin,relrspmax));
         RelRspVsRefPt_AtLeast2Hadron.back()->Sumw2();

         hname = Form("RelRspVsRefPt_AtLeast2Hadron_SLDecay_JetEta%sto%s",eta_boundaries[ieta],eta_boundaries[ieta+1]);
         RelRspVsRefPt_AtLeast2Hadron_SLDecay.push_back(new TH2F(hname,hname,NPtBins,vpt,nbinsrelrsp,relrspmin,relrspmax));
         RelRspVsRefPt_AtLeast2Hadron_SLDecay.back()->Sumw2();

         hname = Form("RelRspVsRefPt_AtLeast2Hadron_HadDecay_JetEta%sto%s",eta_boundaries[ieta],eta_boundaries[ieta+1]);
         RelRspVsRefPt_AtLeast2Hadron_HadDecay.push_back(new TH2F(hname,hname,NPtBins,vpt,nbinsrelrsp,relrspmin,relrspmax));
         RelRspVsRefPt_AtLeast2Hadron_HadDecay.back()->Sumw2();

         hname = Form("BJetRefIndVsRefPt_AtLeast2Hadron_JetEta%sto%s",eta_boundaries[ieta],eta_boundaries[ieta+1]);
         BJetRefIndVsRefPt_AtLeast2Hadron.push_back(new TH2F(hname,hname,NPtBins,vpt,nbinsRef, 0, nbinsRef));
         BJetRefIndVsRefPt_AtLeast2Hadron.back()->Sumw2();

         hname = Form("RefHadronPtRatioVsRefPt_FirstHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronPtRatioVsRefPt_FirstHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsRatio, ratioMin, ratioMax));
         RefHadronPtRatioVsRefPt_FirstHadron.back()->Sumw2();

         hname = Form("RefHadronPtRatioVsDeltaRRef_FirstHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronPtRatioVsDeltaRRef_FirstHadron.push_back(new TH2F(hname, hname, nbinsDeltaR, drMin, drMax, nbinsRatio, ratioMin, ratioMax));
         RefHadronPtRatioVsDeltaRRef_FirstHadron.back()->Sumw2();

         hname = Form("RelRspVsRefHadronPtRatio_FirstHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefHadronPtRatio_FirstHadron.push_back(new TH2F(hname, hname, nbinsrelrsp,relrspmin,relrspmax, nbinsRatio, ratioMin, ratioMax));
         RelRspVsRefHadronPtRatio_FirstHadron.back()->Sumw2();

         hname = Form("RelRspVsRefHadronDeltaRRef_FirstHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefHadronDeltaRRef_FirstHadron.push_back(new TH2F(hname, hname, nbinsrelrsp,relrspmin,relrspmax, nbinsDeltaR, drMin, drMax));
         RelRspVsRefHadronDeltaRRef_FirstHadron.back()->Sumw2();

         hname = Form("RefHadronPdgidVsRefPt_FirstHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronPdgidVsRefPt_FirstHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsPDGID, pdgidMin, pdgidMax));
         RefHadronPdgidVsRefPt_FirstHadron.back()->Sumw2();

         hname = Form("RefHadronNdecayVsRefPt_FirstHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronNdecayVsRefPt_FirstHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, nhadrons, 0, nhadrons));
         RefHadronNdecayVsRefPt_FirstHadron.back()->Sumw2();

         hname = Form("RefHadronSldecayVsRefPt_FirstHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronSldecayVsRefPt_FirstHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, 2, 0, 2));
         RefHadronSldecayVsRefPt_FirstHadron.back()->Sumw2();

         hname = Form("RefHadronDecayPtRatioVsRefPt_FirstHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPtRatioVsRefPt_FirstHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsRatio, ratioMin, ratioMax));
         RefHadronDecayPtRatioVsRefPt_FirstHadron.back()->Sumw2();

         hname = Form("RefHadronDecayPdgidVsRefPt_FirstHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPdgidVsRefPt_FirstHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsPDGID, pdgidMin, pdgidMax ));
         RefHadronDecayPdgidVsRefPt_FirstHadron.back()->Sumw2();

         hname = Form("RefHadronDecayPtRatioVsRefPt_FirstHadron_Lepton_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPtRatioVsRefPt_FirstHadron_Lepton.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsRatio, ratioMin, ratioMax));
         RefHadronDecayPtRatioVsRefPt_FirstHadron_Lepton.back()->Sumw2();

         hname = Form("RefHadronDecayPdgidVsRefPt_FirstHadron_Lepton_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPdgidVsRefPt_FirstHadron_Lepton.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsLeptonIDs, leptonIdMin, leptonIdMax));
         RefHadronDecayPdgidVsRefPt_FirstHadron_Lepton.back()->Sumw2();

         hname = Form("RefHadronDecayPtRatioVsRefPt_FirstHadron_Neutrino_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPtRatioVsRefPt_FirstHadron_Neutrino.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsRatio, ratioMin, ratioMax));
         RefHadronDecayPtRatioVsRefPt_FirstHadron_Neutrino.back()->Sumw2();

         hname = Form("RefHadronDecayPdgidVsRefPt_FirstHadron_Neutrino_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPdgidVsRefPt_FirstHadron_Neutrino.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsLeptonIDs, leptonIdMin, leptonIdMax));
         RefHadronDecayPdgidVsRefPt_FirstHadron_Neutrino.back()->Sumw2();

         // subleading hadron

         hname = Form("RefHadronPtRatioVsRefPt_SecondHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronPtRatioVsRefPt_SecondHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsRatio, ratioMin, ratioMax));
         RefHadronPtRatioVsRefPt_SecondHadron.back()->Sumw2();

         hname = Form("RefHadronPtRatioVsDeltaRRef_SecondHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronPtRatioVsDeltaRRef_SecondHadron.push_back(new TH2F(hname, hname, nbinsDeltaR, drMin, drMax, nbinsRatio, ratioMin, ratioMax));
         RefHadronPtRatioVsDeltaRRef_SecondHadron.back()->Sumw2();

         hname = Form("RelRspVsRefHadronPtRatio_SecondHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefHadronPtRatio_SecondHadron.push_back(new TH2F(hname, hname, nbinsrelrsp,relrspmin,relrspmax, nbinsRatio, ratioMin, ratioMax));
         RelRspVsRefHadronPtRatio_SecondHadron.back()->Sumw2();

         hname = Form("RelRspVsRefHadronDeltaRRef_SecondHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RelRspVsRefHadronDeltaRRef_SecondHadron.push_back(new TH2F(hname, hname, nbinsrelrsp,relrspmin,relrspmax, nbinsDeltaR, drMin, drMax));
         RelRspVsRefHadronDeltaRRef_SecondHadron.back()->Sumw2();

         hname = Form("RefHadronPdgidVsRefPt_SecondHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronPdgidVsRefPt_SecondHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsPDGID, pdgidMin, pdgidMax));
         RefHadronPdgidVsRefPt_SecondHadron.back()->Sumw2();

         hname = Form("RefHadronNdecayVsRefPt_SecondHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronNdecayVsRefPt_SecondHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, nhadrons, 0, nhadrons));
         RefHadronNdecayVsRefPt_SecondHadron.back()->Sumw2();

         hname = Form("RefHadronSldecayVsRefPt_SecondHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronSldecayVsRefPt_SecondHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, 2, 0, 2));
         RefHadronSldecayVsRefPt_SecondHadron.back()->Sumw2();

         hname = Form("RefHadronDecayPtRatioVsRefPt_SecondHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPtRatioVsRefPt_SecondHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsRatio, ratioMin, ratioMax));
         RefHadronDecayPtRatioVsRefPt_SecondHadron.back()->Sumw2();

         hname = Form("RefHadronDecayPdgidVsRefPt_SecondHadron_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPdgidVsRefPt_SecondHadron.push_back(new TH2F(hname, hname, NPtBins, vpt, 6000, 0, 6000 ));
         RefHadronDecayPdgidVsRefPt_SecondHadron.back()->Sumw2();

         hname = Form("RefHadronDecayPtRatioVsRefPt_SecondHadron_Lepton_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPtRatioVsRefPt_SecondHadron_Lepton.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsRatio, ratioMin, ratioMax));
         RefHadronDecayPtRatioVsRefPt_SecondHadron_Lepton.back()->Sumw2();

         hname = Form("RefHadronDecayPdgidVsRefPt_SecondHadron_Lepton_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPdgidVsRefPt_SecondHadron_Lepton.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsLeptonIDs, leptonIdMin, leptonIdMax));
         RefHadronDecayPdgidVsRefPt_SecondHadron_Lepton.back()->Sumw2();

         hname = Form("RefHadronDecayPtRatioVsRefPt_SecondHadron_Neutrino_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPtRatioVsRefPt_SecondHadron_Neutrino.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsRatio, ratioMin, ratioMax));
         RefHadronDecayPtRatioVsRefPt_SecondHadron_Neutrino.back()->Sumw2();

         hname = Form("RefHadronDecayPdgidVsRefPt_SecondHadron_Neutrino_JetEta%sto%s", eta_boundaries[ieta], eta_boundaries[ieta+1]);
         RefHadronDecayPdgidVsRefPt_SecondHadron_Neutrino.push_back(new TH2F(hname, hname, NPtBins, vpt, nbinsLeptonIDs, leptonIdMin, leptonIdMax));
         RefHadronDecayPdgidVsRefPt_SecondHadron_Neutrino.back()->Sumw2();

      }
      RespVsEtaVsPt = new TH3F("RespVsEtaVsPt","RespVsEtaVsPt",NPtBins,vpt,NETA,veta,nbinsrelrsp,vresp);
      RespVsEtaVsPt->Sumw2();
      ScaleVsEtaVsPt = new TH3F("ScaleVsEtaVsPt","ScaleVsEtaVsPt",NPtBins,vpt,NETA,veta,nbinsrelrsp,vcorr);
      ScaleVsEtaVsPt->Sumw2();
      for(int i=0;i<NPtBins;i++)
      {
         sprintf(name,"RelRspVsJetEta_RefPt%sto%s",Pt[i],Pt[i+1]);
         RelRspVsJetEta[i] = new TH2F(name,name,NETA,veta,nbinsrelrsp,relrspmin,relrspmax);
      }
      odir->cd();

      //
      // fill histograms
      //
      TEventList* el = new TEventList("el","el");
      stringstream selection; selection<<"1";
      for (unsigned icut=0;icut<presel.size();icut++) selection<<"&&("<<presel[icut]<<")";
      if (presel.size()>0) cout<<"Selection: "<<selection.str()<<endl;
      chain->Draw(">>el",selection.str().c_str());
      cout<<"chain entries: "<<chain->GetEntries()<<" elist: "<<el->GetN()<<endl;

      chain->GetEntry( el->GetEntry(0) );

      unsigned int nevt = (evtmax>0) ? evtmax : (unsigned) el->GetN();
      cout << "Jet Collection: " << algs[a] << " ...... Processing " << nevt << " of " << el->GetN() << " entries:" << endl;
      for (unsigned int ievt=0;ievt<nevt;ievt++) {
         loadbar2(ievt+1,nevt,50,"\t");

         const Long64_t ientry = el->GetEntry(ievt);
         chain->GetEntry(ientry);

         float pthat = JRAEvt->pthat;
         float evt_fill = true;

         if (dphimin>0 && abs(JRAEvt->jtphi->at(0)-JRAEvt->jtphi->at(1))<dphimin) continue;
         if (pthatmin>0.0 && pthat<pthatmin) {
            if(verbose) cout << "WARNING::The pthat of this event is less than the minimum pthat!" << endl;
            continue;
         }
         if (pthatmax!=-1.0 && pthat>pthatmax) {
            if(verbose) cout << "WARNING::The pthat of this event is greater than the maximum pthat!" << endl;
            continue;
         }

         vector<uint> goodJetInds;
         for (unsigned int iref=0;iref<JRAEvt->nref;iref++) {
            float ptgen  = JRAEvt->refpt->at(iref);
            if (ptgen<ptgenmin) continue;
            if (ptgen>ptgenmax) continue;
            if ((relpthatmax!= -1.0) && (pthat != 0) && ((ptgen/pthat)>relpthatmax)) {
               if(verbose) cout << "WARNING::The ptref/pthat of this event is greater than the maximum relative pthat!" << endl;
               continue;
            }
            float eta    = JRAEvt->jteta->at(iref);
            if (etamax>0 && TMath::Abs(eta)>etamax) continue;
            float pt     = JRAEvt->jtpt->at(iref);
            if (pt > 14000) {
               cout << "WARNING::pt>14000 GeV (pt = " << pt << " GeV, eta = "<< eta << ")." << endl << "Skipping this jet." << endl;
               continue;
            }
            if (drmax.size()>0 && JRAEvt->refdrjt->at(iref) > drmax[a]) continue;
            goodJetInds.push_back(iref);
         }

         if (goodJetInds.size() == 0) continue;

         // Now go through and fill hists
         uint jetCounter = 0;
         for (unsigned int iref : goodJetInds) {
            if (nrefmax>0 && jetCounter==nrefmax) break;

            float rho = JRAEvt->rho;
            float ptgen  = JRAEvt->refpt->at(iref);
            float eta    = JRAEvt->jteta->at(iref);
            float abseta = fabs(eta);
            float pt     = JRAEvt->jtpt->at(iref);
            float plotEta = abseta;

            if(JetCorrector) {
               JetCorrector->setJetPt(pt);
               JetCorrector->setJetEta(eta);
               if (TString(JetInfo::get_correction_levels(levels,L1FastJet)).Contains("L1FastJet")) {
                  if (JRAEvt->jtarea->at(iref)!=0)
                     JetCorrector->setJetA(JRAEvt->jtarea->at(iref));
                  else if (jetInfo.coneSize>0)
                     JetCorrector->setJetA(TMath::Pi()*TMath::Power(jetInfo.coneSize/10.0,2));
                  else {
                     cout << "WARNING::Unknown jet area. Skipping event." << endl;
                     continue;
                  }

                   JetCorrector->setRho(JRAEvt->rho);
               }
               if(!L1FastJet) JetCorrector->setNPV(JRAEvt->npv);
            }
            float scale = (JetCorrector) ? JetCorrector->getCorrection() : 1.0;

            //
            // we have to fill this histogram before we kill the event
            //
            ScaleVsEtaVsPt->Fill(ptgen,eta,scale);
            if (scale < 0) continue;
            if (pt<ptrawmin) continue;
            if ((pt*scale)<ptmin) continue;

            // Count number of jets after all selections but before flavour selection
            // e.g. want to get the 1st jet after a potential gamma fake
            jetCounter++;

            // Do flavour selection
            if (doflavor){
               int flav = 0;
               if (flavorDef == FlavDef::Physics)
                  flav = JRAEvt->refpdgid_parton_physics->at(iref);
               else if (flavorDef == FlavDef::Algo)
                  flav = JRAEvt->refpdgid_parton_algo->at(iref);
               else if (flavorDef == FlavDef::Hadron)
                  flav = JRAEvt->refpdgid_hadron->at(iref);
               else if (flavorDef == FlavDef::HadronParton) {
                  int hadronid = abs(JRAEvt->refpdgid_hadron->at(iref));
                  int partonid = abs(JRAEvt->refpdgid_parton_physics->at(iref));
                  if (abs(partonid) == 4 || abs(partonid) == 5) partonid = 0;
                  flav = hadronid != 0 ? hadronid : partonid;
               }

               flav = abs(flav);

               // Only use jets if match our desired pdgid
               if (abs(pdgid)!=12) {
                  if (abs(flav)!=abs(pdgid)) continue;
               } else {
                  if (flav>2 || flav==0) continue;
               }
            }

            // Check no genjet-genjet overlaps
            // if (drmin>0) {
            //    float refEta = JRAEvt->refeta->at(iref);
            //    float refPhi = JRAEvt->refphi->at(iref);
            //    bool overlap = false;
            //    for (unsigned int jref : goodJetInds) {
            //       if (jref == iref) {
            //          continue;
            //       } else {
            //          float thisDeltaR = reco::deltaR(refEta, refPhi, JRAEvt->refeta->at(jref), JRAEvt->refphi->at(jref));
            //          // Care about cuts on other genjets?
            //          // if (thisDeltaR < drmin && JRAEvt->refpt->at(jref) > 0.3/ptgen) {
            //          if (thisDeltaR < drmin && JRAEvt->refpt->at(jref) > 10) {
            //             overlap = true;
            //             break;
            //          }
            //       }
            //    }
            //    if (overlap) continue;
            // }

            float relrsp = scale*JRAEvt->jtpt->at(iref)/JRAEvt->refpt->at(iref);
            double weight(1.0);

            if(xsection>0.0) weight = (xsection*luminosity)/nevt;
            if(useweight) weight = JRAEvt->weight;
            if(!(xsection>0.0) && !useweight) weight = 1.0;
            if(weightHist!=nullptr) weight *= weightHist->GetBinContent(weightHist->FindBin(ptgen,eta));
            // if(!MCPUReWeighting.IsNull() && !DataPUReWeighting.IsNull()) {
            //    double LumiWeight = LumiWeights_.weight(JRAEvt->tnpus->at(iIT));
            //    weight *= LumiWeight;
            // }
            if(pThatReweight!=-9999) weight*=pow(pthat/15.,pThatReweight);


            if(evt_fill) {pThatDistribution->Fill(pthat,weight); evt_fill=false;}
            //-4 to cut off the negative side of the detector
            if(eta<veta[NETA] && eta > veta[0]) {
               if(debug && ientry>5400000) {
                  cout << "fabs(eta)="<< fabs(eta) << endl;
                  cout << "veta[NETA]=" << veta[NETA] << endl;
                  cout << "getBin(fabs(eta),veta,NETA)-4=" << getBin(fabs(eta),veta,NETA)-(NETA/2) << endl;
               }
               uint etaBin = getBin(plotEta,veta,NETA);
               RelRspVsRefPt[etaBin]->Fill(ptgen,relrsp,weight);

               JtchfVsRefPt[etaBin]->Fill(ptgen,JRAEvt->jtchf->at(iref),weight);
               JtnhfVsRefPt[etaBin]->Fill(ptgen,JRAEvt->jtnhf->at(iref),weight);
               JtnefVsRefPt[etaBin]->Fill(ptgen,JRAEvt->jtnef->at(iref),weight);
               JtcefVsRefPt[etaBin]->Fill(ptgen,JRAEvt->jtcef->at(iref),weight);
               JtmufVsRefPt[etaBin]->Fill(ptgen,JRAEvt->jtmuf->at(iref),weight);
               JtchmultVsRefPt[etaBin]->Fill(ptgen,JRAEvt->jtchmult->at(iref),weight);
               JtnmultVsRefPt[etaBin]->Fill(ptgen,JRAEvt->jtnmult->at(iref),weight);

               RefchfVsRefPt[etaBin]->Fill(ptgen,JRAEvt->refchf->at(iref),weight);
               RefnhfVsRefPt[etaBin]->Fill(ptgen,JRAEvt->refnhf->at(iref),weight);
               RefnefVsRefPt[etaBin]->Fill(ptgen,JRAEvt->refnef->at(iref),weight);
               RefcefVsRefPt[etaBin]->Fill(ptgen,JRAEvt->refcef->at(iref),weight);
               RefmufVsRefPt[etaBin]->Fill(ptgen,JRAEvt->refmuf->at(iref),weight);
               RefchmultVsRefPt[etaBin]->Fill(ptgen,JRAEvt->refchmult->at(iref),weight);
               RefnmultVsRefPt[etaBin]->Fill(ptgen,JRAEvt->refnmult->at(iref),weight);

               RelRspVsJtchf[etaBin]->Fill(JRAEvt->jtchf->at(iref),relrsp,weight);
               RelRspVsJtnhf[etaBin]->Fill(JRAEvt->jtnhf->at(iref),relrsp,weight);
               RelRspVsJtnef[etaBin]->Fill(JRAEvt->jtnef->at(iref),relrsp,weight);
               RelRspVsJtcef[etaBin]->Fill(JRAEvt->jtcef->at(iref),relrsp,weight);
               RelRspVsJtmuf[etaBin]->Fill(JRAEvt->jtmuf->at(iref),relrsp,weight);
               RelRspVsJtchmult[etaBin]->Fill(JRAEvt->jtchmult->at(iref),relrsp,weight);
               RelRspVsJtnmult[etaBin]->Fill(JRAEvt->jtnmult->at(iref),relrsp,weight);

               RelRspVsRefchf[etaBin]->Fill(JRAEvt->jtchf->at(iref),relrsp,weight);
               RelRspVsRefnhf[etaBin]->Fill(JRAEvt->jtnhf->at(iref),relrsp,weight);
               RelRspVsRefnef[etaBin]->Fill(JRAEvt->jtnef->at(iref),relrsp,weight);
               RelRspVsRefcef[etaBin]->Fill(JRAEvt->jtcef->at(iref),relrsp,weight);
               RelRspVsRefmuf[etaBin]->Fill(JRAEvt->jtmuf->at(iref),relrsp,weight);
               RelRspVsRefchmult[etaBin]->Fill(JRAEvt->jtchmult->at(iref),relrsp,weight);
               RelRspVsRefnmult[etaBin]->Fill(JRAEvt->jtnmult->at(iref),relrsp,weight);

               JtchfVsRefchf[etaBin]->Fill(JRAEvt->refchf->at(iref),JRAEvt->jtchf->at(iref),weight);
               JtnhfVsRefnhf[etaBin]->Fill(JRAEvt->refnhf->at(iref),JRAEvt->jtnhf->at(iref),weight);
               JtnefVsRefnef[etaBin]->Fill(JRAEvt->refnef->at(iref),JRAEvt->jtnef->at(iref),weight);
               JtcefVsRefcef[etaBin]->Fill(JRAEvt->refcef->at(iref),JRAEvt->jtcef->at(iref),weight);
               JtmufVsRefmuf[etaBin]->Fill(JRAEvt->refmuf->at(iref),JRAEvt->jtmuf->at(iref),weight);
               JtchmultVsRefchmult[etaBin]->Fill(JRAEvt->refchmult->at(iref),JRAEvt->jtchmult->at(iref),weight);
               JtnmultVsRefnmult[etaBin]->Fill(JRAEvt->refnmult->at(iref),JRAEvt->jtnmult->at(iref),weight);

               RelRspVsJtchfRefchfRatio[etaBin]->Fill(safe_divide(JRAEvt->jtchf->at(iref), JRAEvt->refchf->at(iref)),relrsp,weight);
               RelRspVsJtnhfRefnhfRatio[etaBin]->Fill(safe_divide(JRAEvt->jtnhf->at(iref), JRAEvt->refnhf->at(iref)),relrsp,weight);
               RelRspVsJtnefRefnefRatio[etaBin]->Fill(safe_divide(JRAEvt->jtnef->at(iref), JRAEvt->refnef->at(iref)),relrsp,weight);
               RelRspVsJtcefRefcefRatio[etaBin]->Fill(safe_divide(JRAEvt->jtcef->at(iref), JRAEvt->refcef->at(iref)),relrsp,weight);
               RelRspVsJtmufRefmufRatio[etaBin]->Fill(safe_divide(JRAEvt->jtmuf->at(iref), JRAEvt->refmuf->at(iref)),relrsp,weight);
               RelRspVsJtchmultRefchmultRatio[etaBin]->Fill(safe_divide(JRAEvt->jtchmult->at(iref), JRAEvt->refchmult->at(iref)),relrsp,weight);
               RelRspVsJtnmultRefnmultRatio[etaBin]->Fill(safe_divide(JRAEvt->jtnmult->at(iref), JRAEvt->refnmult->at(iref)),relrsp,weight);

               if (relrsp < 1.1) {
                  JtchfVsRefchf_LowRsp[etaBin]->Fill(JRAEvt->refchf->at(iref),JRAEvt->jtchf->at(iref),weight);
                  JtnhfVsRefnhf_LowRsp[etaBin]->Fill(JRAEvt->refnhf->at(iref),JRAEvt->jtnhf->at(iref),weight);
                  JtnefVsRefnef_LowRsp[etaBin]->Fill(JRAEvt->refnef->at(iref),JRAEvt->jtnef->at(iref),weight);
                  JtcefVsRefcef_LowRsp[etaBin]->Fill(JRAEvt->refcef->at(iref),JRAEvt->jtcef->at(iref),weight);
                  JtmufVsRefmuf_LowRsp[etaBin]->Fill(JRAEvt->refmuf->at(iref),JRAEvt->jtmuf->at(iref),weight);
                  JtchmultVsRefchmult_LowRsp[etaBin]->Fill(JRAEvt->refchmult->at(iref),JRAEvt->jtchmult->at(iref),weight);
                  JtnmultVsRefnmult_LowRsp[etaBin]->Fill(JRAEvt->refnmult->at(iref),JRAEvt->jtnmult->at(iref),weight);
               } else {
                  JtchfVsRefchf_HighRsp[etaBin]->Fill(JRAEvt->refchf->at(iref),JRAEvt->jtchf->at(iref),weight);
                  JtnhfVsRefnhf_HighRsp[etaBin]->Fill(JRAEvt->refnhf->at(iref),JRAEvt->jtnhf->at(iref),weight);
                  JtnefVsRefnef_HighRsp[etaBin]->Fill(JRAEvt->refnef->at(iref),JRAEvt->jtnef->at(iref),weight);
                  JtcefVsRefcef_HighRsp[etaBin]->Fill(JRAEvt->refcef->at(iref),JRAEvt->jtcef->at(iref),weight);
                  JtmufVsRefmuf_HighRsp[etaBin]->Fill(JRAEvt->refmuf->at(iref),JRAEvt->jtmuf->at(iref),weight);
                  JtchmultVsRefchmult_HighRsp[etaBin]->Fill(JRAEvt->refchmult->at(iref),JRAEvt->jtchmult->at(iref),weight);
                  JtnmultVsRefnmult_HighRsp[etaBin]->Fill(JRAEvt->refnmult->at(iref),JRAEvt->jtnmult->at(iref),weight);
               }
               
               RelRspVsJtArea[etaBin]->Fill(JRAEvt->jtarea->at(iref), relrsp, weight);

               // Bhadron hists
               uint nBHadrons = JRAEvt->ref_nhadron->at(iref);
               // uint nBHadrons = 0;
               NHadronsVsRefPt[etaBin]->Fill(ptgen, nBHadrons, weight);
               // find the start for this jet's hadrons,
               // need to sum over number of hadrons in all previous jets
               uint thisBhadronStartInd = 0;
               uint thisBhadronDecayStartInd = 0;
               for (uint ij=0; ij<iref; ij++) {
                  uint nb = JRAEvt->ref_nhadron->at(ij);
                  // for each b hadron, add number of its decay products
                  for (uint id=0; id < nb; id++){
                     thisBhadronDecayStartInd += JRAEvt->ref_hadron_ndecay->at(thisBhadronStartInd+id);
                  }
                  thisBhadronStartInd += nb;
               }
               if(nBHadrons == 1) {
                  RelRspVsRefPt_SingleHadron[etaBin]->Fill(ptgen, relrsp, weight);
                  RelRspVsBJetRefInd_SingleHadron[etaBin]->Fill(iref, relrsp, weight);
                  BJetRefIndVsRefPt_SingleHadron[etaBin]->Fill(ptgen, iref, weight);

                  float bHadronPt = JRAEvt->ref_hadron_pt->at(thisBhadronStartInd);
                  RefHadronPtRatioVsRefPt_SingleHadron[etaBin]->Fill(ptgen, bHadronPt/ptgen, weight);

                  float hadronEta = JRAEvt->ref_hadron_eta->at(thisBhadronStartInd);
                  float hadronPhi = JRAEvt->ref_hadron_phi->at(thisBhadronStartInd);
                  float refEta = JRAEvt->refeta->at(iref);
                  float refPhi = JRAEvt->refphi->at(iref);
                  float dRHadronJet = reco::deltaR(hadronEta, hadronPhi, refEta, refPhi);
                  RefHadronPtRatioVsDeltaRRef_SingleHadron[etaBin]->Fill(dRHadronJet, bHadronPt/ptgen, weight);

                  RelRspVsRefHadronPtRatio_SingleHadron[etaBin]->Fill(bHadronPt/ptgen, relrsp, weight);
                  RelRspVsRefHadronDeltaRRef_SingleHadron[etaBin]->Fill(dRHadronJet, relrsp, weight);

                  int bHadronPdgid = abs(JRAEvt->ref_hadron_pdgid->at(thisBhadronStartInd));
                  RelRspVsRefHadronPdgid_SingleHadron[etaBin]->Fill(bHadronPdgid, relrsp, weight);
                  RefHadronPdgidVsRefPt_SingleHadron[etaBin]->Fill(ptgen, bHadronPdgid, weight);

                  int ndecay = JRAEvt->ref_hadron_ndecay->at(thisBhadronStartInd);
                  RefHadronNdecayVsRefPt_SingleHadron[etaBin]->Fill(ptgen, ndecay ,weight);
                  RelRspVsRefHadronNDecay_SingleHadron[etaBin]->Fill(ndecay, relrsp, weight);

                  int sldecay = JRAEvt->ref_hadron_sldecay->at(thisBhadronStartInd);
                  RefHadronSldecayVsRefPt_SingleHadron[etaBin]->Fill(ptgen, sldecay, weight);

                  if (sldecay==1) {
                     RelRspVsRefPt_SingleHadron_SLDecay[etaBin]->Fill(ptgen, relrsp, weight);
                  } else {
                     RelRspVsRefPt_SingleHadron_HadDecay[etaBin]->Fill(ptgen, relrsp, weight);
                  }

                  RelRspVsRefHadronVx_SingleHadron[etaBin]->Fill(JRAEvt->ref_hadron_vx->at(thisBhadronStartInd), relrsp, weight);
                  RelRspVsRefHadronVy_SingleHadron[etaBin]->Fill(JRAEvt->ref_hadron_vy->at(thisBhadronStartInd), relrsp, weight);
                  RelRspVsRefHadronVz_SingleHadron[etaBin]->Fill(JRAEvt->ref_hadron_vz->at(thisBhadronStartInd), relrsp, weight);

                  // iterate over all decay products
                  for (uint id=0; id<JRAEvt->ref_hadron_ndecay->at(thisBhadronStartInd); id++) {
                     float decayPt = JRAEvt->ref_hadron_decay_pt->at(thisBhadronDecayStartInd+id);
                     RefHadronDecayPtRatioVsRefPt_SingleHadron[etaBin]->Fill(ptgen,decayPt/bHadronPt,weight);
                     RefHadronDecayPtRatioJetVsRefPt_SingleHadron[etaBin]->Fill(ptgen,decayPt/ptgen,weight);

                     int decayPdgid = abs(JRAEvt->ref_hadron_decay_pdgid->at(thisBhadronDecayStartInd+id));
                     RefHadronDecayPdgidVsRefPt_SingleHadron[etaBin]->Fill(ptgen,decayPdgid,weight);

                     if (decayPdgid == 11 || decayPdgid == 13 || decayPdgid == 15) {
                        RefHadronDecayPtRatioVsRefPt_SingleHadron_Lepton[etaBin]->Fill(ptgen,decayPt/bHadronPt,weight);
                        RefHadronDecayPtRatioJetVsRefPt_SingleHadron_Lepton[etaBin]->Fill(ptgen,decayPt/ptgen,weight);
                        RefHadronDecayPdgidVsRefPt_SingleHadron_Lepton[etaBin]->Fill(ptgen,decayPdgid,weight);
                        RelRspVsRefHadronDecayPtRatioJet_SingleHadron_Lepton[etaBin]->Fill(decayPt/ptgen,relrsp,weight);
                     }
                     if (decayPdgid == 12 || decayPdgid == 14 || decayPdgid == 16) {
                        RefHadronDecayPtRatioVsRefPt_SingleHadron_Neutrino[etaBin]->Fill(ptgen,decayPt/bHadronPt,weight);
                        RefHadronDecayPtRatioJetVsRefPt_SingleHadron_Neutrino[etaBin]->Fill(ptgen,decayPt/ptgen,weight);
                        RefHadronDecayPdgidVsRefPt_SingleHadron_Neutrino[etaBin]->Fill(ptgen,decayPdgid,weight);
                        RelRspVsRefHadronDecayPtRatioJet_SingleHadron_Neutrino[etaBin]->Fill(decayPt/ptgen,relrsp,weight);
                     }
                  }
               } else if (nBHadrons > 1) {
                  RelRspVsRefPt_AtLeast2Hadron[etaBin]->Fill(ptgen, relrsp, weight);
                  BJetRefIndVsRefPt_AtLeast2Hadron[etaBin]->Fill(ptgen, iref, weight);

                  // leading hadron
                  float bHadronPt = JRAEvt->ref_hadron_pt->at(thisBhadronStartInd);
                  RefHadronPtRatioVsRefPt_FirstHadron[etaBin]->Fill(ptgen, bHadronPt/ptgen, weight);

                  float hadronEta = JRAEvt->ref_hadron_eta->at(thisBhadronStartInd);
                  float hadronPhi = JRAEvt->ref_hadron_phi->at(thisBhadronStartInd);
                  float refEta = JRAEvt->refeta->at(iref);
                  float refPhi = JRAEvt->refphi->at(iref);
                  float dRHadronJet = reco::deltaR(hadronEta, hadronPhi, refEta, refPhi);
                  RefHadronPtRatioVsDeltaRRef_FirstHadron[etaBin]->Fill(dRHadronJet, bHadronPt/ptgen, weight);

                  RelRspVsRefHadronPtRatio_FirstHadron[etaBin]->Fill(bHadronPt/ptgen, relrsp, weight);
                  RelRspVsRefHadronDeltaRRef_FirstHadron[etaBin]->Fill(dRHadronJet, relrsp, weight);

                  int bHadronPdgid = abs(JRAEvt->ref_hadron_pdgid->at(thisBhadronStartInd));
                  RefHadronPdgidVsRefPt_FirstHadron[etaBin]->Fill(ptgen, bHadronPdgid, weight);

                  int ndecay = JRAEvt->ref_hadron_ndecay->at(thisBhadronStartInd);
                  RefHadronNdecayVsRefPt_FirstHadron[etaBin]->Fill(ptgen, ndecay ,weight);

                  int sldecay = JRAEvt->ref_hadron_sldecay->at(thisBhadronStartInd);
                  RefHadronSldecayVsRefPt_FirstHadron[etaBin]->Fill(ptgen, sldecay, weight);

                  if (sldecay==1) {
                     RelRspVsRefPt_AtLeast2Hadron_SLDecay[etaBin]->Fill(ptgen, relrsp, weight);
                  } else {
                     RelRspVsRefPt_AtLeast2Hadron_HadDecay[etaBin]->Fill(ptgen, relrsp, weight);
                  }

                  // iterate over all decay products
                  for (uint id=0; id<JRAEvt->ref_hadron_ndecay->at(thisBhadronStartInd); id++) {
                     float decayPt = JRAEvt->ref_hadron_decay_pt->at(thisBhadronDecayStartInd+id);
                     RefHadronDecayPtRatioVsRefPt_FirstHadron[etaBin]->Fill(ptgen,decayPt/bHadronPt,weight);

                     int decayPdgid = abs(JRAEvt->ref_hadron_decay_pdgid->at(thisBhadronDecayStartInd+id));
                     RefHadronDecayPdgidVsRefPt_FirstHadron[etaBin]->Fill(ptgen,decayPdgid,weight);

                     if (decayPdgid == 11 || decayPdgid == 13 || decayPdgid == 15) {
                        RefHadronDecayPtRatioVsRefPt_FirstHadron_Lepton[etaBin]->Fill(ptgen,decayPt/bHadronPt,weight);
                        RefHadronDecayPdgidVsRefPt_FirstHadron_Lepton[etaBin]->Fill(ptgen,decayPdgid,weight);
                     }
                     if (decayPdgid == 12 || decayPdgid == 14 || decayPdgid == 16) {
                        RefHadronDecayPtRatioVsRefPt_FirstHadron_Neutrino[etaBin]->Fill(ptgen,decayPt/bHadronPt,weight);
                        RefHadronDecayPdgidVsRefPt_FirstHadron_Neutrino[etaBin]->Fill(ptgen,decayPdgid,weight);
                     }
                  }


                  //subleading
                  bHadronPt = JRAEvt->ref_hadron_pt->at(thisBhadronStartInd+1);
                  RefHadronPtRatioVsRefPt_SecondHadron[etaBin]->Fill(ptgen, bHadronPt/ptgen, weight);

                  hadronEta = JRAEvt->ref_hadron_eta->at(thisBhadronStartInd+1);
                  hadronPhi = JRAEvt->ref_hadron_phi->at(thisBhadronStartInd+1);
                  dRHadronJet = reco::deltaR(hadronEta, hadronPhi, refEta, refPhi);
                  RefHadronPtRatioVsDeltaRRef_SecondHadron[etaBin]->Fill(dRHadronJet, bHadronPt/ptgen, weight);

                  RelRspVsRefHadronPtRatio_SecondHadron[etaBin]->Fill(bHadronPt/ptgen, relrsp, weight);
                  RelRspVsRefHadronDeltaRRef_SecondHadron[etaBin]->Fill(dRHadronJet, relrsp, weight);

                  bHadronPdgid = abs(JRAEvt->ref_hadron_pdgid->at(thisBhadronStartInd+1));
                  RefHadronPdgidVsRefPt_SecondHadron[etaBin]->Fill(ptgen, bHadronPdgid, weight);

                  ndecay = JRAEvt->ref_hadron_ndecay->at(thisBhadronStartInd+1);
                  RefHadronNdecayVsRefPt_SecondHadron[etaBin]->Fill(ptgen, ndecay ,weight);

                  sldecay = JRAEvt->ref_hadron_sldecay->at(thisBhadronStartInd+1);
                  RefHadronSldecayVsRefPt_SecondHadron[etaBin]->Fill(ptgen, sldecay, weight);

                  // add # decay products from leading jet to offset
                  thisBhadronDecayStartInd += JRAEvt->ref_hadron_ndecay->at(thisBhadronStartInd);

                  for (uint id=0; id<JRAEvt->ref_hadron_ndecay->at(thisBhadronStartInd+1); id++) {
                     float decayPt = JRAEvt->ref_hadron_decay_pt->at(thisBhadronDecayStartInd+id);
                     RefHadronDecayPtRatioVsRefPt_SecondHadron[etaBin]->Fill(ptgen,decayPt/bHadronPt,weight);

                     int decayPdgid = abs(JRAEvt->ref_hadron_decay_pdgid->at(thisBhadronDecayStartInd+id));
                     RefHadronDecayPdgidVsRefPt_SecondHadron[etaBin]->Fill(ptgen,decayPdgid,weight);

                     if (decayPdgid == 11 || decayPdgid == 13 || decayPdgid == 15) {
                        RefHadronDecayPtRatioVsRefPt_SecondHadron_Lepton[etaBin]->Fill(ptgen,decayPt/bHadronPt,weight);
                        RefHadronDecayPdgidVsRefPt_SecondHadron_Lepton[etaBin]->Fill(ptgen,decayPdgid,weight);
                     }
                     if (decayPdgid == 12 || decayPdgid == 14 || decayPdgid == 16) {
                        RefHadronDecayPtRatioVsRefPt_SecondHadron_Neutrino[etaBin]->Fill(ptgen,decayPt/bHadronPt,weight);
                        RefHadronDecayPdgidVsRefPt_SecondHadron_Neutrino[etaBin]->Fill(ptgen,decayPdgid,weight);
                     }
                  }
               }

            }

            RespVsEtaVsPt->Fill(ptgen,plotEta,relrsp,weight);

            j = getBin(ptgen,vpt,NPtBins);
            k = getBin(plotEta,veta,NETA);
            if (j<NPtBins && j>=0 && k<NETA && k>=0)
            {
               RelRspVsJetEta[j]->Fill(plotEta,relrsp,weight);

            }//if (j<NPtBins && j>=0)

         }//for (unsigned char iref=0;iref<nrefmax;iref++)
      }//for (unsigned int ievt=0;ievt<nevt;ievt++)

      //
      // final cout statements
      //

      delete chain;
   }//for(unsigned int a=0; a<algs.size(); a++)

   cout << "Write " << "Closure.root" << " ... ";
   outf->cd();
   outf->Write();
   cout << "DONE" << endl;
   outf->Close();

   m_benchmark->Stop("event");
   cout << "jet_correction_analyzer_x" << endl << "\tCPU time = " << m_benchmark->GetCpuTime("event") << " s" << endl
        << "\tReal time = " << m_benchmark->GetRealTime("event") << " s" << endl;
   delete m_benchmark;

   return 0;
}

////////////////////////////////////////////////////////////////////////////////
// implement local functions
////////////////////////////////////////////////////////////////////////////////

//______________________________________________________________________________
int getBin(double x, const double boundaries[], int length)
{
   int i;
   int n = length;
   if (n<=0) return -1;
   if (x<boundaries[0] || x>=boundaries[n])
      return -1;
   for(i=0;i<n;i++)
   {
      if (x>=boundaries[i] && x<boundaries[i+1])
         return i;
   }
   return 0;
}

//______________________________________________________________________________
string get_flavor_name(int pdgid)
{
   string result;
   int abspdgid = abs(pdgid);
   if      (abspdgid==1 || abspdgid==2) result = "qJ";
   else if (abspdgid==12)               result = "udJ";
   else if (abspdgid==3)                result = "sJ";
   else if (abspdgid==4)                result = "cJ";
   else if (abspdgid==5)                result = "bJ";
   else if (abspdgid==21)               result = "gJ";
   else if (abspdgid==9999)             result = "aJ";
   else {
      cout << "***ERROR***get_flavor_name::flavor for PDGID="<<pdgid<<" is not known"<<endl;
   }
   return result;
}

//______________________________________________________________________________
string getPostfix(vector<string> postfix, string alg, int level)
{
  for(unsigned int ipostfix=0; ipostfix<postfix.size(); ipostfix+=3)
    {
      TString tmp(postfix[ipostfix+1]);
      if(postfix[ipostfix].compare(alg)==0 && atoi(tmp.Data())==level)
        return postfix[ipostfix+2];
    }
  return "";
}

/*
  TO DO::FOR FLAVOR ANALYSIES
  -give list of pdgids
  -create folders for each pdgid on list
  -check one pdgid at a time
  -map pdgid==1 || pdgid==2 || pdgid==3 to light quarks
*/

bool sort_by_pt(const TLorentzVector & a, const TLorentzVector & b)
{
   return a.Pt() > b.Pt();
}

float safe_divide(float a, float b){
   if (b == 0) {
      return std::numeric_limits<float>::infinity();
   } else {
      return a / b;
   }
}