import re

"""ID rule check"""


def id_check(user_id: str) -> bool:
    """A function that validate ID complexity"""
    idCheck = re.findall("[a-zA-Z]", user_id)

    if len(user_id) == len(idCheck) and len(user_id) >= 1 and len(user_id) <= 15:
        return True
    else:
        return False


def test_id_check():
    """A test function that checks id_check()"""
    # 1. Correct answer given
    assert id_check("roadmansion") is True
    # 2. Special character included
    assert id_check("roadmansion@") is False
    # 3. Numbers included
    assert id_check("roadmansion12") is False
    # 4. Characters more than 15
    assert id_check("roadmansioneeeeeeeeeeeeeeeeeeeeeeeeeeeeee") is False
    # 5. Nothing given
    assert id_check("") is False


"""PW Rule Check"""


def pw_check(user_pw: str) -> bool:
    """A function that validate PW complexity"""
    pwCheck = re.findall(r"[a-zA-Z0-9_\W]", user_pw)

    if (
        len(user_pw) == len(pwCheck)
        and len(re.findall(r"[_\W]", user_pw)) == 1
        and len(user_pw) >= 8
        and len(user_pw) <= 20
    ):
        return True
    else:
        return False


def test_pw_check():
    """A test function that checks pw_check()"""
    # 1. correct answer given
    assert pw_check("@24680rM") is True
    # 2. Less than 8 characters
    assert pw_check("2468") is False
    # 3. More than 20 characters
    assert pw_check("@24680rMMMMMMMMMMMMMMMM") is False
    # 4. Special Character more than 1
    assert pw_check("@@24680rM") is False
    # 5. No special character included
    assert pw_check("24680rM") is False
    # 6. Nothing is given
    assert pw_check("") is False


"""Header Validation Check"""


def header_check(header):
    """A function that validate a header"""
    if header == "test":
        return True
    else:
        return False


def test_header_check():
    """A test function that checks header_check()"""
    # 1. correct answer given
    assert header_check("test") is True
    # 2. numbers are included
    assert header_check("test12") is False
    # 3. special character are included
    assert header_check("test@#") is False
    # 4. Nothing is given
    assert header_check("") is False
