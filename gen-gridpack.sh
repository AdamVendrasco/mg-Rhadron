#! /usr/bin/bash

# bash gridpack-gen.sh mg-Rhadron_mGl-1800 CMSSW_12_4_8 1000 mergeOff

run=$1
cmssw_version="${2:-}"
nevents="${3:-100}"
debug_tag="${4:-}"
parent_dir_name=$(basename "$PWD")

if [[ $cmssw_version == "" ]]; then
	echo "No CMSSW version declared. Checking for parent CMSSW directory"
	if [[ "$parent_dir_name" != "CMSSW"* ]]; then
		echo "Parent directory is not a CMSSW distrobution. Exiting."
		exit 1
	else
		cmssw_version=$parent_dir_name
		echo "Parent directory is a CMSSW distrobution. Using parent CMSSW directory version $cmssw_version"
	fi 
elif [ $cmssw_version != $parent_dir_name ]; then
	echo "Declared CMSSW version does not match CMSSW directory. Exiting."
	exit 1
else
	echo "Parent directory matches declared CMSSW version. Proceeding."
fi

config_in_filename="$run-fragment.py"
config_out_filename="../output-configs/$run-$cmssw_version-n$nevents-$debug_tag-1_cfg.py"
root_out_filename="../root-files/$run-$cmssw_version-n$nevents-$debug_tag.root"
debug_out_filename="../text-logs/$run-$cmssw_version-n$nevents-$debug_tag.debug"

if [[ ! -z $(grep -F "$cmssw_version" "src/Configuration/GenProduction/python/$config_in_filename") ]]; then
	echo "Gridpack CMSSW version matches declared CMSSSW version."
else
	echo "gridpack CMSSW version does not match declared CMSSW version. Exiting."
fi 

echo "Storing log file in $debug_out_filename"
echo "Setting up cmsenv"
cmsenv
echo "Copying $config_in_filename from ../$run/input-configs/ to src/Configuration/GenProduction/python/"
cp -v ../$run/input-configs/$config_in_filename src/Configuration/GenProduction/python/
echo "Scram step"
scram b

nohup cmsDriver.py Configuration/GenProduction/python/$config_in_filename --python_filename $config_out_filename --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:$root_out_filename --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step LHE,GEN --geometry DB:Extended --era Run2_2018 --mc -n $nevents 2>&1 | tee $debug_out_filename
