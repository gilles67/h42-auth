from datetime import datetime, timedelta
from h42auth import app

@app.template_filter('tdelta')
def timedelta_filter(s):
    seconds = (s - datetime.now()).total_seconds()
    sign_string = '-' if seconds < 0 else ''
    seconds = abs(int(seconds))
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '{}{:03d} : {:02d}:{:02d}:{:02d}'.format(sign_string, days, hours, minutes, seconds)
    else:
        return '{}{:02d}:{:02d}:{:02d}'.format(sign_string, hours, minutes, seconds)
