#!/usr/bin/python

#
# Run GEANT4 simulations for the Modulation setup
#
# runsim.py -s <source_type> -n <number_of_events>
#
#   <source_type>       - which source ti44, co60, cs137, mn54
#   <number_of_events>  - number of events to simulate
#
# A.P. Colijn - colijn@nikhef.nl
#

import sys,os
import getopt
#--------------------------------------------------------------------------------------------

# IMPORTANT: set the variables below according to your own system

# where is the modusim code
simulation_basedir = "/user/z37/Modulation/modusim"
# where should the output go
output_basedir = "/data/atlas/users/acolijn/Modulation/simulation"
# where should the scripts for running go?
run_dir = output_basedir + "/macros"

# ROOT VERSION
###ROOT_version = "6.04.10-x86_64-slc6-gcc48-opt"
### GEANT4 VERSION
###GEANT4_version = "/cvmfs/geant4.cern.ch/geant4/10.1.p02/x86_64-slc6-gcc48-opt/bin/"
###GEANT4_version = "10.1.p02"

#--------------------------------------------------------------------------------------------
def make_G4preinit_script():
    #
    # make the preinit_script
    #
    print('make_preinit_script:: macro ='+preinit_script)
    
    fout = open(preinit_script,'w')
    
    fout.write('# GEANT4 - G4simu pre_init macro (AUTOMATICALLY GENERATED) \n')
    # EM physics list to select: emlivermore, empenelope
    fout.write('/run/physics/setEMlowEnergyModel emlivermore \n')
    # HAD physics list to select: G4QGSP_BERT or G4QGSP_BERT_HP
    fout.write('/run/physics/setHadronicModel    G4QGSP_BERT_HP \n')
    # do we like to have the physics histograms or not? true OR false
    fout.write('/run/physics/setHistograms true \n')
    # format of the output ntuple = compact OR raw
    fout.write('/G4simu/analysis/setTreeType compact \n')
    
    fout.close()
#--------------------------------------------------------------------------------------------
def make_G4run_script():
    #
    # make the run_script
    #
    print('make_run_script:: macro ='+run_script)
    
    fout = open(run_script,'w')
    
    fout.write('# GEANT4 - G4simu run macro (AUTOMATICALLY GENERATED) \n')
    fout.write('/control/verbose  0 \n')
    fout.write('/run/verbose      0\n')
    fout.write('/event/verbose    0\n')
    fout.write('/tracking/verbose 0\n')
    
    fout.write('/run/random/setRandomSeed '+str(ran_seed)+'\n')
    
    fout.write('/gps/pos/type    Volume\n')
    fout.write('/gps/pos/shape   Sphere\n')
    fout.write('/gps/pos/centre  0. 0. 0. cm\n')
    fout.write('/gps/pos/radius  1 cm\n')
    fout.write('/gps/pos/confine SourceCore\n')
    fout.write('/gps/ang/type   iso\n')
    
    fout.write('/grdm/BRbias 0\n')
    fout.write('/grdm/fBeta 0\n')
    fout.write('/grdm/verbose 0\n')
    fout.write('/grdm/analogueMC 1\n')
    fout.write('/gps/particle ion\n')
    fout.write('/gps/energy 0. eV\n')
    
    if   source_name == 'ti44':
        fout.write('/gps/ion 22 44 0 0 \n')
        fout.write('/grdm/nucleusLimits 44 44 22 22 \n')
    elif source_name == 'sc44':
        fout.write('/gps/ion 21 44 0 0 \n')
        fout.write('/grdm/nucleusLimits 44 44 21 21 \n')
    elif source_name == 'mn54':
        fout.write('/gps/ion 25 54 \n')
    elif source_name == 'co60':
        fout.write('/gps/ion 27 60 \n')
    elif source_name == 'cs137':
        fout.write('/gps/ion 55 137 \n')
    else:
        print('make_G4run_script::ERROR source '+source_name+' not recognized')
        print('make_G4run_script::      -s <ti44, sc44, co60, cs137, mn54>')
        sys.exit(2)
    
    fout.close()
