import pymysql.cursors
import common.setting as setting


class MySQLConnect:
    """This class is comprised of the methods which are related to DB connection"""

    def __init__(self) -> None:
        self.createConnection()

    def queryData(self, query: str) -> str:  # query data type is requried
        """
        This method retrieves data by query
        :param1 str query: sql line
        :return str: depends on what to retrieve if succeeds, return Null if fails
        """

        if not self.checkConnection():
            self.createConnection()

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()

        self.connection.commit()
        return result

    def checkConnection(self) -> bool:
        """This Method checks a MySQL connection.
        Return True if connection is active otherwise False
        """
        if self.connection.ping(True):
            return True
        else:
            return False

    def createConnection(self):
        """This method creates a connection."""
        self.connection = pymysql.connect(
            host=setting.DB_HOST,
            user=setting.DB_USER,
            password=setting.DB_PASSWORD,
            database=setting.DB_DATABASE,
            cursorclass=pymysql.cursors.DictCursor,
        )
