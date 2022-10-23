#! /usr/bin/python3

import re
    
def write_param(text, params):
    
    ### Write number of events
    events_line_old = re.findall("^.*nevents.*$", text, re.MULTILINE)[0]
    events_line_new = "  " + str(params.nevents) + events_line_old[7:len(events_line_old)]
    text = text.replace(events_line_old, events_line_new)
    
    ### Write energy
    energy_line_old = re.findall("^.*ebeam1.*$", text, re.MULTILINE)[0]
    energy_line_new = "     " + str(params.energy / 2) + energy_line_old[11:len(energy_line_old)]
    text = text.replace(energy_line_old, energy_line_new)
    energy_line_old = re.findall("^.*ebeam2.*$", text, re.MULTILINE)[0]
    energy_line_new = "     " + str(params.energy / 2) + energy_line_old[11:len(energy_line_old)]
    text = text.replace(energy_line_old, energy_line_new)
    
    ### Write PDF
    pdlabel_line_old = re.findall("^.*pdlabel.*$", text, re.MULTILINE)[0]
    pdlabel_line_new = "     lhapdf" + pdlabel_line_old[12:len(pdlabel_line_old)]
    text = text.replace(pdlabel_line_old, pdlabel_line_new)
    lhaid_line_old = re.findall("^.*lhaid.*$", text, re.MULTILINE)[0]
    lhaid_line_new = "     " + str(params.lhapdfid) + lhaid_line_old[11:len(pdlabel_line_old)] ### corresponds to NNPDF30_lo_as_0118
    text = text.replace(lhaid_line_old, lhaid_line_new)

    ### Write scale
    scale_line_old = re.findall("^.*fixed_ren_scale.*$", text, re.MULTILINE)[0]
    scale_line_new = " True = fixed_ren_scale  ! if .true. use fixed ren scale"
    text = text.replace(scale_line_old, scale_line_new)
    scale_line_old = re.findall("^.*fixed_fac_scale.*$", text, re.MULTILINE)[0]
    scale_line_new = " True = fixed_fac_scale  ! if .true. use fixed fac scale"
    text = text.replace(scale_line_old, scale_line_new)
    scale_line_old = re.findall("^.*91.188  = scale.*$", text, re.MULTILINE)[0]
    scale_line_new = " " + str(params.scale) + "  = scale            ! fixed ren scale"
    text = text.replace(scale_line_old, scale_line_new)
    scale_line_old = re.findall("^.*91.188  = dsqrt_q2fact1.*$", text, re.MULTILINE)[0]
    scale_line_new = " " + str(params.scale) + "  = dsqrt_q2fact1    ! fixed fact scale for pdf1"
    text = text.replace(scale_line_old, scale_line_new)
    scale_line_old = re.findall("^.*91.188  = dsqrt_q2fact2.*$", text, re.MULTILINE)[0]
    scale_line_new = " " + str(params.scale) + "  = dsqrt_q2fact2    ! fixed fact scale for pdf2"
    text = text.replace(scale_line_old, scale_line_new)
    scale_line_old = re.findall("^.*dynamical_scale_choice.*$", text, re.MULTILINE)[0]
    scale_line_new = "  " + str(params.scale_choice) + scale_line_old[3:len(scale_line_old)] ### corresponds to user defined ren/fact scales choice
    text = text.replace(scale_line_old, scale_line_new) 
    
    return text
    
def write_run_card(path, run):
    
    ### Open and read default param card
    run_template = open(path + "Cards/run_card_default.dat", "r")
    text = run_template.read()
    run_template.close()
    
    text = write_param(text, run)
    
    ### Write run card file
    run_new = open(path + "Cards/run_card.dat", "w")
    run_new.write(text)
    run_new.close()
