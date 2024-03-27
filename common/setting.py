import re


class LoginRuleCheck:
    """This class is comprised of the methods which are related to validation check by regex"""

    def __init__(self) -> None:
        pass

    def userIdCheck(self, userIdParam: str) -> bool:
        """This is a function that check an user ID to the pre-defined condition
        :param1 str userIdParam: user ID
        :return bool: true if the condition meets, else false
        """
        idCheck = re.findall("[a-zA-Z]", userIdParam)
        if len(userIdParam) == len(idCheck) and len(userIdParam) <= 15:
            return True
        else:
            return False

    def userPWCheck(self, userPwParam: str) -> bool:
        """This is a function that check an user password to the pre-defined condition
        :param1 str userIdParam: user password
        :return bool: true if the condition meets, else false
        """
        pwCheck = re.findall("[a-zA-Z0-9_\W]", userPwParam)
        if (
            len(userPwParam) == len(pwCheck)  # matches a regulation
            and len(re.findall("[_\W]", userPwParam)) == 1  # special character == 1
            and len(userPwParam) >= 8
            and len(userPwParam) <= 20  # length >= 8 and length <= 20
        ):
            return True
        else:
            return False
