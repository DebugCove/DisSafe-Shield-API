from datetime import date, datetime


def generate_date():
    return date.today().strftime('%d/%m/%Y')

def generate_hour():
    return datetime.now().strftime('%H:%M:%S')
