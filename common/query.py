import pymysql.cursors


class MySQLConnect:
    """This class is comprised of the methods which are related to DB connection"""

    def __init__(self) -> None:
        pass

    def queryData(self, query) -> str:
        """
        This method retrieves data by query
        :param1 str query: sql line
        :return str: depends on what to retrieve if succeeds, return Null if fails
        """
        connection = pymysql.connect(
            host="localhost",
            user="user1",
            password="rushhour04",
            database="rushhour",
            cursorclass=pymysql.cursors.DictCursor,
        )

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
            connection.commit()  # connection is not autocommit by default.
            # So you must commit to save your changes.

        return result
