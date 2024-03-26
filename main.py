from fastapi import FastAPI, Request
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
5. validate the authorization defined in request header
"""


@app.post("/api/v1/login")
async def userLogin(usr_login: Login, request: Request) -> dict:
    """This is the main function that gives an proper response when requested
    :param1 str user_login: instance for Login Class
    :param2 str request: instance for Request Class,
    pre-built function(import from fastapi) mainly handles the request header
    :return dict: return response in json format
    """
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

    # [Feature 1] ID : a-zA-Z, length: less than 15 characters
    def userIdCheck(user_id) -> bool:
        """This function checks the user-id in conditions
        :param str user_id: intake user_id
        :return bool: True if passsed, vice versa
        """
        if user_id is None:  # null handler
            return False

        id_check = re.findall("[a-zA-Z]", user_id)
        if len(user_id) == len(id_check) and len(user_id) <= 15:
            return True
        else:
            return False

    # [Feature 2] Password : a-zA-Z0-9 + one special character length,
    # more than 8, less than 20 characters
    def userPWCheck(user_pw) -> bool:
        """This function checks the user-id in conditions
        :param str user_pw: intake user_pw
        :return bool: True if passsed, vice versa
        """
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

    # [Feature 3] checks if the given credential equates to the data in DB
    def credentialCheck(user_id, user_pw) -> str:
        """This function connects MySQL and check if the params given are corresponding
        to the data in DB
        :param1 str user_id: intake user_pw
        :param2 str user_id: intake user_pw
        :return str: return Room_code if successed, return Null if failed
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
                sql = 'SELECT room_code FROM rushhour.users where user_id = "{id}" and user_pw = "{pw}"; '.format(
                    id=user_id, pw=user_pw
                )
                cursor.execute(sql)
                result = cursor.fetchone()
            connection.commit()  # connection is not autocommit by default.
            # So you must commit to save your changes.

        return result

    # final
    """return a final result when userLogin function executes"""
    while True:
        try:
            if (
                headers.get("Authorization") == "test"
            ):  # [Function 5] validate the authorization defined in request header
                if userIdCheck(usr_login.user_id) and userPWCheck(
                    usr_login.user_pw
                ):  # [Function 1, 2] check userID, userPw credential in regulations
                    query = credentialCheck(
                        usr_login.user_id, usr_login.user_pw
                    )  # [Function 3] check the given credential with DB
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
        except (RuntimeError, TypeError):  # [Function 4] check runtime error
            fail_format["status"] = "700"
            fail_format["statusMessage"] = "Runtime Error"
            return fail_format
