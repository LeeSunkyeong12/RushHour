class HttpCommonError:
    """This class is comprised of the methods which are related to common error from HTTP request"""

    def __init__(self) -> None:
        self.httpResponseTrue = {
            "ifLogin": True,
            "roomCode": "rand",
            "status": "200",
            "statusMessage": "Success",
        }

        self.httpResponseFalse = {
            "ifLogin": False,
            "status": "500",
            "statusMessage": "Invalid Format",
        }

        self.errorCode = {
            300: "bad request",
            400: "unauthorized",
            500: "invalid format",
            700: "internal error",
        }

    def httpSignInStatus(self, errorNum: int, queryResult=None):
        """
        This is a function that checks the info in the response
        and return the corresponding results
        :param1 int errorNum: error code defined in Wiki; common error code
        :param2 str queryResult (optional): receive query result(room number) when succeeds,
        :param1 int errorNum: error code defined in Wiki; common error code
        :param2 str queryResult (optional): receive query result(room number) when succeeds,
          default as Null when fails
        :return dict: return response in json format
        """
        if errorNum == 200:
            self.httpResponseTrue["roomCode"] = queryResult
            return self.httpResponseTrue
        else:
            self.httpResponseFalse["status"] = errorNum
            self.httpResponseFalse["statusMessage"] = self.errorCode[errorNum]

            return self.httpResponseFalse
