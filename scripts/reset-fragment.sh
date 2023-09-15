#! /usr/bin/bash

echo "Cleaning /src/Configuration/GenProduction/python of auto-generated files"
rm -v ~/hscp/GENrecipie/CMSSW_10_6_25/src/Configuration/GenProduction/python/__*
rm -v ~/hscp/GENrecipie/CMSSW_10_6_25/src/Configuration/GenProduction/python/*.pyc
rm -v ~/hscp/GENrecipie/CMSSW_10_6_25/src/*_cfg.py

cd ~/hscp/GENrecipie/CMSSW_10_6_25/src
cmsenv
scram b

echo "setup complete. Ready for cmsDriver."
