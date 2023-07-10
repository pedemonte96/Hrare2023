#!/bin/bash
# Creates and compares files with the branch names of different ROOT files
declare -A paths
# Add key-value pairs to the paths
paths["br_omega.txt"]="/work/submit/mariadlf/Hrare/D02/2018/ggh-homegagamma-powheg/NANOAOD_03_test4/step7_ggH_OmegaGamma_9.root"
paths["br_phi3.txt"]="/work/submit/mariadlf/Hrare/D02/2018/ggh-hphipipipi0gamma-powheg/NANOAOD_03_test4/step7_ggH_Phi3Gamma_9.root"
paths["br_d0StarKmRho.txt"]="/work/submit/mariadlf/Hrare/D02/2018/ggh-hD0StarKmPiPPi0gamma-powheg/NANOAOD_03_test4/step7_ggh-hD0StarKmPiPPi0gamma_7.root"
paths["br_d0Star.txt"]="/work/submit/mariadlf/Hrare/D02/2018/ggh-hD0Stargamma-powheg/NANOAOD_03_test4/step7_ggH_HD0StarGamma_9.root"

# Iterate over keys and values in the paths
for namefile in "${!paths[@]}"; do
    path="${paths[$namefile]}"
    echo -e "Creating $namefile..."
    #Printing information to $namefile
    root -q -l 'gettingOutput.C("'${path}'")' > ${namefile} 2> /dev/null

    #Delete all lines that don't contain pattern "*Br"
    sed -i '/\*Br/!d' ${namefile}
    #Replaces any sequence of caracters followed by ":" by nothing (deleting)
    sed -i 's/[^:]*://' ${namefile}
    #Replaces any sequence of caracters after a ":" by nothing (deleting)
    sed -i 's/:.*//' ${namefile}
    tput cuu1 && tput el
    #hash=$(echo "$(sha1sum ${namefile})" | awk '{print $1}')
    #echo -e "$namefile:\t$hash"
    sha1sum $namefile
done
