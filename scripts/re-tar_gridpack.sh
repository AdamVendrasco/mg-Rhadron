#! usr/bin/bash

echo "Removing old tarball"
sleep .5
rm -v modified-GlGl_mGl-1500_tarball.tar.xz
sleep .5
echo "Changing directory to ./modified-GlGl_mGl-1500_tarball"
sleep .5
pwd
sleep .5
echo "Creating new tarball"
sleep .5
tar -cvJf ../modified-GlGl_mGl-1500_tarball.tar.xz InputCards/ gridpack_generation.log merge.pl mgbasedir/ process/ runcmsgrid.sh


