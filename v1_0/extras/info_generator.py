from datetime import date, datetime


def generate_date() -> str:
    """
    Returns the current date as a string in the format 'YYYY/MM/DD'.
    """
    return date.today().strftime('%Y/%m/%d')

def generate_time() -> str:
    """
    Returns the current time as a string in the format 'HH:MM:SS'.
    """

    return datetime.now().strftime('%H:%M:%S')
