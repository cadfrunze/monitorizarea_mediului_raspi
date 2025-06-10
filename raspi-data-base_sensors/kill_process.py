import os
import subprocess






def kill_process(port:int)->None:
    try:
        result = subprocess.run(f"lsof -i :{port} -t", shell=True, capture_output=True, text=True)
        pids = result.stdout.strip().split("\n")

        for pid in pids:
            if pid.isdigit(): 
                os.system(f"kill -9 {pid}")
    except Exception as e:
        raise e


kill_process(5000)
