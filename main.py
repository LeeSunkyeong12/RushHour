from fastapi import FastAPI, Header, Request
from pydantic import BaseModel
import re
import pymysql.cursors

app = FastAPI()


class Login(BaseModel):
    user_id: str
    user_pw: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


"""
API handler that functions the followings;
1. validate the user id in accordance with regulations
2. validate the user password in accordance with regulations
3. checks if the given credential equates with the data in DB
4. handles the HTTP errors
"""


@app.post("/api/v1/login")
async def usr_login(usr_login: Login, request: Request):
    headers = request.headers

    success_format = {
        "ifLogin": True,
        "roomCode": "rushhour",
        "status": "200",
        "statusMessage": "Success",
    }

    fail_format = {
        "ifLogin": False,
        "status": "500",
        "statusMessage": "Invalid Format",
    }

    # 1. ID : a-zA-Z, length: less than 15 characters
    def userIdCheck(user_id) -> bool:
        if user_id is None:  # null handler
            return False

        id_check = re.findall("[a-zA-Z]", user_id)
        if len(user_id) == len(id_check) and len(user_id) <= 15:
            return True
        else:
            return False

    # 2. Password : a-zA-Z0-9 + one special character length, more than 8, less than 20 characters
    def userPWCheck(user_pw) -> bool:
        if user_pw is None:  # null handler
            return False

        pw_check = re.findall("[a-zA-Z0-9_\W]", user_pw)
        if (
            len(user_pw) == len(pw_check)  # matches a regulation
            and len(re.findall("[_\W]", user_pw)) == 1  # special character == 1
            and len(user_pw) >= 8
            and len(user_pw) <= 20  # length >= 8 and length <= 20
        ):
            return True
        else:
            return False

    # 3. checks if the given credential equates to the data in DB
    def credentialCheck(user_id, user_pw):
        connection = pymysql.connect(
            host="localhost",
            user="user1",
            password="rushhour04",
            database="rushhour",
            cursorclass=pymysql.cursors.DictCursor,
        )

        with connection:
            with connection.cursor() as cursor:
                sql = 'SELECT room_code FROM rushhour.users where user_id = "{id}" and user_pw = "{pw}"; '.format(
                    id=user_id, pw=user_pw
                )
                cursor.execute(sql)
                result = cursor.fetchone()
            connection.commit()  # connection is not autocommit by default. So you must commit to save your changes.

        return result

    # final
    while True:
        try:
            if headers.get("Authorization") == "test":
                if userIdCheck(usr_login.user_id) and userPWCheck(usr_login.user_pw):
                    query = credentialCheck(usr_login.user_id, usr_login.user_pw)

                    if query is None:
                        fail_format["status"] = "400"
                        fail_format["statusMessage"] = "Unauthorized"
                        return fail_format

                    else:
                        success_format["roomCode"] = query["room_code"]
                        return success_format

                else:
                    fail_format["status"] = "500"
                    fail_format["statusMessage"] = "Invalid Format"
                    return fail_format
            else:
                fail_format["status"] = "400"
                fail_format["statusMessage"] = "Unauthorized"
                return fail_format
        except (RuntimeError, TypeError):
            fail_format["status"] = "700"
            fail_format["statusMessage"] = "Runtime Error"
            return fail_format
