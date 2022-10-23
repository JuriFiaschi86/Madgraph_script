import os
import subprocess

def write_mg5_shell(model, process, output):
    
    
    current_dir = os.getcwd() + "/"
    lhapdf_dir = "/home/juri/LHAPDF/bin/lhapdf-config"
    
    #### Get LHAPDF dir automatically
    #command = "echo $LD_LIBRARY_PATH"
    #call = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    #(call_output, call_error) = call.communicate()
    #call_status = call.wait()
    #lhapdf_dir = call_output.decode("utf-8")
    #lhapdf_dir = lhapdf_dir[:-4] + "bin/lhapdf-config"
    
    #### Get LHAPDF dir automatically
    #command = "locate -b 'LHAPDF'"
    #call = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    #(call_output, call_error) = call.communicate()
    #call_status = call.wait()
    #lhapdf_dir = call_output.decode("utf-8").split()[0] + "/bin/lhapdf-config"
    
    #lhapdf_dir = "/srv/pheno_dir/tools/MG5_aMC_v2_8_2/HEPTools/lhapdf6_py3/bin/lhapdf-config"
    
    text = ""
    #text += "set lhapdf " + str(lhapdf_dir)
    text += "set lhapdf_py3 " + str(lhapdf_dir)
    text += "\n"
    text += "import model " + model
    text += "\n"
    text += "define su = uR uR~"
    text += "\n"
    text += "generate " + process
    text += "\n"
    text += "output " + output
    text += "\n"
    text += "quit"
    
    shell_file = open(current_dir + "mg5_shell.sh", "w")
    shell_file.write(text)
    shell_file.close()
