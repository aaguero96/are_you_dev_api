import jwt
import datetime


def encode_data(payload) -> str:
    secret = ""

    payload["exp"] = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)

    return jwt.encode(payload, secret, algorithm='HS256')