from db import *
from query import *
import requests
from datetime import timedelta, datetime

import boto3
import logging

## 소셜 로그인 아닌 경우 회원가입
def user_token_update(user_token, created, expires, email):
    code, message = exec_query(USER_TOKEN_UPDATE_QUERY, {'USER_TOKEN': user_token, 'USER_TOKEN_EXPIRED_DTTM': expires, 'CREATED_DTTM': created, 'USER_EMAIL': email})
    return code, message

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


# def user_social_login(args):
#     token = exec_fetch_query(USER_SOCIAL_LOGIN_QUERY, args)

#     if not token:
#         return 404, "User not found"
#     else: #유저는 존재하지만 소셜 토큰값이 업데이트 된 경우
#         usernm = exec_fetch_query()
#         if token['USER_TOKEN'] != args['USER_TOKEN']:
#             # 유저는 존재하지만 OAuth 토큰값이 업데이트 된 경우
#             #code, _ = exec_query(USER_SOCIAL_TOKEN_UPDATE_QUERY, args)
#             return code, "Updated user token"
#     return 200, "Success"

bucket_name = "nuruimages"
client = boto3.client(
				's3', 
                aws_access_key_id='AKIAXGUVCKKK7DWDXFHU', 
                aws_secret_access_key='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',    
)


def user_kakao_getInfo(access_token, refresh_token):
    response = requests.post(url="https://kapi.kakao.com/v2/user/me", headers={'Authorization': "Bearer {" + access_token + "}"})
    
    if response.status_code != 200:
        response = requests.post(url="https://kapi.kakao.com/v2/user/me", headers={'Authorization': "Bearer {" + refresh_token + "}"})
        if response.status_code != 200: return response.status_code, "no user id"
    response_data = response.json()
    user_kakao_id = str(response_data['id'])
    args = {'USER_SOCIAL_YN': "Y", 'USER_AUTH_TYPE': "KAKA  O", 'USER_SOCIAL_ID': user_kakao_id}
    result = exec_fetch_query(USER_SOCIAL_ACCOUNT_QUERY, args)
    if not result:
        code, _ = exec_query(USER_SOCIAL_REGISTER_QUERY, args)
        return code, user_kakao_id
    return 200, user_kakao_id
     # 신규 유저인 경우, 회원가입

def user_kakao_signin(args):
    datas = {'grant_type': "authorization_code", 'client_id': "c38ee04e16631dabbb8e43a1ed540d05", 'redirect_uri': "http://localhost:3000/oauth/callback/kakao-login", 'code': args['USER_KAKAO_CODE']}
    response = requests.post(url="https://kauth.kakao.com/oauth/token", data=datas)
    response_data = response.json()
    if response.status_code != 200: return response.status_code, "invalid code", 0
    token = response_data['access_token']
    refresh_token = response_data['refresh_token']
    code, user_id = user_kakao_getInfo(token, refresh_token)
    return code, user_id, response_data['expires_in'] + response_data['refresh_token_expires_in']  

def s3_upload_image(image_file, image_key):
    try:
        client.put_object(Body=image_file.file, Bucket=bucket_name, Key=image_key, ContentType=image_file.content_type, ACL='public-read')
    except Exception:
        raise DBRequestFailException(err_msg="s3 update failed")
    return 200, "image uploaded"
    
def get_user_image_locations(image_key):
    location = client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
    url = "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, image_key)
    return url