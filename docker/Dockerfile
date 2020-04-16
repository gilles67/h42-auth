FROM debian

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip nano python3-flask python3-flaskext.wtf \
	 python3-dnspython python3-flask-login

EXPOSE 5000

CMD ["/bin/bash"]
