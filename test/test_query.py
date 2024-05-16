import common.query as sql

# import sys
# import os

# sys.path.append(os.getcwd())

sqlQuery = sql.MySQLConnect()


def test_query():
    assert sqlQuery.queryData(
        'Select room_code from rushhour.users where user_id = "rushhour";'
    ) == {"room_code": "rm01"}
