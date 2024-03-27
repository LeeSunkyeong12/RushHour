from fastapi import FastAPI, Request
from pydantic import BaseModel
import common.query as sql
import common.httperror as httperror
import common.setting as setting

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
async def userLogin(usrLogin: Login, request: Request) -> dict:
    """This is the main function that gives an proper response when requested
    :param1 str usrLogin: instance for Login Class
    :param2 str request: instance for Request Class
    pre-built function(import from fastapi) mainly handles the request header
    :return dict: return response in json format
    """
    headers = request.headers

    # query caller
    loginQuery = sql.MySQLConnect()
    findIdPwQuery = """SELECT room_code FROM rushhour.users
    where user_id = "{id}" and user_pw = "{pw}"; """.format(
        id=usrLogin.user_id, pw=usrLogin.user_pw
    )

    # Common Error Check
    checkStatus = httperror.HttpCommonError()

    # id, pw check
    loginCheck = setting.LoginRuleCheck()

    # [Function 5] handles the HTTP errors
    try:
        # [Feature 1] validate the authorization defined in request header
        if headers.get("Authorization") == "test":
            if len(usrLogin.user_id) == 0 or len(usrLogin.user_pw) == 0:
                return checkStatus.httpSignInStatus(500)  # no input
            else:  # [Function 2, 3] check user_id, user_pw credential in regulations
                if loginCheck.userIdCheck(usrLogin.user_id) and loginCheck.userPWCheck(
                    usrLogin.user_pw
                ):
                    # [Function 4] checks if the given credential equates with the data in DB
                    query = loginQuery.queryData(findIdPwQuery)
                    if query is None:
                        return checkStatus.httpSignInStatus(400)  # unsearchable

                    else:
                        return checkStatus.httpSignInStatus(
                            200, query["room_code"]
                        )  # if succeed

                else:
                    return checkStatus.httpSignInStatus(500)  # id, pw regulation check
        else:
            return checkStatus.httpSignInStatus(400)  # handler check
    except Exception:
        return checkStatus.httpSignInStatus(300)  # runtime error
