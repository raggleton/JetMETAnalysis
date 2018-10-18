#!/usr/bin/env bash

set -e
set -u

# This encapsulates what I do to make and test L2 JECs
# It is designed to run over a small sample so you can see all the steps
# But that means it will probably produce weird results!

# MAKE A NTUPLE OF MATCHED PAIRS
# Make sure the run_JRA_cfg.py is setup how you want
# This makes a file called JRA.root
# This might take a little while, time for a cuppa
# Make sure you have a VO certificate
cmsRun run_JRA_cfg.py

# APPLY L1FastJet JECs
# See JetAnalyzers/bin/jet_apply_jec_x.cc
# This just makes a copy of the Ntuple but with updated reco jet pt
JAJ_INPUT="JRA.root"
JAJ_OUTPUT="JAJX.root"
jet_apply_jec_x -input "$JAJ_INPUT" -output "$JAJ_OUTPUT" \
    -algs ak4pfchs -levels 1 \
    -era Summer16_07Aug2017_V15_MC \
    -jecpath $CMSSW_BASE/src/JetMETAnalysis/JECDatabase/textFiles/Summer16_07Aug2017_V15_MC/ \
    -L1FastJet true -saveitree false

# # MAKE RESPONSE HISTOGRAMS
# # See JetAnalyzers/bin/jet_response_analyzer_x.cc
JRA_OUTPUT="JRAX.root"
jet_response_analyzer_x ../config/jra_flavour_wide.config \
    -input "$JAJ_OUTPUT" -output "$JRA_OUTPUT" \
    -algs ak4pfchsl1:0.2 -flavorDefinition HADRONPARTON \
    -xsection -1 \
    -jtptmin 4 -relpthatmax 2.5 \
    -nbinsrelrsp 10000 -relrspmax 6 -useweight true

# CALCULATE L2 CORRECTIONS FOR ud JETS
# See JetAnalyzers/bin/jet_l2_correction_x.cc
L2_OUTPUT="L2X.root"
FLAV="g"
ERA="MyTestJEC_$FLAV"
jet_l2_correction_x -input "$JRA_OUTPUT" -algs ak4pfchsl1 \
    -l2l3 true -histMet median -era "$ERA" \
    -output "$L2_OUTPUT" -batch true \
    -flavor g_ -fitMin 10 -l2pffit standard

# TEST CORRECTIONS BY APPPLYING THEM
# See JetAnalyzers/bin/jet_correction_analyzer_x.cc
CLOSURE_DIR="ClosureTest"
if [ ! -d $CLOSURE_DIR ]; then mkdir $CLOSURE_DIR; fi
jet_correction_analyzer_x -inputFilename "$JAJ_OUTPUT" \
    -outputDir "$CLOSURE_DIR" -algs ak4pfchsl1 \
    -era "$ERA" -path $(pwd) -levels 2 \
    -doflavor true -pdgid 21 -flavorDefinition HADRONPARTON \
    -suffix _$FLAV \
    -xsection -1 -luminosity 35900 -useweight true \
    -nrefmax 2 -ptgenmin 4 -ptrawmin 4 -relpthatmax 2.5 -relrspmax 2 \
    -drmin 0.8 \
    -drmax 0.2
    # -alphamax $(alpha) -pfCandIds $(pfpid) -pfCandPtMin $(pfpt) -pfCandDr $(pfdr) -efmax $(efmax) \
    # -findZ $(findz) -findGamma $(findgamma) 

# DRAW CLOSURE PLOTS
# See JetAnalyzers/bin/jet_draw_closure_x.cc
# See JetUtilities/src/ClosureMaker.cc
jet_draw_closure_x  -doPt true -doEta true \
    -doRatioPt false -doRatioEta false -ptcl false \
    -histMet median -outputFormat ".pdf" \
    -filename "${CLOSURE_DIR}/Closure_ak4pfchsl1" \
    -flavor $FLAV \
    -title "QCD MC ($FLAV jets)" \
    -outputDir "${CLOSURE_DIR}"
