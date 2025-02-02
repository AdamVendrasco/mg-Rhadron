# mg-Rhadron

After cloning, run ```bash initial-setup.sh <cmssw_version> <run (optional)>``` in the root of the repo. Example: ```bash initial-setup.sh CMSSW_12_4_8 mg-Rhadron_mGl-1800```  
To gen, run ```bash run-gridpack.sh <run> <cmssw_version> <nevents> <debug_tag>``` in the root of the repo. Example: ```bash run-gridpack.sh mg-Rhadron_mGl-1800 CMSSW_12_4_8 1000 test```  

Notes:
1. scripts require you to have a configured github ssh-key.
2. If you use an older cmssw release (eg. CMSSW_12_4_8) you will need to run in a singualrity image of Centos for that release. For CMSSW_12_4_8 I use Centos 7 or cmssw-el7. To run in a singualrity container for different versions of Centos type the follwouing command:
```cmssw-(centos version)```. For example to get into a Centos 7 image I use ```cmssw-el7```.
