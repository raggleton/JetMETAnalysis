#!/bin/bash -e

set -u

declare -a samples=(
    "jra_QCD_FLAT_NoJEC" 
    "jra_QCD_FLAT_withL1L2L3_Summer16_03Feb2017_V8" 
    "jra_QCD_FLAT_withL1L2L3_Summer16_23Sep2016V4" 
    "jra_QCD_FLAT_HERWIG_NoJEC_ak4pfchs_newFlav" 
    "jra_QCD_FLAT_HERWIG_withL1L2L3_Summer16_03Feb2017_V8_ak4pfchs_newFlav"
    )

declare -a settings=(
    "fitMean"
    "rawMean"
    "median"
    )

for sample in ${samples[@]}
do
    for setting in ${settings[@]}
    do
        echo $sample, $setting
        algo="ak4pfchs"
        if [[ "$sample" == *"L1L2L3"* ]]
        then
            algo=${algo}l1l2l3
        fi

        jet_response_and_resolution_x -input ${sample}_f.root -output ${sample}_f_g_${setting}.root -flavors ud s c b g -algs ${algo} -metric ${setting}
    done
done

