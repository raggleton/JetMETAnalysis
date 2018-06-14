#!/bin/bash

STEM="jra_QCD_FLAT_NoJEC_oldFlav"
STEM="jra_QCD_FLAT_withL1L2L3_Summer16_03Feb2017_V8_oldFlav"
STEM="jra_QCD_FLAT_withL1L2L3_Summer16_23Sep2016V4_oldFlav"
STEM="jra_QCD_FLAT_HERWIG_NoJEC_ak4pfchs_newFlav"
# STEM="jra_QCD_FLAT_HERWIG_NoJEC_ak4pfchs_oldFlav"
STEM="jra_QCD_FLAT_HERWIG_withL1L2L3_Summer16_03Feb2017_V8_ak4pfchs_newFlav"
# STEM="jra_QCD_FLAT_HERWIG_withL1L2L3_Summer16_03Feb2017_V8_ak4pfchs_oldFlav"
# hadd ${STEM}.root ${STEM}_ak4pfchs.root ${STEM}_ak4puppi.root ${STEM}_ak8pfchs.root ${STEM}_ak8puppi.root
jet_response_fitter_x -input ${STEM}.root -output ${STEM}_f.root -doFlavor true
jet_response_and_resolution_x -input ${STEM}_f.root -flavors ud s c b g
