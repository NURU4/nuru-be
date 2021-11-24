from db import *
from query import *
import requests 
from datetime import timedelta, datetime

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




def user_social_login(args):
    token = exec_fetch_query(USER_SOCIAL_LOGIN_QUERY, args)

    if not token:
        return 404, "User not found"
    else: #유저는 존재하지만 소셜 토큰값이 업데이트 된 경우
        usernm = exec_fetch_query()
        if token['USER_TOKEN'] != args['USER_TOKEN']:
            # 유저는 존재하지만 OAuth 토큰값이 업데이트 된 경우
            code, _ = exec_query(USER_SOCIAL_TOKEN_UPDATE_QUERY, args)
            return code, "Updated user token"
    return 200, "Success"

def user_social_register(args):
    code, message = exec_query(USER_SOCIAL_REGISTER_QUERY, args)
    return code, message

def user_kakao_getInfo(access_token):
    response = requests.post(url="https://kapi.kakao.com/v2/user/me", headers={'Authorization': access_token})
    response_data = response.json()
    user_kakao_id = str(response_data['id'])
    args = {'USER_EMAIL': " ", 'USER_SOCIAL_YN': "Y", 'USER_AUTH_TYPE': "KAKAO", 'USER_SOCIAL_ID': user_kakao_id}
    result = exec_fetch_query(USER_SOCIAL_ACCOUNT_QUERY, args)
    if result: return "access token"
    if 'kakao_account' in response_data:
        user_info = response_data['kakao_account']
        args['USER_EMAIL'] = user_info['email']
    code, message = user_social_register(args)
    
    return code, message

def user_kakao_login(args):
    datas = {'grant_type': "authorization_code", 'client_id': "c38ee04e16631dabbb8e43a1ed540d05", 'redirect_uri': "http://localhost:3000/oauth/callback/kakao-login", 'code': args['USER_KAKAO_CODE']}
    response = requests.post(url="https://kauth.kakao.com/oauth/token", data=datas)
    response_data = response.json()
    token = response_data['access_token']
    refresh_token = response_data['refresh_token']
    # app_token = user_kakao_getInfo(token)
    if response.status_code != 200: return response.status_code, "invalid code"
    return response.status_code, response_data
    


        