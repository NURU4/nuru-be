from exception import *
from datetime import datetime
from pytz import timezone
import jwt



secret_key = "nuru2021"
algorithm = ["HS256"]

def get_user_email_from_token(token:str) -> str:
    """
        decoder: receive Authorization token from the client -> return decoded
    """
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=algorithm)

        if decoded_token.get("expires") < datetime.strftime(datetime.now(timezone('Asia/Seoul')),'%Y-%m-%d %H:%M:%S'):
            raise TokenExpiredException()

        if not decoded_token.get("USER_EMAIL"):
            raise InvalidUserEmailException()

        return decoded_token.get("USER_EMAIL")

    except Exception as err:
        if TokenExpiredException or InvalidUserEmailException:
            raise

        