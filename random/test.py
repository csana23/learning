"""
Write a function in Python that given any date as an input 
returns the following Friday after that date!
"""

import datetime as DT

def next_friday(date):
    # Calculate the days until the next Friday
    days = (3 - date.weekday() + 7) % 7 + 1
    next_friday_date = date + DT.timedelta(days=days)
    return next_friday_date

input_date = DT.date(2024, 5, 17)
result = next_friday(input_date)
print(f"The next Friday after {input_date} is {result}")

