from settingsConfig import settingsConfig
import psycopg2


class DatabaseConnection(object):
    def __init__(self, __settings):
        self.__settings = __settings
        self.dbConnection = None

    def __enter__(self):
        self.dbConnection = psycopg2.connect(**self.__settings)
        self.dbConnection.set_session(autocommit=True)
        self.dbCursor = self.dbConnection.cursor()
        return self

    def __exit__(self, exception_type, exception_val, trace):
        try:
            self.dbCursor.close()
            self.dbConnection.close()
        except AttributeError:
            return True

    def execute(self, sql, data=None):
        if data is not None:
            self.dbCursor.execute(sql, data)
        else:
            self.dbCursor.execute(sql)
        self.dbConnection.commit()

    def getRows(self, sql, data=None):
        self.dbCursor.execute(sql)
        return self.dbCursor.fetchall()


databaseSession = DatabaseConnection(settingsConfig.DatabaseSettings)
