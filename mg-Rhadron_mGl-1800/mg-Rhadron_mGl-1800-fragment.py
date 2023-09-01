FLAVOR = 'gluino'
COM_ENERGY = 13000. # GeV
MASS_POINT = 1800   # GeV
PROCESS_FILE = 'SimG4Core/CustomPhysics/data/RhadronProcessList.txt'
PARTICLE_FILE = 'Configuration/Generator/data/particles_%s_%d_GeV.txt'  % (FLAVOR, MASS_POINT)
SLHA_FILE ='Configuration/Generator/data/HSCP_%s_%d_SLHA.spc' % (FLAVOR, MASS_POINT)
PDT_FILE = 'Configuration/Generator/data/hscppythiapdt%s%d.tbl'  % (FLAVOR, MASS_POINT)
USE_REGGE = False

import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *  

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring("/afs/cern.ch/user/m/masizemo/hscp/GENrecipie/mg-Rhadron_mGl-1800/mg-Rhadron_mGl-1800_slc7_amd64_gcc10_CMSSW_12_4_8_tarball.tar.xz"),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

import math

generator = cms.EDFilter("Pythia8HadronizerFilter",
  maxEventsToPrint = cms.untracked.int32(1),
  pythiaPylistVerbosity = cms.untracked.int32(1),
  filterEfficiency = cms.untracked.double(1.0),
  pythiaHepMCVerbosity = cms.untracked.bool(False),
  comEnergy = cms.double(13000.),
  PythiaParameters = cms.PSet(
    pythia8CommonSettingsBlock,
    pythia8CP5SettingsBlock,
    JetMatchingParameters = cms.vstring(
      'JetMatching:setMad = off',
      'JetMatching:scheme = 1',
      'JetMatching:merge = on',
      'JetMatching:jetAlgorithm = 2',
      'JetMatching:etaJetMax = 5.',
      'JetMatching:coneRadius = 1.',
      'JetMatching:slowJetPower = 1',
      'JetMatching:qCut = 147', #this is the actual merging scale
      'JetMatching:nQmatch = 5', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
      'JetMatching:nJetMax = 2', #number of partons in born matrix element for highest multiplicity
      'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
      '6:m0 = 172.5',
      '24:mMin = 7',
      'Check:abortIfVeto = on',
    ),
    processParameters = cms.vstring(
      'RHadrons:allow  = on',
      'RHadrons:allowDecay = off',
      'RHadrons:setMasses = on',
      'RHadrons:probGluinoball = 0.1',
	),     
    parameterSets = cms.vstring('pythia8CommonSettings',
      'pythia8CP5Settings',
      'JetMatchingParameters',
      'processParameters'
    )
  ),
 # SLHATableForPythia8 = cms.string(baseSLHATable),
)

#generator.hscpFlavor = cms.untracked.string(FLAVOR)
#generator.massPoint = cms.untracked.int32(MASS_POINT)
#generator.particleFile = cms.untracked.string(PARTICLE_FILE)
#generator.slhaFile = cms.untracked.string(SLHA_FILE)
#generator.processFile = cms.untracked.string(PROCESS_FILE)
#generator.pdtFile = cms.FileInPath(PDT_FILE)
#generator.useregge = cms.bool(USE_REGGE)

#We would like to change the particleID lists to be more inclusive of all RHadrons.
dirhadrongenfilter = cms.EDFilter("MCParticlePairFilter",
    Status = cms.untracked.vint32(1, 1),
    MinPt = cms.untracked.vdouble(0., 0.),
    MinP = cms.untracked.vdouble(0., 0.),
    MaxEta = cms.untracked.vdouble(100., 100.),
    MinEta = cms.untracked.vdouble(-100, -100),
    ParticleCharge = cms.untracked.int32(0),
    ParticleID1 = cms.untracked.vint32(1000993,1009213,1009313,1009323,1009113,1009223,1009333,1091114,1092114,1092214,1092224,1093114,1093214,1093224,1093314,1093324,1093334),
    ParticleID2 = cms.untracked.vint32(1000993,1009213,1009313,1009323,1009113,1009223,1009333,1091114,1092114,1092214,1092224,1093114,1093214,1093224,1093314,1093324,1093334)
)

ProductionFilterSequence = cms.Sequence(generator*dirhadrongenfilter)
