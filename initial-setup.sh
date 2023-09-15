#! /usr/bin/bash

cmssw_version=$1
run=${2:-}

if [[ ! -z $(ls | grep "genproductions") ]]; then
	echo "genproductions already installed."
	sleep 2
else
	echo "genproductions not found. Cloning."
	sleep 2
	git clone git@github.com:cms-sw/genproductions.git
fi

if [[ ! -z $(ls | grep "$cmssw_version") ]]; then
        echo "$cmssw_version already installed."
        sleep 2
else
        echo "$cmssw_version not found. Installing..."
        sleep 2
	cmsrel $cmssw_version
	echo "creating path for pythia config fragment in $cmssw_version directory"
	sleep 2
	mkdir -vp $cmssw_version/src/Configuration/GenProduction/python/
fi

if [[ $run == "" ]]; then
	echo "no run specified. Exiting."
	exit 1	
else
	if [[ ! -z $(ls | grep "$run") ]]; then
		echo "$run directory already exists. Exiting."
		exit 1
	else		
		echo "$run directory does not exist. Building directory structure."
		mkdir -vp $run/input-cards/ $run/output-configs/ $run/root-files/ $run/text-logs/ $run/input-configs
	fi
fi
