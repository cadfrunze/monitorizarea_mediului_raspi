from databases.db_access import DbAccess
from dotenv import load_dotenv
import os
import paramiko
import ast




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
    
    def run_script(self) -> dict | None:
        """
        Ruleaza scriptul de pe Raspberry Pi pentru a citi datele de la senzori
        """
        if self.client is None or not self.client.get_transport() or not self.client.get_transport().is_active():
            self.client = self.connect_raspi()
            if self.client is None:
                raise ConnectionError("lipa conex ssh")

        folder: str = self.__path
        script: str = "run_script.py"
        venv: str = "source venv/bin/activate"
        command: str = f"cd {folder} && {venv} && python {script}"
        stdin, stdout, stderr = self.client.exec_command(command)
        output: str = stdout.read().decode().strip()
        self.client.close()
        try:
            output_dict: dict = ast.literal_eval(output)
        except (SyntaxError, ValueError) as e:
            raise e
        else:
            self.client.close()
            return output_dict
    

        
