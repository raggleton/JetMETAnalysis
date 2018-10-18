import FWCore.ParameterSet.Config as cms

#!
#! PROCESS
#!
# Conditions source options: GT, SQLite, DB
conditionsSource = "GT"
era = "Fall17_17Nov2017_V11"
doProducer = False
process = cms.Process("JRA")
multithread = False
if doProducer:
        process = cms.Process("JRAP")
        multithread = True


#!
#! CHOOSE ALGORITHMS
#!
# Note: Not all combinations of options will work
# Algorithm options: ak, kt, ic, sc, ca
# Size options: integers 1-10
# Jet type options: calo, pf, pfchs, puppi
# Correction levels: '' (blank), l1, l2, l3, l2l3, l1l2l3
algsizetype = {'ak':[4,8]}
jettype = ['pfchs','puppi']

algsizetype = {'ak':[4]}
jettype = ['pfchs']
corrs = ['']

algorithms = []
jcr = cms.VPSet()

for k, v in algsizetype.iteritems():
    for s in v:
        for j in jettype:
            for c in corrs:
                algorithms.append(str(k+str(s)+j+c))
                if conditionsSource != "GT":
                    upperAlg = str(k.upper()+str(s)+j.upper().replace("CHS","chs")).replace("PUPPI","PFPuppi")
                    jcr.append(cms.PSet(record = cms.string("JetCorrectionsRecord"),
                                        tag = cms.string("JetCorrectorParametersCollection_"+era+"_"+upperAlg),
                                        label= cms.untracked.string(upperAlg)))

# If need be you can append additional jet collections using the style below
#algorithms.append('ak5calo')


#!
#! CONDITIONS (DELIVERING JEC BY DEFAULT!)
#!
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.GlobalTag.globaltag = cms.string('80X_mcRun2_asymptotic_2016_TrancheIV_v8')

if conditionsSource != "GT":
    if conditionsSource == "DB":
        conditionsConnect = cms.string("frontier://FrontierPrep/CMS_COND_PHYSICSTOOLS")
    elif conditionsSource == "SQLite":
        conditionsConnect = cms.string('sqlite_file:'+era+'.db')

    from CondCore.DBCommon.CondDBSetup_cfi import *
    process.jec = cms.ESSource("PoolDBESSource",CondDBSetup,
                               connect = conditionsConnect,
                               toGet =  cms.VPSet(jcr))
    process.es_prefer_jec = cms.ESPrefer("PoolDBESSource","jec")


#!
#! INPUT
#!
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(5000))

##############################################
# External Input File (most likely from DAS) #
##############################################
# try:
#     process.load("JetMETAnalysis.JetAnalyzers.<filename without extension>")
# except ImportError:
#     print "Couldn't open the external list of files from DAS. If you just checkout out the JetResponseAnalyzer package you will need to make this file yourself. Currently Falling back to opening the list hard-coded in run_JRA_cfg.py. This is not a bad action as long as it is what you intended to have happen."
#     inputFiles = cms.untracked.vstring(
#           'root://cmsxrootd.fnal.gov//store/mc/<path to root file>/<filename>.root',
#           )
#     process.source = cms.Source("PoolSource", fileNames = inputFiles )
process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring('root://cmsxrootd.fnal.gov//store/mc/RunIISummer16DR80Premix/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/100000/02A0DA71-14D3-E611-8FEE-A0000420FE80.root')
        # fileNames = cms.untracked.vstring('root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv2/QCD_Pt-15to7000_TuneCUETHS1_Flat_13TeV_herwigpp/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v2/10000/3C313E17-5DAF-E811-9A68-A0369F7F8E80.root')
)


#!
#! SERVICES
#!
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100
# process.MessageLogger.cerr.FwkReport.reportEvery = 1
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True))
if doProducer:
    process.add_(cms.Service("Tracer"))
    process.options.numberOfThreads = cms.untracked.uint32(8)
    process.options.numberOfStreams = cms.untracked.uint32(0)
else:
    process.load('CommonTools.UtilAlgos.TFileService_cfi')
    process.TFileService.fileName=cms.string('JRA.root')


#!
#! NEEDED FOR PFCHS
#!
process.load('CommonTools.ParticleFlow.pfNoPileUpJME_cff')
process.pfPileUpJME.checkClosestZVertex = False


#!
#! JET & REFERENCE KINEMATIC CUTS
#!
import JetMETAnalysis.JetAnalyzers.Defaults_cff as Defaults


#!
#! RUN JET RESPONSE ANALYZER
#!

# set to False to use jets from the input file (NOT RECOMMENDED)
doJetReco = True
doMiniAOD = False
outCom = cms.untracked.vstring('drop *')
from JetMETAnalysis.JetAnalyzers.addAlgorithm import addAlgorithm
for algorithm in algorithms:
    if (algorithm.find('HLT') > 0) :
        process.load("Configuration.Geometry.GeometryIdeal_cff")
        process.load("Configuration.StandardSequences.MagneticField_cff")
        addAlgorithm(process,algorithm,Defaults,False,doProducer,doMiniAOD)
    else:
        addAlgorithm(process,algorithm,Defaults,doJetReco,doProducer,doMiniAOD)
    outCom.extend(['keep *_'+algorithm+'_*_*'])


#!
#! Check the keep and drop commands being added to the outputCommamnds
#!
printOC = False
if printOC:
    for oc in outCom:
        print oc

# process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
# process.printTree = cms.EDAnalyzer("ParticleListDrawer",
#   maxEventsToPrint = cms.untracked.int32(1),
#   printVertex = cms.untracked.bool(False),
#   printOnlyHardInteraction = cms.untracked.bool(False), # Print only status=3 particles. This will not work for Pythia8, which does not have any such particles.
#   src = cms.InputTag("prunedGenParticles")
# )
# process.ak4pfchsPath *= process.printTree

#!
#! Output
#!
if doProducer:
    process.out = cms.OutputModule("PoolOutputModule",
                                   fileName = cms.untracked.string('JRAP.root'),
                                   outputCommands = outCom
                                   )
    process.e = cms.EndPath(process.out)


#!
#! THAT'S ALL! CAN YOU BELIEVE IT? :-D
#!

#Not sure what this does
#processDumpFile = open('runJRA.dump' , 'w')
#print >> processDumpFile, process.dumpPython()
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.options.allowUnscheduled = cms.untracked.bool(True)
