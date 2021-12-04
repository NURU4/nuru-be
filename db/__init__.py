import pymysql
from exception import *
from typing import Dict,Any

## DB CONFIG
def get_DB_access_info():
    return {
        "host": "13.125.255.212",  
        "user": "nuru",
        "password": "nuru2021",
        "port": 3306,
    }

## CONNECT_DB
def connect_db() -> pymysql.cursors:
    try:
        db = pymysql.connect(**get_DB_access_info(), cursorclass=pymysql.cursors.DictCursor, read_timeout=20, write_timeout=20, autocommit=True)
        cursor = db.cursor()

        return cursor

    except Exception as err:
        raise DBConnectionFailException(str(err))

## QUERY EXECUTE
def exec_query(query_str: str, input_params=""):
    try:
        cursor = connect_db()
        cursor.execute(query_str, input_params)

        if cursor.rowcount == 0:
            return 404, "Not found"

        print("ssss")

        return 200, "Success"

    except Exception as err:
        if "Duplicate" in str(err):
            raise DBPrimaryKeyDuplicateException(str(err))
            
        raise DBRequestFailException(str(err))

## EXECUTE SELECT QUERY
def exec_fetch_query(query_str: str, input_params="") -> Dict[Any, Any]:
    try:
        cursor = connect_db()
        cursor.execute(query_str, input_params)

        result = cursor.fetchall()

        if len(result) == 0:
            return None

        if len(result) == 1:
            return result[0]
        return result
        
    except Exception as err:
        raise DBRequestFailException(str(err))
