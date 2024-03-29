import pymysql.cursors
import common.setting as setting


class MySQLConnect:
    """This class is comprised of the methods which are related to DB connection"""

    def __init__(self) -> None:
        self.createConnection()

    def queryData(self, query) -> str:
        """
        This method retrieves data by query
        :param1 str query: sql line
        :return str: depends on what to retrieve if succeeds, return Null if fails
        """

        # check connection
        if not self.checkConnection():
            self.createConnection()

        # if passed go next
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
        self.connection.commit()  # connection is not autocommit by default.
        # So you must commit to save your changes. 데이터 crud시 transaction 생기는데 commit을 해야만 반영
        return result

    def checkConnection(self):
        # if connection is alive return True else false
        pass

    def createConnection(self):
        self.connection = pymysql.connect(
            host=setting.DB_HOST,
            user=setting.DB_USER,
            password=setting.DB_PASSWORD,
            database=setting.DB_DATABASE,
            cursorclass=pymysql.cursors.DictCursor,
        )
