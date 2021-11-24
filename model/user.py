from pydantic import BaseModel
from typing import Optional


# 소셜 로그인 아닌 경우 회원가입 모델
class UserNoSocialRegister(BaseModel):
    USER_EMAIL: str
    USER_PW: str
    USER_NM: str

# 소셜 로그인 아닌 경우 로그인 모델
class UserLogin(BaseModel):
    USER_EMAIL: str
    USER_PW: str

# 소셜 로그인 시 회원가입 모델
class UserSocialRegister(BaseModel):
    USER_EMAIL: str
    USER_TOKEN: str
    USER_AUTH_TYPE: str
    USER_SOCIAL_ID: str = ''
    USER_NM: str

# 소셜 로그인 시 로그인 모델
class UserSocialLogin(BaseModel):
    USER_SOCIAL_ID: str
    USER_TOKEN: str # 이걸 Oauth객체로 두는게 나을것같긴한데 일단 두겠음
    USER_NM: str

class UserKakaoCode(BaseModel):
    USER_KAKAO_CODE: str

