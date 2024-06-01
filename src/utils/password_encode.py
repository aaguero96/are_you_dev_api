import bcrypt


def password_encode(password: str) -> str:
    salt = bcrypt.gensalt()
    response = bcrypt.hashpw(password.encode('utf-8'), salt)
    return response.decode('utf-8')