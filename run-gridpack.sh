#! /usr/bin/bash

# bash gridpack-gen.sh mg-Rhadron_mGl-1800 CMSSW_12_4_8 1000 mergeOff

run=$1
cmssw_version="${2:-}"
nevents="${3:-100}"
debug_tag="${4:-}"
parent_dir_name=$(basename "$PWD")

config_in_filename="$run-fragment.py"

if [[ $cmssw_version == "" ]]; then
	echo "No CMSSW version declared. Exiting"
	exit 1
elif[[ ! -z $(ls | grep "$cmssw_version") ]]; then
	echo "Declared CMSSW version $cmssw_version installed."
else
	echo "Declared CMSSW version $cmssw_version not found. Exiting."
	exit 1
fi

if [[ ! -z $(grep -F "$cmssw_version" "$cmssw_version/src/Configuration/GenProduction/python/$config_in_filename") ]]; then
        echo "Gridpack CMSSW version matches declared CMSSSW version."
else
        echo "gridpack CMSSW version does not match declared CMSSW version. Exiting."
	exit 1
fi

config_out_filename="$run/output-configs/$run-$cmssw_version-n$nevents-$debug_tag-1_cfg.py"
root_out_filename="$run/root-files/$run-$cmssw_version-n$nevents-$debug_tag.root"
debug_out_filename="$run/text-logs/$run-$cmssw_version-n$nevents-$debug_tag.debug"


echo "Storing log file in $debug_out_filename"
echo "Copying $config_in_filename from $run/input-configs/ to src/Configuration/GenProduction/python/"
cp -v $run/input-configs/$config_in_filename $cmssw_version/src/Configuration/GenProduction/python/


genStart() {
	cd -v $cmssw_version
	echo "Setting up cmsenv"
	cmsenv
	echo "Scram step"
	scram b

	nohup cmsDriver.py Configuration/GenProduction/python/$config_in_filename --python_filename $config_out_filename --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:$root_out_filename --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --step LHE,GEN --geometry DB:Extended --era Run2_2018 --mc -n $nevents 2>&1 | tee $debug_out_filename
}

genStart()
