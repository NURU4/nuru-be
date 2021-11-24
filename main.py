import json
from typing import Optional

from pymysql import NULL
from fastapi import FastAPI, Header, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from jwt import encode
from datetime import timedelta, datetime
from pytz import timezone


from exception import *

from model import user

from controller.user import *

from auth import *

app = FastAPI()

# configure middleware

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
async def root(authorization: str = Header(None)):
    return JSONResponse(content={"message": "test endpoint"})

## 소셜 로그인 아닌경우 회원가입
@app.post('/signup/nuru')
async def signup_no_social(user_args:user.UserNoSocialRegister):
    user_args = jsonable_encoder(user_args)
    # user argument 인코딩
    code, message = user_register_no_social_login(args=user_args)
    
    return JSONResponse(content={Header: {"Access-Control-Allow-Origin": '*'}, "message": message, "code": code}, status_code=code)


## 로그인 
@app.post('/signin/nuru')
async def signin(user_args:user.UserLogin):
    user_args = jsonable_encoder(user_args)

    code, message = user_login(args=user_args)
    
    ## 웹 토큰 만들어서 프론트에 전달
    expires = datetime.strftime(datetime.now(timezone('Asia/Seoul')) + timedelta(hours=24), '%Y-%m-%d %H:%M:%S')
    created = datetime.strftime(datetime.now(timezone('Asia/Seoul')),'%Y-%m-%d %H:%M:%S')

    if code == 200:
        token = encode(
            {
                'expires': expires,
                'created': created,
                'USER_EMAIL': user_args.get("USER_EMAIL")
            },
            key=secret_key
        )
    
    else:
        token = ""

    return JSONResponse(content={"message": message, "code": code, "token": token}, status_code=code)


@app.post('/signin/kakao')
async def signup_social(user_args: user.UserKakaoCode):
    user_args = jsonable_encoder(user_args)
    code, user_id, expires_in = user_kakao_signin(user_args)
    if code != 200:
        return JSONResponse(content={"message": "invalid account", "code": code, "token": NULL}, status_code=code)
    token = ""

    expires = datetime.strftime(datetime.now(timezone('Asia/Seoul')) + timedelta(seconds = expires_in), '%Y-%m-%d %H:%M:%S')
    created = datetime.strftime(datetime.now(timezone('Asia/Seoul')),'%Y-%m-%d %H:%M:%S')

    if code == 200:
        token = encode(
            {
                'expires': expires,
                'created': created,
                'social_token': user_id
            },
            key=secret_key
        )
    else:
        token = ""
    if len(token) > 50: token = token[:49]
    token_message, token_code = user_token_update(user_token=token, created=created, expires=expires, email=user_id)
    return JSONResponse(content={"message": "success", "token": token, "token_message": {"message": token_message, "code": token_code}}, status_code=code)


## 소셜 로그인 아닌경우 회원가입
"""
@app.post('/signup/social')
async def signup_social(user_args:user.UserSocialRegister):
    user_args = jsonable_encoder(user_args)
    # user argument 인코딩
    code, message = user_register_social_login(args=user_args)
    

    return JSONResponse(content={"message": message, "code": code}, status_code=code)


@app.post('/signin/social')
async def social_signin(user_args: user.UserSocialLogin):
    user_args = jsonable_encoder(user_args)
    code, message = user_social_login(args=user_args['code'])

    expires = datetime.strftime(datetime.now(timezone('Asia/Seoul')) + timedelta(hours=24), '%Y-%m-%d %H:%M:%S')
    created = datetime.strftime(datetime.now(timezone('Asia/Seoul')),'%Y-%m-%d %H:%M:%S')

    if code == 200:
        token = encode(
            {
                'expires': expires,
                'created': created,
                'USER_EMAIL': user_args.get("USER_EMAIL")
            },
            key=secret_key
        )
    
    else:
        token = ""

    return JSONResponse(content={"message": message, "code": code, "token": token}, status_code=code)
  """  


# 토큰 decode test (client가 signin에서 만든 token을 받아서 저장한 후 Authorization이라는 헤더에 넣어서 보냄 -> decode)
@app.get('/getuser')
async def get_user_info(Authorization: str = Header(None)):
    """
        getting user information needs user authorization and token should be decoded, if valid.
    """
    user_email = get_user_email_from_token(Authorization)
    return JSONResponse(content={"USER_EMAIL": user_email}, status_code=200)

#### ERROR HANDLING ####

@app.exception_handler(DBConnectionFailException)
async def db_connection_fail_exception_handler(request: Request, exc: DBConnectionFailException):
    return JSONResponse(status_code=400, content=exc.response_content)

@app.exception_handler(DBRequestFailException)
async def db_request_fail_exception_handler(request: Request, exc: DBRequestFailException):
    return JSONResponse(status_code=400, content=exc.response_content)

@app.exception_handler(DBPrimaryKeyDuplicateException)
async def db_primarykey_duplicate_exception_handler(request: Request, exc: DBPrimaryKeyDuplicateException):
    return JSONResponse(status_code=409, content=exc.response_content)

@app.exception_handler(InvalidUserEmailException)
async def invalid_user_email_exception_handler(request: Request, exc: InvalidUserEmailException):
    return JSONResponse(status_code=400, content=exc.response_content)

@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(request: Request, exc: TokenExpiredException):
    return JSONResponse(status_code=400, content=exc.response_content)