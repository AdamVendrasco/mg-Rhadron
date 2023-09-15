# mg-Rhadron

After cloning, run ```bash initial-setup.sh <cmssw_version> <run (optional)>``` in the root of the repo. Example: ```bash initial-setup.sh CMSSW_12_4_8 mg-Rhadron_mGl-1800```  
To gen, run ```bash run-gridpack.sh <run> <cmssw_version> <nevents> <debug_tag>``` in the root of the repo. Example: ```bash run-gridpack.sh mg-Rhadron_mGl-1800 CMSSW_12_4_8 1000 test```  

Note, scripts require you to have a configured github ssh-key.
