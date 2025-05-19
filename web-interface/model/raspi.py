from databases.db_access import DbAccess

def get_info_raspi() -> dict[str, str]:
    """
    Returneaza adresa IP/Ssid de la Raspberry Pi
    """
    db = DbAccess()
    info: dict[str, str] = dict()
    info["ip"] = db.get_ip()
    info["ssid"] = db.get_ssid()
    return info
