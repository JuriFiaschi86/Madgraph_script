#! /usr/bin/python3

import os

#def write_madevent_shell(process):
def write_madevent_shell():
    
    current_dir = os.getcwd() + "/"
    
    text = ""
    text += "set automatic_html_opening False"
    text += "\n"
    #text += "launch " + process + " --multicore --nb_core=8"
    text += "launch --multicore --nb_core=8"
    text += "\n"
    text += " shower=OFF"
    text += "\n"
    text += " detector=OFF"
    text += "\n"
    text += " analysis=OFF"
    text += "\n"
    text += "quit"    
    
    shell_file = open(current_dir + "madevent_shell.sh", "w")
    shell_file.write(text)
    shell_file.close()
