#! /usr/bin/python3

import re

def write_mass(text, param, value):
    line_old = re.findall("^.*" + param + ".*$", text, re.MULTILINE)[0]    
    line_new = "      " + line_old.split()[0] + " " + "{:.6E}".format(value) + " " + line_old.split()[2] + " " + line_old.split()[3]
    text = text.replace(line_old, line_new)
    return text

def write_coupling(text, param, value):
    line_old = re.findall("^.*" + param + ".*$", text, re.MULTILINE)[0]
    line_new = line_old[0:6] + "{:.6E}".format(value) + line_old[18:len(line_old)]
    text = text.replace(line_old, line_new)
    return text

def write_width(text, param, value):
    line_old = re.findall("^.*" + param + ".*$", text, re.MULTILINE)[0]
    if ((type(value) == int) or (type(value) == float)):
        line_new = line_old.split()[0] + " " + line_old.split()[1] + " " + "{:.6E}".format(value)
    elif (type(value) == str):
        line_new = line_old.split()[0] + " " + line_old.split()[1] + " " + value
    text = text.replace(line_old, line_new)
    return text
    
#def write_param_card(path, couplings, masses):
    
    #### Open and read default param card
    #param_template = open(path + "Cards/param_card_default.dat", "r")
    #text = param_template.read()
    #param_template.close()
    
    #### Write masses
    #text = write_mass(text, "MXr", masses.MXr)
    #text = write_mass(text, "MXc", masses.MXc)
    #text = write_mass(text, "MXd", masses.MXd)
    #text = write_mass(text, "MY0", masses.MY0)
    #text = write_mass(text, "MY1", masses.MY1)
    
    #### Write widths
    #text = write_width(text, "DECAY 9000008", masses.WY0)
    #text = write_width(text, "DECAY 9000009", masses.WY1)
    
    #### Write couplings
    #text = write_coupling(text, "gSXr", couplings.gSXr)
    #text = write_coupling(text, "gSXc", couplings.gSXc)
    #text = write_coupling(text, "gSXd", couplings.gSXd)
    #text = write_coupling(text, "gSd11", couplings.gSd11)
    #text = write_coupling(text, "gSu11", couplings.gSu11)
    #text = write_coupling(text, "gSd22", couplings.gSd22)
    #text = write_coupling(text, "gSu22", couplings.gSu22)
    #text = write_coupling(text, "gSd33", couplings.gSd33)
    #text = write_coupling(text, "gSu33", couplings.gSu33)
    #text = write_coupling(text, "gSg", couplings.gSg)
    #text = write_coupling(text, "gPXd", couplings.gPXd)
    #text = write_coupling(text, "gPd11", couplings.gPd11)
    #text = write_coupling(text, "gPu11", couplings.gPu11)
    #text = write_coupling(text, "gPd22", couplings.gPd22)
    #text = write_coupling(text, "gPu22", couplings.gPu22)
    #text = write_coupling(text, "gPd33", couplings.gPd33)
    #text = write_coupling(text, "gPu33", couplings.gPu33)
    #text = write_coupling(text, "gPg", couplings.gPg)
    #text = write_coupling(text, "gVXc", couplings.gVXc)
    #text = write_coupling(text, "gVXd", couplings.gVXd)
    #text = write_coupling(text, "gVd11", couplings.gVd11)
    #text = write_coupling(text, "gVu11", couplings.gVu11)
    #text = write_coupling(text, "gVd22", couplings.gVd22)
    #text = write_coupling(text, "gVu22", couplings.gVu22)
    #text = write_coupling(text, "gVd33", couplings.gVd33)
    #text = write_coupling(text, "gVu33", couplings.gVu33)
    #text = write_coupling(text, "gAXd", couplings.gAXd)
    #text = write_coupling(text, "gAd11", couplings.gAd11)
    #text = write_coupling(text, "gAu11", couplings.gAu11)
    #text = write_coupling(text, "gAd22", couplings.gAd22)
    #text = write_coupling(text, "gAu22", couplings.gAu22)
    #text = write_coupling(text, "gAd33", couplings.gAd33)
    #text = write_coupling(text, "gAu33", couplings.gAu33)
    
    #### Write param card file
    #param_new = open(path + "Cards/param_card.dat", "w")
    #param_new.write(text)
    #param_new.close()


def write_param_card(input_slha, path, masses):
    
    ### Open and read default param card
    param_template = open(input_slha, "r")
    text = param_template.read()
    param_template.close()
    
    ### Write masses
    text = write_mass(text, "~u_r", masses.m_sup_R)
    text = write_mass(text, "~chi_10", masses.m_chi10)
    #text = write_mass(text, "~chi_1+", masses.m_chi1p)
    text = write_mass(text, "~g", masses.m_gl)
    
    ### Write param card file
    param_new = open(path + "Cards/param_card.dat", "w")
    param_new.write(text)
    param_new.close()
