from db import *
from query import *

## 소셜 로그인 아닌 경우 회원가입
def user_register_no_social_login(args):
    """
        receive encoded user info and execute query.
        - add record to user_table and parameters would be user data(model.user.UserNoSocialRegister)
    """
    code, message = exec_query(USER_REGISTER_NO_SOCIAL_LOGIN_QUERY, args)

    return code, message


## 로그인
def user_login(args):
    result = exec_fetch_query(USER_LOGIN_QUERY, args)

    if not result:
        return 404, "User not found"

    return 200, "Success"


def user_register_social_login(args):
    code, message = exec_query(USER_REGISTER_SOCIAL_LOGIN_QUERY, args)
    return code, message


def user_social_login(args):
    token = exec_fetch_query(USER_SOCIAL_LOGIN_QUERY, args)
    
    if not token:
        return 404, "User not found"
    else:
        if token['USER_TOKEN'] != args['USER_TOKEN']:
            # 유저는 존재하지만 OAuth 토큰값이 업데이트 된 경우
            code, _ = exec_query(USER_SOCIAL_TOKEN_UPDATE_QUERY, args)
            return code, "Updated user token"
    return 200, "Success"