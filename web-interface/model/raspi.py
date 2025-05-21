from databases.db_access import DbAccess
from dotenv import load_dotenv
import os
import paramiko




def get_info_raspi() -> dict[str, str]:
    """
    Returneaza adresa IP/Ssid de la Raspberry Pi
    """
    db: DbAccess = DbAccess()
    info: dict[str, str] = dict()
    info["ip"] = db.get_ip()
    info["ssid"] = db.get_ssid()
    return info


class RaspiSsh:
    """
    Clasa RaspiSsh este responsabila pentru gestionarea conexiunii SSH cu Raspberry Pi si....
    rularea scriptului pentru a citi date de la senzori in timp real.
    """
    def __init__(self):
        self.__info: dict[str, str] = get_info_raspi()
        load_dotenv()
        self.__user: str = os.getenv("USER_RASPI")
        self.__password: str = os.getenv("PASS_RASPI")
        self.__path: str = os.getenv("PATH_SCRIPT")
        self.client: paramiko.SSHClient | None = self.connect_raspi()

    def connect_raspi(self) -> None | paramiko.SSHClient:
        """
        Conecteaza la Raspberry Pi prin SSH
        """
        client: paramiko.SSHClient = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=self.__info["ip"], username=self.__user, password=self.__password)
            
        except paramiko.SSHException as e:
            raise e
        else: 
            return client
    
    def run_script(self) -> None:
        """
        Ruleaza scriptul de pe Raspberry Pi pentru a citi datele de la senzori
        """
        if self.client is None:
            self.connect_raspi()
        # print(self.__path)
        folder: str = self.__path
        script: str = "main.py"
        venv: str = "source venv/bin/activate && "
        command: str = f"cd {folder} && {venv} nohup python {script} > log.txt 2>&1 & echo $! > pid.txt"
        # print(command)
        stdin, stdout, stderr = self.client.exec_command(command)
        # print(stdout.read().decode())
        # print(stderr.read().decode())
    
    def stop_script(self) -> None:
        """
        Opreste scriptul de pe Raspberry Pi
        """
        if self.client is None:
            self.connect_raspi()
        command: str = f"cd {self.__path} && kill $(cat pid.txt) && rm pid.txt"
        stdin, stdout, stderr = self.client.exec_command(command)
        # print(stdout.read().decode())
        # print(stderr.read().decode())
        self.client.close()
        
