from databases.db_access import DbAccess


class AppService:
    """
    Clasa AppService este responsabila pentru gestionarea/cerintele aplicatiei.
    """
    def __init__(self):
        self.__db_access: DbAccess = DbAccess()