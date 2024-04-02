from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
import common.query as sql
import common.httperror as httperror
import re

app = FastAPI()
checkStatus = httperror.HttpCommonError()
loginQuery = sql.MySQLConnect()


class Login(BaseModel):
    # user_id: str = Field(min_length=1, max_length=15, pattern=r"[a-zA-Z]")
    # user_pw: str = Field(min_length=8, max_length=20, pattern=r"[a-zA-Z0-9_\W]")
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
    findIdPwQuery = """SELECT room_code FROM rushhour.users
    where user_id = "{id}" and user_pw = "{pw}"; """.format(
        id=usrLogin.user_id, pw=usrLogin.user_pw
    )

    # id, pw check
    idCheck = re.findall("[a-zA-Z]", usrLogin.user_id)
    pwCheck = re.findall("[a-zA-Z0-9_\W]", usrLogin.user_pw)

    # [Function 5] handles the HTTP errors
    try:
        # [Feature 1] validate the authorization defined in request header
        if not headers.get("Authorization") == "test":
            return checkStatus.httpSignInStatus(400)

        # if null
        if len(usrLogin.user_id) == 0 or len(usrLogin.user_pw) == 0:
            return checkStatus.httpSignInStatus(500)  # no input

        # [Function 2, 3] check userID, user_pw credential in regulations
        if not (
            (len(usrLogin.user_id) == len(idCheck) and len(usrLogin.user_id) <= 15)
            and (
                len(usrLogin.user_pw) == len(pwCheck)
                and len(re.findall("[_\W]", usrLogin.user_pw)) == 1
                and len(usrLogin.user_pw) >= 8
                and len(usrLogin.user_pw) <= 20
            )
        ):
            return checkStatus.httpSignInStatus(500)

        # [Function 4] checks if the given credential equates with the data in DB
        query = loginQuery.queryData(findIdPwQuery)
        if query is None:
            return checkStatus.httpSignInStatus(400)  # unsearchable

        # final return
        return checkStatus.httpSignInStatus(200, query["room_code"])

    except Exception:
        return checkStatus.httpSignInStatus(300)  # runtime error


## check if regex is appliable into pydantic field
## create test API to test out the case above

# if __name__ == "__main__":

#     class Login(BaseModel):
#         user_id: str
#         user_pw: str

#     @app.post("/api/v1/login_test")
#     async def userLogin_(usrLogin: Login) -> dict:
#         userLogin.
