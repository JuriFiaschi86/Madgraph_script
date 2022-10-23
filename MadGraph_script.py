#! /usr/bin/python3

import os
import shutil
#import re
#import sys
#import glob
import subprocess
#import datetime
#import pandas
#import argparse
#import math

from write_MG5_shell import write_mg5_shell
from write_param_card import write_param_card
from write_run_card import write_run_card
from write_madevent_shell import write_madevent_shell
#from analyse_lhco import read_lhco
#from analyse_lhco import events_analysis
#from write_scan_summary import scan_summary
#from plot_results import plot_results



class params_masses():
    ### right up squark
    m_sup_R = 4.88389928E+03
    ### neutralino 1
    m_chi10 = 1.00568552E+02
    ### chargino 1
    m_chi1p = 1.48190189E+03
    ### gluino
    m_gl = 4.96920633E+03

class params_run():
    ### number of events
    nevents = 100
    ### c.o.m. energy
    energy = 13600
    ### LHAPDF PDF set id
    lhapdfid = 27000 # MSHT20lo_as130
    ### ren/fact scale choice
    scale_choice = -1
    ### scale
    scale =  91.188
    



#######################
### SET DIRECTORIES ###
#######################

current_dir = os.getcwd() + "/"

### Get MG5_aNLO path
command = "locate -b 'MG5_aMC_v'"
call = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
(call_output, call_error) = call.communicate()
call_status = call.wait()
path_Madgraph = call_output.decode("utf-8").split()[0] + "/"

#path_Madgraph = "/srv/pheno_dir/tools/MG5_aMC_v2_8_2/"


model = "MSSM_SLHA2-full"

input_slha = current_dir + "param_card_bino.dat"

process = "p p > su su QED=99 QCD=99"
#process = "p p > su su QED=99 QCD=0"


process_name = "sq_sq_13600_GeV_full"

#process_path = path_Madgraph + process_name + "/"
output_folder = current_dir + process_name + "/"




#########################
#### GENERATE PROCESS ###
#########################
if not(os.path.exists(output_folder)):
    os.mkdir(output_folder)

### Write MG5 shell script
write_mg5_shell(model, process, output_folder)

### Run MG5
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)

os.chdir(path_Madgraph)
command = "./bin/mg5_aMC " + current_dir + "mg5_shell.sh"
os.system(command)
os.chdir(current_dir)

#### Copy setscale.f
#if os.path.exists(output_folder + "SubProcesses/setscales.f"):
    #os.remove(output_folder + "SubProcesses/setscales.f")
#shutil.copy2(current_dir + "setscales.f", output_folder + "SubProcesses/")




#########################
#### WRITE PARAM CARD ###
#########################


masses = params_masses()

#### test point
### up squark right
masses.m_sup_R = 5.00000000E+02
### neutralino 1
masses.m_chi10 = 5.00000000E+02
#### chargino 1
#masses.m_chi1p = 5.00000000E+02
## chargino 1
masses.m_gl = 1.00000000E+04



write_param_card(input_slha, output_folder, masses)


######################
### RUN PARAM CARD ###
######################

run = params_run()
run.lhapdfid = 27000
run.nevents = 10000
run.energy = 13600
run.scale = masses.m_sup_R

write_run_card(output_folder, run)


####################
### RUN MADEVENT ###
####################

if os.path.exists(current_dir + "madevent_shell.sh"):
    os.remove(current_dir + "madevent_shell.sh")

write_madevent_shell(process_name)

### Delete RunWeb if exists
if os.path.exists(output_folder + "RunWeb"):
    os.remove(output_folder + "RunWeb")

#### Begin time count
#start = datetime.datetime.now()

### Generate events
os.chdir(output_folder)
command = "./bin/madevent " + current_dir + "madevent_shell.sh"
os.system(command)
os.chdir(current_dir)

#### End time count
#end = datetime.datetime.now()
#elapsed_time = end - start

### Delete RunWeb if exists
if os.path.exists(output_folder + "RunWeb"):
    os.remove(output_folder + "RunWeb")










#######################
#### START THE LOOP ###
#######################

#mZpr_list = list(range(mZpr_min, mZpr_max + mZpr_bin, mZpr_bin))
#mDM_list = list(range(mDM_min, mDM_max + mDM_bin, mDM_bin))

#for mZpr in mZpr_list:
    #for mDM in mDM_list:
    
        ##if (2*mDM > mZpr): continue ### skip points with off-shell Z' decay into DM
        #if (((mDM > 0.5*mZpr + 100) or (mDM < 0.5*mZpr - 150)) and (mZpr < 2000)): continue ### skip points far from the on-shell limit
        #if ((mZpr >= 2000) and (mDM > 0.5*mZpr)): continue ### for sufficiently heavy Zpr compute also small DM points, but do not go above on-shell limit
    
        #masses.MY1 = mZpr
        #masses.MXd = mDM
        
        #print("\n")
        #print("###########################################")
        #print("Analysing mZpr = " + str(mZpr) + " & mDM = " + str(mDM))
        #print("###########################################")
        
        #parameter_space_point = "psp_mZpr_" + str(masses.MY1) + "_mDM_" + str(masses.MXd)
        
        #output_folder_events_lhco = current_dir + process_name + "_Events/"
        #lhco_filename = "events_" + parameter_space_point + ".lhco"
        #lhco_file_path = output_folder_events_lhco + lhco_filename
        
        #if not((flag_generate_events) or (os.path.exists(process_path + "Events/" + parameter_space_point)) or (os.path.exists(lhco_file_path))):
            #sys.exit("The events for this parameter space point have not been generated.\nSwitch on 'flag_generate_events' to generate the events\n")
        
        #if flag_generate_events:
            
            #########################
            #### WRITE PARAM CARD ###
            #########################
            
            #write_param_card(process_path, couplings, masses)
            
            #######################
            #### RUN PARAM CARD ###
            #######################

            #write_run_card(process_path, run)
            
            #####################
            #### RUN MADEVENT ###
            #####################

            #if os.path.exists(current_dir + "madevent_shell.sh"):
                #os.remove(current_dir + "madevent_shell.sh")

            #write_madevent_shell(parameter_space_point)

            #### Delete RunWeb if exists
            #if os.path.exists(process_path + "RunWeb"):
                #os.remove(process_path + "RunWeb")

            #### Begin time count
            #start = datetime.datetime.now()

            #### Generate events
            #os.chdir(process_path)
            #command = "./bin/madevent " + current_dir + "madevent_shell.sh"
            #os.system(command)
            #os.chdir(current_dir)

            #### End time count
            #end = datetime.datetime.now()
            #elapsed_time = end - start

            #### Delete RunWeb if exists
            #if os.path.exists(process_path + "RunWeb"):
                #os.remove(process_path + "RunWeb")

        ###############################
        #### CONVERT DELPHES OUTPUT ###
        ###############################
        
        #### If the lhco file does not exist already, then create one looking for the root file
        #if not(os.path.exists(lhco_file_path)):
        
            #### Get latest .root event file
            #root_file_list = sorted(glob.glob(process_path + "Events/" + parameter_space_point + "/*.root"))
            #last_root_file = root_file_list[len(root_file_list)-1]
            
            #if not(os.path.exists(output_folder_events_lhco)):
                #os.mkdir(output_folder_events_lhco)
            #command = path_Madgraph + "Delphes/root2lhco " + last_root_file + " " + lhco_file_path
            #os.system(command)
                
                
                
                
