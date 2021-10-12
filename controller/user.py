from db import *
from query import *

## 소셜 로그인 아닌 경우 회원가입
def user_register_no_social_login(args):
    code, message = exec_query(USER_REGISTER_NO_SOCIAL_LOGIN_QUERY, args)

    return code, message


## 로그인
def user_login(args):
    result = exec_fetch_query(USER_LOGIN_QUERY, args)

    if not result:
        return 404, "User not found"
    
    return 200, "Success"