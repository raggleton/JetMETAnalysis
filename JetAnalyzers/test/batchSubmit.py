#!/usr/bin/env python

"""
This script is designed to submit lots of CRAB jobs.
"""


import subprocess
import os
from time import strftime
from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
from httplib import HTTPException
from DasQuery import autocomplete_Datasets
from multiprocessing import Process, Pool


inputDatasets = [

# MG+Pythia
# '/DYJetsToLL_M-50_HT-*_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_*/AODSIM',
# '/QCD_HT*_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6*/AODSIM',
# '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext*/AODSIM',
# '/GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',
# '/GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/AODSIM',
# '/GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',
# '/GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/AODSIM',
# '/GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',
# '/GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/AODSIM',
# '/GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',
# '/GJets_HT-40To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/AODSIM',
# '/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',
# '/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/AODSIM',

# Herwig
# '/GJet_Pt-15To6000_TuneCUETHS1-Flat_13TeV_herwigpp/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',
# '/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/MINIAODSIM',  # the large stats one WARNING MINIAOD
 
'/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/RunIISummer16MiniAODv2-NoPU_80X_mcRun2_asymptotic_2016_TrancheIV_v4-v1/MINIAODSIM',

# '/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',
# '/TT_TuneEE5C_13TeV-powheg-herwigpp/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext3-v1/AODSIM',  # the v1, v2 don't exist on disk
# '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-herwigpp_30M/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',  # does actually have MG, uses HS1 tune
# '/DYJetsToLL_M-50_TuneCUETHS1_13TeV-madgraphMLM-herwigpp/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/AODSIM',  # doesn't actually use MG
# '/QCD_Pt-15to7000_TuneCH2_Flat_13TeV_herwig7/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM',
# '/QCD_Pt-15to7000_TuneCH2_Flat_13TeV_herwig7/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15-v2/MINIAODSIM',

# '/QCD_Pt-15to7000_TuneCH2_Flat_13TeV_herwig7/RunIIAutumn18DRPremix-102X_upgrade2018_realistic_v15-v2/AODSIM',
# '/QCD_Pt-15to7000_TuneCH2_Flat_13TeV_herwig7/RunIIAutumn18DR-NoPU_102X_upgrade2018_realistic_v15-v2/AODSIM',

# Pythia only
# '/QCD_Pt-15to7000_TuneCUETP8M1_FlatP6_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',
# '/QCD_Pt_15to30_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v*/AODSIM',
# '/QCD_Pt_30to50_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v*/AODSIM',
# '/QCD_Pt_50to80_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v*/AODSIM',
# '/QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v*/AODSIM',
# '/QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v*/AODSIM',
# '/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v*/AODSIM',
# '/QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v*/AODSIM',
# '/QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v*/AODSIM',
# '/QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v*/AODSIM',
# '/QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v*/AODSIM',
# '/QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v*/AODSIM',
# '/QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v*/AODSIM',
# '/QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v*/AODSIM',
# '/QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v*/AODSIM',
# '/QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v*/AODSIM',

# '/QCD_Pt_15to30_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',
# '/QCD_Pt_30to50_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v*/MINIAODSIM',
# '/QCD_Pt_50to80_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v*/MINIAODSIM',
# '/QCD_Pt_80to120_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v*/MINIAODSIM',
# '/QCD_Pt_120to170_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v*/MINIAODSIM',
# '/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v*/MINIAODSIM',
# '/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v*/MINIAODSIM',
# '/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v*/MINIAODSIM',
# '/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v*/MINIAODSIM',
# '/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',
# '/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v*/MINIAODSIM',
# '/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v*/MINIAODSIM',
# '/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v*/MINIAODSIM',
# '/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v*/MINIAODSIM',
# '/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v*/MINIAODSIM',

# '/QCD_Pt_15to30_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',
# '/QCD_Pt_30to50_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
# '/QCD_Pt_50to80_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
# '/QCD_Pt_50to80_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',
# '/QCD_Pt_80to120_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
# '/QCD_Pt_120to170_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
# '/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
# '/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
# '/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
# '/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',
# '/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
# '/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',
# '/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
# '/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
# '/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',
# '/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
# '/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',
# '/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
# '/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',
# '/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
# '/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-NoPU_102X_upgrade2018_realistic_v15_ext2-v2/MINIAODSIM',

# 2017 samples for P8M1 vs CP5 tests
# '/QCD_Pt-15to7000_TuneCP5_Flat2017_13TeV_pythia8/RunIIFall17MiniAOD-PU2017_94X_mc2017_realistic_v11-v1/MINIAODSIM',
# '/QCD_Pt-15to7000_TuneCUETP8M1_Flat_13TeV_pythia8/RunIIFall17MiniAOD-PU2017_94X_mc2017_realistic_v11-v1/MINIAODSIM',

# POWHEG+Pythia
# '/Dijet_NNPDF30_powheg_pythia8_TuneCUETP8M1_13TeV_bornktmin150/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/AODSIM',
# '/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM',
]

filter_keywords = [
'GenJets5',
'BGenFilter',
]

# requestNameCustom = "_Autumn18_noJEC_constitInfo_miniaod_withPF"
requestNameCustom = "_Summer16_noJEC_constitInfo_miniaod_withPF"


def filter_datasets(input_datasets):
    return [x for x in input_datasets if not any(y in x for y in filter_keywords)]


