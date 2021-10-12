from typing import Dict

# DB 연결 실패
class DBConnectionFailException(Exception):
    def __init__(self, err_msg):
        self.message = "DB 연결에 실패했습니다."
        self.err_msg = err_msg

        self.response_content = {"message": self.message, "err_msg": self.err_msg}


# DB 쿼리 실패
class DBRequestFailException(Exception):
    def __init__(self, err_msg):
        self.message = "DB 요청에 실패했습니다."
        self.err_msg = err_msg

        self.response_content = {"message": self.message, "err_msg": self.err_msg}

# DB PK 중복
class DBPrimaryKeyDuplicateException(Exception):
    def __init__(self, err_msg):
        self.message = "PK가 중복되는 항목이 있습니다."
        self.err_msg = err_msg

        self.response_content = {"message": self.message, "err_msg": self.err_msg}


# 잘못된 USER_EMAIL
class InvalidUserEmailException(Exception):
    def __init__(self):
        self.message = "사용자를 찾을 수 없습니다."



        self.response_content = {"message": self.message}

# 토큰 만료
class TokenExpiredException(Exception):
    def __init__(self):
        self.message = "TOKEN이 만료되었습니다."

        self.response_content = {"message": self.message}