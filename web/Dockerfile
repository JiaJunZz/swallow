FROM node:11.14.0-stretch-slim
LABEL Description="This images is swallow vue app" Maintainer="jiajunzz"

ENV SWALLWO_DJANGO swallow-django

RUN mkdir -p /opt/web
COPY .babelrc .editorconfig .eslintignore .eslintrc.js favicon.ico index.html LICENSE package.json .postcssrc.js .travis.yml /opt/web/
COPY build/ /opt/web/build/
COPY config/ /opt/web/config/
COPY src/ /opt/web/src/
COPY static/ /opt/web/static/
WORKDIR /opt/web/
RUN set -ex;\
	\
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
	apt-get install -y python; \
	rm -rf /var/lib/apt/lists/*; \
	\
	sed -i s/192.168.123.173/django/g /opt/web/config/dev.env.js; \
	npm install --registry=https://registry.npm.taobao.org

CMD ["npm","run","dev"]

EXPOSE 9528
