FROM debian

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends git python3 netbase nano  \
 python3-pip python3-setuptools python3-wheel python3-dev build-essential libffi-dev libssl-dev && \
 mkdir -p /app && git clone https://github.com/gilles67/h42-auth.git /app/h42-auth && \
 pip3 install -r /app/h42-auth/requirements.txt && \
 chmod a+x /app/h42-auth/prod-app.sh && \
 apt-get purge -y python3-dev libffi-dev libssl-dev build-essential git && apt-get -y autoremove && apt-get clean

EXPOSE 5000

CMD ["/app/h42-auth/prod-app.sh"]
