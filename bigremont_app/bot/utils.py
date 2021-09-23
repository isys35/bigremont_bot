from datetime import datetime, timedelta


def get_date_of_delivery_from_text(text: str):
    date_params = {
        'сегодня': datetime.now(),
        'завтра': datetime.now() + timedelta(days=1),
        'послезавтра': datetime.now() + timedelta(days=2),
    }
    date_of_delivery = date_params.get(text)
    if date_of_delivery:
        return date_of_delivery
    try:
        date_of_delivery = datetime.strptime(text, "%d.%m.%Y")
        return date_of_delivery
    except Exception:
        return
