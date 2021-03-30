import datetime

def process_time(intime, start, end):
    if start <= intime <= end:
        return True
    elif start > end:
        end_day = time(hour=23, minute=59, second=59, microsecond=999999)
        if start <= intime <= end_day:
            return True
        elif intime <= end:
            return True
    return False