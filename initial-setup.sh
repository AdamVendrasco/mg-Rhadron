#! /usr/bin/bash

cmssw_version=$1

if [[ ! -z $(ls | grep "genproductions") ]]; then
	echo "genproductions already installed. Skipping."
	sleep 2
else
	echo "genproductions not found. Cloning."
	sleep 2
	git clone git@github.com:cms-sw/genproductions.git
fi

echo "installing declared CMSSW version $cmssw_version"
sleep 2
cmsrel $cmssw_version

