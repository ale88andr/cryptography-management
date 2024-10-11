from datetime import date, datetime


DATE_FORMAT = "%Y-%m-%d"
DATE_FORMAT_STR = "%d.%m.%Y"


def format_string(str_: str) -> str:
    return str_.strip() \
                .replace("\n","") \
                .replace("\r","")


def format_string_lower(str_: str) -> str:
    return format_string(str_).lower()


def format_date(
    date_str: str, date_format: str=DATE_FORMAT
) -> datetime|None:
    if date_str:
        return datetime.strptime(date_str, date_format)
    return None


def format_date_to_str(date_: date, date_format: str=DATE_FORMAT_STR) -> str|None:
    if date_:
        return date_.strftime(date_format)
    return None


def get_month(date_: date) -> str:
    if date_:
        return date_.strftime("%B").lower()
    return None


def get_year(date_: date) -> str:
    if date_:
        return date_.strftime("%Y")
    return None


def get_date_tuple(date_: date) -> tuple:
    if date_:
        return date_.strftime("%d"), date_.strftime("%B").lower(), date_.strftime("%Y")
    return None


def get_str_now_date(date_format: str=DATE_FORMAT) -> str:
    return datetime.today().strftime(date_format)
