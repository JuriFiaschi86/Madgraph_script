#! /usr/bin/python3

import os
import shutil
import re
#import sys
#import glob
import subprocess
#import datetime
import pandas
#import argparse
#import math

from write_MG5_shell import write_mg5_shell
from write_param_card import write_param_card
from write_run_card import write_run_card
from write_madevent_shell import write_madevent_shell
from contour_plot import contour_plot
#from analyse_lhco import read_lhco
#from analyse_lhco import events_analysis
#from write_scan_summary import scan_summary
#from plot_results import plot_results



class params_masses():
    ### reference masses as in the default slha files
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
    scale_choice = -1 ### fixed scale
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
#input_slha = current_dir + "param_card_wino.dat"

process = "p p > su su QED=99 QCD=99"
#process = "p p > su su QED=99 QCD=0"


#####################
### SCAN SETTINGS ###
#####################

flag_generate_events = True

flag_analysis = False


masses = params_masses()

### decouple gluino
masses.m_gl = 1.00000000E+04

### run card settings
run = params_run()
run.lhapdfid = 27000 ### MSHT20lo_as130
run.nevents = 10000
run.energy = 13600
#run.scale = masses.m_sup_R


### squark range
m_sup_R_min = 500
m_sup_R_max = 2000
m_sup_R_bin = 150

### electroweakinos range
m_ewk_min = 500
m_ewk_max = 2500
m_ewk_bin = 200
### I will set only the lightest neutralino mass

m_sup_R_list = list(range(m_sup_R_min, m_sup_R_max + m_sup_R_bin, m_sup_R_bin))
m_ewk_list = list(range(m_ewk_min, m_ewk_max + m_ewk_bin, m_ewk_bin))

##################
### START LOOP ###
##################


if (flag_generate_events):

    for m_sup_R_value in m_sup_R_list:
        for m_ewk_value in m_ewk_list:
            
            ### up squark right
            masses.m_sup_R = m_sup_R_value
            ### neutralino 1
            masses.m_chi10 = m_ewk_value
            #### chargino 1
            #masses.m_chi1p = m_ewk_value
            
            run.scale = masses.m_sup_R
            
            output_folder = current_dir + "temp/"
            
            
            
            if not(os.path.exists(output_folder)):
                os.mkdir(output_folder)
            else:
                shutil.rmtree(output_folder)
                os.mkdir(output_folder)
            
            
            #########################
            #### GENERATE PROCESS ###
            #########################
            
            #if not(os.path.exists(output_folder)):
                #os.mkdir(output_folder)

                
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

            ###################
            ### WRITE CARDS ###
            ###################

            write_param_card(input_slha, output_folder, masses)
            
            write_run_card(output_folder, run)


            ####################
            ### RUN MADEVENT ###
            ####################

            if os.path.exists(current_dir + "madevent_shell.sh"):
                os.remove(current_dir + "madevent_shell.sh")

            #write_madevent_shell(process_name)
            write_madevent_shell()

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
                
                
            #############
            ### CLEAN ###
            #############
            
            ### I am going to keep only the banner file which contains all the info I need.
            ### The rest is deleted as it takes too much space.
            
            temp_folder = output_folder
            if (process == "p p > su su QED=99 QCD=99"): process_name = "full"
            elif (process == "p p > su su QED=99 QCD=0"): process_name = "qed"
            
            process_name += "_msq_" + str(int(masses.m_sup_R)) + "_mchi10_" + str(int(masses.m_chi10))        
            
            output_folder = current_dir + "sq_sq_" + str(int(run.energy)) + "/"
            if not(os.path.exists(output_folder)):
                os.mkdir(output_folder)
            #output_folder = current_dir + "sq_sq_" + str(int(run.energy)) + "/" + process_name + "/"
            
            banner_file_name = process_name + ".txt"
            shutil.move(temp_folder + "Events/run_01/run_01_tag_1_banner.txt", output_folder + banner_file_name)
            
            shutil.rmtree(temp_folder)
        

################
### ANALYSIS ###
################

####
m_sup_R_list = list(range(m_sup_R_min, m_sup_R_max + m_sup_R_bin, m_sup_R_bin))
m_ewk_list = list(range(m_ewk_min, m_ewk_max + m_ewk_bin, m_ewk_bin))
####

#flag_analysis = False
#flag_analysis = True

if (flag_analysis):

    XS_QED_QCD = pandas.DataFrame(columns=["msq [GeV]", "mchi10 [GeV]", "xs [pb]"])
    XS_QED = pandas.DataFrame(columns=["msq [GeV]", "mchi10 [GeV]", "xs [pb]"])
    
    for m_sup_R_value in m_sup_R_list:
        for m_ewk_value in m_ewk_list:
            
            ### up squark right
            masses.m_sup_R = m_sup_R_value
            ### neutralino 1
            masses.m_chi10 = m_ewk_value
            
            ####################
            ### READ BANNERS ###
            ####################
            
            ### QED + QCD
            process_name = "full"
            process_name += "_msq_" + str(int(masses.m_sup_R)) + "_mchi10_" + str(int(masses.m_chi10))        
            output_folder = current_dir + "sq_sq_" + str(int(run.energy)) + "/"
            banner_file_name = process_name + ".txt"
            
            banner_file = open(output_folder + banner_file_name, "r")
            banner_text = banner_file.read()
            banner_file.close()
            
            xs_line = re.findall("^.*Integrated weight.*$", banner_text, re.MULTILINE)[0]            
            xs = float(xs_line.split()[5]) ### XS in pb
            
            XS_QED_QCD.loc[len(XS_QED_QCD.index)] = [masses.m_sup_R, masses.m_chi10, xs]
            
            ### QED
            process_name = "qed"
            process_name += "_msq_" + str(int(masses.m_sup_R)) + "_mchi10_" + str(int(masses.m_chi10))        
            output_folder = current_dir + "sq_sq_" + str(int(run.energy)) + "/"
            banner_file_name = process_name + ".txt"
            
            banner_file = open(output_folder + banner_file_name, "r")
            banner_text = banner_file.read()
            banner_file.close()
            
            xs_line = re.findall("^.*Integrated weight.*$", banner_text, re.MULTILINE)[0]            
            xs = float(xs_line.split()[5]) ### XS in pb
            
            XS_QED.loc[len(XS_QED.index)] = [masses.m_sup_R, masses.m_chi10, xs]
            
    
    
    
    
    
    
    
    
    ### read banners
    
    print(XS_QED_QCD)
    print(XS_QED)
    
    plot_file_name = "contour_test.pdf"
    plot_file_path = current_dir + plot_file_name
    
    columns_name = ["msq [GeV]", "mchi10 [GeV]", "xs [pb]"]
    contour_plot(XS_QED_QCD, columns_name, plot_file_path)
    
    
    
    
    #import matplotlib.pyplot as plt
    #import numpy as np

    #fig = plt.figure(figsize=(6,5))
    #left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
    #ax = fig.add_axes([left, bottom, width, height]) 

    #start, stop, n_values = -8, 8, 800

    #x_vals = np.linspace(start, stop, n_values)
    #y_vals = np.linspace(start, stop, n_values)
    #X, Y = np.meshgrid(x_vals, y_vals)


    #Z = np.sqrt(X**2 + Y**2)

    #cp = plt.contourf(X, Y, Z)
    #plt.colorbar(cp)

    #ax.set_title('Contour Plot')
    #ax.set_xlabel('x (cm)')
    #ax.set_ylabel('y (cm)')
    #plt.show()





















                
