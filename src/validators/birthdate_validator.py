from datetime import date, datetime


def birthdate_validator(birthdate: date) -> bool:
    try:
        datetime.strptime(str(birthdate), "%Y-%m-%d")
        return True
    except ValueError as err:
        return False