import re
import datetime

def validate_card_data(card_number: str, exp_date: str, cvc: str):
    if not re.fullmatch(r'(\d{4}-){3}\d{4}', card_number):
        return {'error': 'Invalid card number'}
    if not re.fullmatch(r'\d{3}', cvc):
        return {'error': 'Invalid CVC'}
    if not re.fullmatch(r'\d{2}/\d{4}', exp_date):
        return {'error': 'Invalid expiration date'}
    month, year = map(int, exp_date.split('/'))
    if month < 1 or month > 12:
        return {'error': 'Invalid expiration date'}
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    if year < current_year or (year == current_year and month < current_month):
        return {'error': 'Card expired'}
    return None
