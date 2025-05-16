import subprocess
proc = subprocess.Popen([BME_BSEC], stdout=subprocess.PIPE)
for line in iter(proc.stdout.readline, ''):
        print(line)