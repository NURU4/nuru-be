from pydantic import BaseModel
from typing import Optional


# 소셜 로그인 아닌 경우 회원가입 모델
class UserNoSocialRegister(BaseModel):
    USER_EMAIL: str
    USER_PW: str
    USER_NM: str

# 로그인 모델
class UserLogin(BaseModel):
    USER_EMAIL: str
    USER_PW: str