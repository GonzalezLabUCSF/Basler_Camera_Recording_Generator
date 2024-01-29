import subprocess, os
directory=os.listdir()
# for file in directory:
#     if file[0:1]=="y":
#         print(file)
subprocess.Popen(["python","Cameras/acA1300-60gcAMZ_23801541_record_script.py"], shell=True)
subprocess.Popen(["python","Cameras/acA1300-60gcAMZ_23801561_record_script.py"], shell=True)