def create_request_name(input_dataset):
    name = input_dataset.split('/')[1]
    modified_name = (name.replace('_TuneCUETP8M1_13TeV-madgraphMLM-pythia8','')
                         .replace('_TuneCUETHS1_13TeV-madgraphMLM-herwigpp', '')
                         .replace('_TuneCUETP8M1_13TeV-madgraphMLM-herwigpp_30M', '')
                         .replace('_TuneCUETP8M1_FlatP6_13TeV_pythia8', '')
                         .replace('_TuneCUETP8M1_13TeV_pythia8', '')
                         .replace('_TuneCUETHS1_Flat_13TeV_herwigpp', '')
                         .replace('_pythia8_TuneCUETP8M1_13TeV_bornktmin150', '')
                         .replace("_TuneCH2_Flat_13TeV_herwig7", "")
                         .replace('_TuneEE5C_13TeV-powheg-herwigpp', '')
                         .replace('_TuneCP5_13TeV_pythia8', '')
                         .replace('_TuneCP5_Flat2017_13TeV_pythia8', '')
                         .replace('_TuneCUETP8M1_Flat_13TeV_pythia8', '')
                    )
    if 'ext1' in input_dataset:
        modified_name += '_ext1'
    elif 'ext2' in input_dataset:
        modified_name += '_ext2'
    elif 'ext' in input_dataset:
        modified_name += '_ext'

    # Shorten generator names
    if 'madgraphMLM-pythia8' in input_dataset:
        modified_name += '_mg-pythia'
    elif 'madgraphMLM-herwigpp_30M' in input_dataset:
        modified_name += '_mg-herwig-proper'
    elif 'madgraphMLM-herwigpp' in input_dataset:
        if 'DYJetsToLL' in input_dataset:
            # cos it isnt actually MG
            modified_name += '_herwig'
        else:
            modified_name += '_mg-herwig-30M'  # ???
    elif 'powheg-herwigpp' in input_dataset:
        modified_name += '_powheg-herwig'
    elif 'powheg_pythia8' in input_dataset:
        modified_name += '_powheg-pythia'
    elif '_pythia8' in input_dataset:
        modified_name += '_pythia'
    elif '_herwigpp' in input_dataset:
        modified_name += '_herwig'
    elif '_herwig7' in input_dataset:
        modified_name += '_herwig7'

    if "cp5" in input_dataset.lower():
        modified_name += "_CP5"
    elif "ch2" in input_dataset.lower():
        modified_name += "_CH2"
    elif "p8m1" in input_dataset.lower():
        modified_name += "_P8M1"

    if 'nopu' in input_dataset.lower():
        modified_name += "_noPU"

    modified_name += "_" + strftime('%d_%b_%y') + requestNameCustom
    return modified_name


def create_crab_config(request_name, input_dataset):
    conf = config()
    conf.General.workArea = 'crab_test'
    conf.General.transferOutputs = True
    conf.General.transferLogs = True
    conf.General.requestName = request_name

    conf.JobType.pluginName = 'Analysis'
    conf.JobType.psetName = 'run_JRA_cfg.py'
    # conf.JobType.outputFiles = ["Ntuple.root"]
    conf.JobType.maxMemoryMB = 2000
    # conf.JobType.inputFiles = ['Summer16_07Aug2017_V1_MC.db']

    conf.Data.inputDataset = input_dataset
    conf.Data.inputDBS = 'global'
    conf.Data.splitting = 'EventAwareLumiBased'
    conf.Data.unitsPerJob = 50000
    # conf.Data.totalUnits = 
    conf.Data.publication = False
    # conf.JobType.sendExternalFolder = True
    #conf.Data.allowNonValidInputDataset = True
    
    # conf.Data.ignoreLocality=True
    # conf.Site.blacklist = ['T2_CH_CSCS', 'T2_TW_NCHC']
    # conf.Site.whitelist = ['T2_DE_DESY']

    conf.Site.storageSite = 'T2_DE_DESY'

    return conf


def write_crab_config_file(conf, filename):
    contents = conf.pythonise_()
    if not os.path.isdir(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, "w") as f:
        f.write(contents)


def submit_config(config_filename):
    # Why not use crabCommand? Well it does weird thing importing the analysis config
    # So you end up with duplciated modules sometimes
    subprocess.call('crab submit -c %s' % os.path.abspath(config_filename), shell=True)


def main():
    print "Getting datasets..."
    input_datasets = filter_datasets(autocomplete_Datasets(inputDatasets))
    request_names = [create_request_name(in_data) for in_data in input_datasets]
    print "Creating Configuration objects..."
    configs = [create_crab_config(rn, in_data) for rn, in_data in zip(request_names, input_datasets)]
    config_filenames = [os.path.join('crab_configs', c.General.requestName, 'crab.py') for c in configs]
    for c, fn in zip(configs, config_filenames):
        write_crab_config_file(c, fn)
    print "Submitting..."
    try:
        p = Pool(1)
        # result = p.map_async(submit_config, configs)
        result = p.map_async(submit_config, config_filenames)
        print result.get()
        p.close()
    except KeyboardInterrupt:
        print 'Got ^C while pool mapping, terminating the pool'
        p.terminate()
        print 'Pool is terminated'
    except Exception, e:
        print 'Got exception: %r, terminating the pool' % (e,)
        p.terminate()
        print 'Pool is terminated'
    finally:
        print 'Joining pool processes'
        p.join()
        print 'Join complete'
    print 'The end'


if __name__ == '__main__':
    main()
