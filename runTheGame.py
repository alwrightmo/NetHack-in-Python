from subprocess import call

#os.system("start /MAX %CD%\\runners\executor.bat")
call("start /MAX %CD%\\runners\executor.bat", shell=True)