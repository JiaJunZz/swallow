FROM python:3.6.8-slim
LABEL Description="This images is swallow django app" Maintainer="jiajunzz"

RUN mkdir -p /opt/swallow
COPY docker-entrypoint.sh LICENSE manage.py README.md requirements.txt /opt/swallow/
COPY apps/ /opt/swallow/apps/
COPY swallow/ /opt/swallow/swallow/

WORKDIR /opt/swallow/
RUN set -ex;\
	\
	sed -i s@"'HOST': '127.0.0.1'"@"'HOST': 'db'"@g /opt/swallow/swallow/settings.py; \
	sed -i s@"BROKER_URL = 'redis://127.0.0.1:6381'"@"BROKER_URL = 'redis://redis'"@g /opt/swallow/swallow/settings.py; \
	sed -i s@"CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6381'"@"CELERY_RESULT_BACKEND = 'redis://redis'"@g /opt/swallow/swallow/settings.py; \
	\
	echo "" > /etc/apt/sources.list; \
	{ \
		echo "deb http://mirrors.aliyun.com/debian/ stretch main non-free contrib"; \
		echo "deb-src http://mirrors.aliyun.com/debian/ stretch main non-free contrib"; \
                echo "deb http://mirrors.aliyun.com/debian-security stretch/updates main"; \
		echo "deb-src http://mirrors.aliyun.com/debian-security stretch/updates main"; \
		echo "deb http://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib"; \
		echo "deb-src http://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib"; \
		echo "deb http://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib"; \
		echo "deb-src http://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib"; \
	} > /etc/apt/sources.list; \
	\
	apt-get update; \
	apt-get install -y --no-install-recommends libmariadbclient-dev gcc; \
	rm -rf /var/lib/apt/lists/*; \
        pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/; \
	\
	chmod 777 /opt/swallow/docker-entrypoint.sh; \
	ln -s /opt/swallow/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
	\
ENTRYPOINT ["docker-entrypoint.sh"]

EXPOSE 8000

