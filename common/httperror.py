http_response_true = {
    "ifLogin": True,
    "roomCode": "rand",
    "status": "200",
    "statusMessage": "Success",
}

http_response_false = {
    "ifLogin": False,
    "status": "500",
    "statusMessage": "Invalid Format",
}

error_code = {
    300: "bad request",
    400: "unauthorized",
    500: "invalid format",
    700: "internal error",
}


class HttpCommonError:
    """This class is comprised of the methods which are related to common error from HTTP request"""

    def __init__(self) -> None:
        pass

    def httpSignInStatus(self, error_num, data=None):
        """
        This is a function that checks the info in the response
        and return the corresponding results
        :param1 int error_num: error code defined in Wiki; common error code
        :param2 str data (optional): receive query result(room number) when succeeds,
          default as Null when fails
        :return dict: return response in json format
        """
        if error_num == 200:
            http_response_true["roomCode"] = data
            return http_response_true
        else:
            http_response_false["status"] = error_num
            http_response_false["statusMessage"] = error_code[error_num]

            return http_response_false
