from fastapi import FastAPI, Request
from pydantic import BaseModel
import re
import common.query as sql
import common.httperror as httperror

app = FastAPI()


class Login(BaseModel):
    user_id: str
    user_pw: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


"""
Login API handler that functions the followings;
1. validate the authorization defined in request header
2. validate the user id in accordance with regulations
   : a-zA-Z, length: less than 15 characters
3. validate the user password in accordance with regulations
   : a-zA-Z0-9 + one special character length,
    more than 8, less than 20 characters
4. checks if the given credential equates with the data in DB
5. handles the HTTP errors
"""


@app.post("/api/v1/login")
async def userLogin(usr_login: Login, request: Request) -> dict:
    """This is the main function that gives an proper response when requested
    :param1 str user_login: instance for Login Class
    :param2 str request: instance for Request Class,
    pre-built function(import from fastapi) mainly handles the request header
    :return dict: return response in json format
    """

    # header caller
    headers = request.headers

    # query caller
    login_query = sql.MySQLConnect()
    find_id_pw_query = """SELECT room_code FROM rushhour.users
    where user_id = "{id}" and user_pw = "{pw}"; """.format(
        id=usr_login.user_id, pw=usr_login.user_pw
    )

    # Common Error Check
    check_status = httperror.HttpCommonError()

    # id, pw check
    id_check = re.findall("[a-zA-Z]", usr_login.user_id)
    pw_check = re.findall("[a-zA-Z0-9_\W]", usr_login.user_pw)

    # [Function 5] handles the HTTP errors
    try:
        # [Feature 1] validate the authorization defined in request header
        if headers.get("Authorization") == "test":
            if len(usr_login.user_id) == 0 or len(usr_login.user_pw) == 0:
                return check_status.httpSignInStatus(500)  # no input
            else:  # [Function 2, 3] check userID, userPw credential in regulations
                if (
                    len(usr_login.user_id) == len(id_check)
                    and len(usr_login.user_id) <= 15
                ) and (
                    len(usr_login.user_pw) == len(pw_check)
                    and len(re.findall("[_\W]", usr_login.user_pw)) == 1
                    and len(usr_login.user_pw) >= 8
                    and len(usr_login.user_pw) <= 20
                ):
                    # [Function 4] checks if the given credential equates with the data in DB
                    query = login_query.queryData(find_id_pw_query)
                    if query is None:
                        return check_status.httpSignInStatus(400)  # unsearchable

                    else:
                        return check_status.httpSignInStatus(
                            200, query["room_code"]
                        )  # if succeed

                else:
                    return check_status.httpSignInStatus(500)  # id, pw regulation check
        else:
            return check_status.httpSignInStatus(400)  # handler check
    finally:
        return check_status.httpSignInStatus(300)  # runtime error
