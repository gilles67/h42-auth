FROM debian

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends git python3 python3-pip python3-setuptools nano python3-wheel \
 python3-dev build-essential netbase && apt-get autoremove && apt-get clean && \
 mkdir -p /app && git clone https://github.com/gilles67/h42-auth.git /app/h42-auth && \
 pip3 install flask werkzeug==0.16.0 flask-bootstrap flask-socketio flask-login flask-session \
 flask-cors flask-wtf flask-pymongo gunicorn eventlet tinydb && \
 chmod a+x /app/h42-auth/prod-app.sh && \
 apt-get purge -y python3-dev build-essential git && apt-get -y autoremove && apt-get clean

EXPOSE 5000

CMD ["/app/h42-auth/prod-app.sh"]
