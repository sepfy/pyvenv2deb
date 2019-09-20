# encoding: utf-8
import os
import json



entry_template = "\
#!/usr/bin/python3\n\
# -*- coding: utf-8 -*-\n\
import re\n\
import sys\n\
\n\
%s\n\
\n\
if __name__ == '__main__':\n\
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])\n\
    sys.exit(run_main())"

def write_entry_point(console_scripts, output_dir):

  # Parse the console scripts  
  scripts = console_scripts.split("=")
  entries = scripts[1].split(":")
  entry_point = entry_template % ("from"+entries[0]+" import "+entries[1])

  # Create folder by Linux command 
  os.system("mkdir -p " + output_dir)

  # Create a commnad with console_scripts
  fout = open(output_dir+scripts[0].strip(" "), "w")
  fout.write(entry_point)
  fout.close()
 
  # Change mode
  os.system("chmod 777 " + output_dir+scripts[0].strip(" "))


def generate_entry_points(input_file, output_dir):

  if os.path.exists(input_file) == False:
    return

  # Find console_scripts section.
  fin = open(input_file)
  for line in fin:
    if line.find("console_scripts") != -1:
      while True:
        console_scripts = fin.readline().strip("\n")
        if console_scripts.strip(" ") == "":
          break
        write_entry_point(console_scripts, output_dir+"usr/bin/")
  fin.close()


def get_depends(pkg_info_path):
  deps = ""
  fmeta = open(pkg_info_path+"/METADATA")
  for line in fmeta:
    if line.find("Requires-Dist") != -1:
      if len(line.split(" ")) < 4:
        deps += pyver+"-"+ line.split(" ")[1].strip("\n").strip(";").replace("_", "-").lower() + ", "
  deps = deps[:-2]
  fmeta.close()
  return deps

 
def copy_packages(pkg_info_path, pylib_inst_path):

  # Copy info package
  os.system("cp -r " + pkg_info_path + " " + pylib_inst_path)

  # Copy python package
  fin = open(pkg_info_path +  "/top_level.txt")
  for line in fin:
    pkg_path = venv_lib_path + line.strip("\n")
    #print(pkg_path)
    if os.path.exists(pkg_path):
      os.system("cp -r " + pkg_path + " " + pylib_inst_path)
    else:
      os.system("cp -r " + pkg_path + ".py " + pylib_inst_path)
  fin.close()



def generate_deb(pkg_info_path):

  pkg_name = pkg_info_path.split("/")[-1].split("-")[0].lower().replace("_", "-")

  # Get pip package version
  pre_ver = pkg_info_path.split("/")[-1].split("-")[1]
  version = pre_ver[0:pre_ver.find("dist")-1]

  # Generate deb name and output directory
  deb_name = pyver+"-"+pkg_name
  output_dir = "outputs/"+deb_name+"/"
  # Create basic foler
  os.system("mkdir -p " + output_dir + "/DEBIAN")
  if pyver == "python3":
    pylib_inst_path = output_dir + "/usr/lib/python3/dist-packages/"
  else:
    pylib_inst_path = output_dir + "/usr/lib/python2.7/dist-packages/"
  os.system("mkdir -p " + pylib_inst_path)


  # Get DEBIAN DEPS
  deps = get_depends(pkg_info_path)
  
  # Generate binary in /usr/bin
  generate_entry_points(pkg_info_path+"/entry_points.txt", output_dir)
   
  # Copy site-packages to dist-packages
  copy_packages(pkg_info_path, pylib_inst_path)
   

  os.system("echo 'Package: "+deb_name+"' > "+output_dir+ "/DEBIAN/control")
  os.system("echo 'Version: " + version + "' >> "+output_dir + "/DEBIAN/control") 
  os.system("echo 'Architecture: all' >> "+ output_dir + "/DEBIAN/control")
  os.system("echo 'Section: python' >> "+output_dir + "/DEBIAN/control")
  os.system("echo 'Priority: optional' >> "+output_dir + "/DEBIAN/control")
  os.system("echo 'maintainer: pyvenv2deb' >> "+output_dir + "/DEBIAN/control")
  os.system("echo 'Depends: "+deps+"' >> "+output_dir + "/DEBIAN/control")
  os.system("echo 'description: auto-gen package' >> "+output_dir + "/DEBIAN/control")
  

def process_pkg(pkg_name):
  for f in os.listdir(venv_lib_path):
    if f.split("-")[0] == pkg_name and f.find("info") != -1:
      pkg_info_path = venv_lib_path + f 
      generate_deb(pkg_info_path)

if __name__ == "__main__":
  #pyver = "python"
  pyver = "python3"
  venv_path = "venv"
  requirements = "requirements.txt"

  if pyver == "python3":
    venv_lib_path = venv_path+"/lib/python3.6/site-packages/"
  else:
    venv_lib_path = venv_path+"/lib/python2.7/site-packages/"
  f = open(requirements)
  for line in f:
    if line == "pkg-resources==0.0.0\n":
      continue
    pkg_name = line.split("==")[0]
    #print(pkg_name)
    process_pkg(pkg_name.replace("-", "_"))
  f.close()




