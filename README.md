# swallow

[swallow](https://github.com/JiaJunZz/Swallow)是一个后端基于[django](https://github.com/django/django)和[DjangoRestFramework](https://github.com/encode/django-rest-framework)，前端基于[vue](https://github.com/vuejs/vue)和[element-ui](https://github.com/ElemeFE/element)实现的应用，主要面向linux运维工程师使用，管理linux资产信息。

## 演示

![demo](https://github.com/JiaJunZz/JiaJun.zz.github.io/blob/master/images/Swallow/demo.gif)

## 功能特性

  - 服务器信息自动定时采集
  - celery异步队列
  - RBAC基于角色的权限访问控制
  - RESTful API

## 技术栈

### 后端
  - [Python 3.6.8](https://www.python.org/)
  - [django2.1](https://github.com/django/django)
  - [DjangoRestFramework3.9.1](https://github.com/encode/django-rest-framework)
  - [Celery4.3.0](https://github.com/celery/celery)
  - [Redis5](https://github.com/antirez/redis)
  - [Ansible2.7](https://github.com/ansible/ansible)
  - [MariaDB10.1.37](https://mariadb.org/)
### 前端
  - [vue](https://github.com/vuejs/vue)
  - [element-ui](https://github.com/ElemeFE/element)
  - [vue-admin-template](https://github.com/PanJiaChen/vue-admin-template)

## 前序准备

你需要在本地linux服务器安装[Python](https://www.python.org/)、[MariaDB](https://mariadb.org/)、[Redis](https://github.com/antirez/redis)、[nodejs](https://github.com/nodejs/node)、[git](https://git-scm.com/)、[Ansible](https://github.com/ansible/ansible)

## 开发环境部署

### 安装
```bash
# 克隆项目
git clone git@github.com:JiaJunZz/Swallow.git

# 进入项目目录
cd Swallow/

# 安装后端依赖
pip install -r requirements.txt

# 进入前端目录
cd web/

# 安装前端依赖
npm install

# 如果node-sass安装失败再次执行
npm install node-sass --unsafe-perm
```

### 配置
配置文件Swallow/swallow/settings.py，修改连接数据库server的配置信息
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'swallow',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
# celery中间件 redis://redis服务所在的ip地址:端口/数据库号
BROKER_URL = 'redis:/127.0.0.1:6379'

# celery结果返回，可用于跟踪结果
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'

# 管理用户
REQUEST_USERNAME = 'admin'

# 管理员用户密码
REQUEST_PASSWORD = 'admin123456'

# 获取token的url
REQUEST_TOKEN_URL = 'http://127.0.0.1:8000/api-token-auth/'

# 服务器数据自动提交的API接口
REQUEST_AUTOSERVER_URL = 'http://127.0.0.1:8000/serverauto/'

```

配置文件 swallow/web/config/dev.env.js，修改连接后端的IP地址和端口
```js
module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  BASE_API: '"http://127.0.0.1:8000"',
})
```

配置文件 swallow/web/config/index.js，修改浏览器登录的地址
```js
module.exports = {
  dev: {
    host: '192.168.123.173',
    port: 9528,
      }
```

修改配置文件 /etc/ansible/hosts，用于自动收集服务器信息
```bash
[swallow_servers]
192.168.123.168 ansible_python_interpreter="/usr/bin/python2"
```

## 启动程序

```bash
cd swallow
# 迁移数据库，如果出现问题可以删除migrations/下migrations的py代码
python manage.py makemigrations
python manage.py migrate
# 创建后台管理员用户
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
celery -A swallow worker -B -l INFO
cd web/
npm run dev
```

## 浏览器登录

```
http://192.168.123.173:9528/#/login
```

## API router

```
http://127.0.0.1:8000
```
![router](https://github.com/JiaJunZz/JiaJun.zz.github.io/blob/master/images/Swallow/router.jpg)

## API Doc
```
http://127.0.0.1:8000/docs
```
![apidoc](https://github.com/JiaJunZz/JiaJun.zz.github.io/blob/master/images/Swallow/apidoc.jpg)

## Browsers support

Modern browsers and Internet Explorer 10+.

| [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/edge/edge_48x48.png" alt="IE / Edge" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>IE / Edge | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/firefox/firefox_48x48.png" alt="Firefox" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>Firefox | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/chrome/chrome_48x48.png" alt="Chrome" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>Chrome | [<img src="https://raw.githubusercontent.com/alrra/browser-logos/master/src/safari/safari_48x48.png" alt="Safari" width="24px" height="24px" />](http://godban.github.io/browsers-support-badges/)</br>Safari |
| --------- | --------- | --------- | --------- |
| IE10, IE11, Edge| last 2 versions| last 2 versions| last 2 versions

## License

[MIT](https://github.com/JiajunZz/swallow/blob/master/LICENSE) license.
