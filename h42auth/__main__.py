import sys
import logging
import os.path
app_path = os.path.abspath(os.path.join(os.path.basename(__file__), '..'))
sys.path.append(app_path)

from h42auth import app

if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    if gunicorn_logger:
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
    app.run(host="0.0.0.0", debug=True)