#--------------------------------------------------------------------------------------------
def make_shell_script():
    #
    # make the shell script for running on stoomboot
    #
    
    print('make_run_script:: macro ='+shell_script)
    fout = open(shell_script,'w')
    fout.write('#!/bin/csh \n')
    
    fout.write('# AUTOMATICALLY GENERATED FILE \n')
    fout.write(' \n')
    fout.write('setenv BASEDIR `pwd` \n')
    fout.write(' \n')
    fout.write('cd '+simulation_basedir+'  \n')
    fout.write('source setup_geant4.csh \n')
#    fout.write(' \n')
#    fout.write('cd '+GEANT4_version+' \n')
#    fout.write(' \n')
#    fout.write('source geant4.csh \n')
#    fout.write(' \n')
    fout.write('cd ${BASEDIR} \n')
    fout.write(' \n')

#    fout.write('source /project/atlas/nikhef/cvmfs/setup.csh \n')
#    fout.write(' \n')
#    fout.write('setupATLAS \n')
#    fout.write(' \n')
#    fout.write('localSetupROOT '+ROOT_version+' \n')
#    fout.write(' \n')
#    fout.write('setenv CXX `which g++` \n')
#    fout.write(' \n')
#    fout.write('setenv CC `which gcc` \n')
#    fout.write(' \n')
    fout.write('cd '+run_dir+' \n')
    fout.write(' \n')
#    fout.write('setenv LD_LIBRARY_PATH ${LD_LIBRARY_PATH}:/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase/x86_64/root/'+ROOT_version+'/lib \n')
    fout.write(simulation_basedir+'/../modusim-build/G4simu -p '+preinit_script+' -f '+run_script+' -n '+str(numberOfEvents)+' -o '+output_root)
    fout.write(' \n')
    
    fout.close()
    
    cmd = 'chmod +x '+shell_script
    os.system(cmd)
#--------------------------------------------------------------------------------------------
def parseArguments(argv):
    # interpret the command line arguments
    source = 'null'
    nevent = 0

    try:
        opts, args = getopt.getopt(argv,"s:n:",["source","nevent"])
    except getopt.GetoptError:
        print('runsim.py -s <source_type> -n <number_of_events>')
        sys.exit(2)
    
    source = 'NULL'
    nevent = -1
    for opt, arg in opts:
        if opt == '-h':
            print('runsim.py -s <source_type> -n <number_of_events>')
            sys.exit()
        elif opt in ("-s", "--source"):
            source = arg
        elif opt in ("-n", "--nevent"):
            nevent = int(arg)

    # check for errors
    if source == 'NULL' or nevent == -1:
        print('runsim.py -s <source_type> -n <number_of_events>')
        sys.exit(2) 

    # convert source name to lower case
    source = source.lower()

    return source, nevent
#--------------------------------------------------------------------------------------------
def get_random_seed():
    
    # open the random seed storage file in the output directory
    seed_file = output_basedir + '/Random_Seed.last'
    
    if not os.path.exists(seed_file):
        # if it does not exist we start with this random seed
        ran_seed = 100000
    else:
        # else we read the latest used seed and add one
        fin = open(seed_file,'r')
        ran_seed = int(fin.read())
        fin.close()
        ran_seed = ran_seed+1

    # update the seed storage
    print('SEED = '+str(ran_seed))
    fout = open(seed_file,'w')
    fout.write(str(ran_seed))
    fout.close()
    #
    
    return ran_seed
#--------------------------------------------------------------------------------------------
def submit_script():
    cmd = 'qsub -W group_list=detrd -e logfiles -o logfiles -j eo -q long '+shell_script
    os.system(cmd)

#--------------------------------------------------------------------------------------------
# MAIN CODE

# interpret the command line arguments
source_name, numberOfEvents = parseArguments(sys.argv[1:])

# generate the random seed
ran_seed = get_random_seed()

# output structure and files
output_basename = source_name + "_"+ str(ran_seed)
output_root     = output_basedir+"/"+output_basename + ".root"

# macros and scripts
preinit_script = run_dir+'/preinit_'+output_basename+'.mac'
run_script     = run_dir+'/run_'+output_basename+'.mac'
shell_script   = run_dir+'/simu_'+output_basename+'.sh'

# generate the GEANT4 preinit script
make_G4preinit_script()

# generate the GEANT4 run script
make_G4run_script()

# generate run shell script
make_shell_script()

# submit the job to the Nikhef stoomboot cluster
# REMOVE IF NOT @ NIKHEF
submit_script()
