from datetime import date, datetime


def generate_date():
    return date.today().strftime('%Y/%m/%d')

def generate_hour():
    return datetime.now().strftime('%H:%M:%S')
