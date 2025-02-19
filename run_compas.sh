source ~/.bashrc
~/COMPAS/src/COMPAS --number-of-systems=$1 \
--initial-mass-min=$2 --initial-mass-max=$3 \
--metallicity=$4 --common-envelope-alpha=$5 \
--output-path=$6 --initial-mass-function=UNIFORM \
--kick-magnitude-distribution=MAXWELLIAN \
--remnant-mass-prescription=FRYER2012 \
--fryer-supernova-engine=DELAYED \
--kick-magnitude-sigma-CCSN-BH=$7 \
--kick-magnitude-sigma-CCSN-NS=$8
