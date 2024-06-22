from datetime import datetime

def get_current_year () :
    return datetime.now().strftime("%Y")

def get_current_month () :
    return datetime.now().strftime("%m")