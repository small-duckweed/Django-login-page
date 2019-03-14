django注册登录
===
## 步骤
1. django-admin startproject my_login
2. 新建login模块 python manage.py startapp login
3. settings installed app 插接上login模块
4. 配置 settings DATABASES
5. 迁移数据库 python manage.py makemigrations ; python manage.py migrate
6. 运行 python manage.py runserver 127.0.0.1:8000

## 开发
### 登录
1. 创建User类
2. settings installed app 插接上login模块
3. python manage.py makemigrations login , python manage.py migrate
4. python manage.py createsuperuser  创建超级管理员
在admin.py 里面添加如下代码
```python
from . import models
admin.site.register(models.User)
```
5. 访问domain:port.admin
用上一步生成的后台账户登录
6. 往user表里添加一些测试用户
6. 设计路由
7. 开发views.py
8. session会话管理。简单的用户名密码跟数据库信息比对成功登录后，服务器仍然还不知道这个用户登录没有，*因为http请求是无状态的*，用户再次访问某一个页面时，服务器并不知道用户登录没有。
解决：当用户登录成功后服务器生成sessionid自己保存一份，并在返回response时添加set-cookie(sessionid='sdkjhfakew'), 游览器根据响应自己把sessionid保存到cookie中，之后游览器每次请求都会携带cookie(就好像参数), 服务器比对sessionid发现有就说明用户刚刚登录过，允许访问受限页面。
django_session表中存储session信息。key字段的值跟游览器cookie中的sessionid值一致，session_data字段解密后是{'is_login':True, 'username':'测试1'}
session和cookie区分：都为了存储一些数据，都是键值对。session加密了，安全，服务器端。cookie安全低，在游览器端。
换用不同游览器在本机模拟多用户登录。
9. 注册功能。表单验证。前端验证体验更好，直接显示错误信息，而后端需要刷新页面才能看出。前端验证缺点被黑客直接构造请求请求后端，后端验证安全。
## 基本需求
1. 简单登录
2. 简单注册
3. session cookie
4. ajax表单验证
5. 邮箱验证
(思路，user表新增字段active，注册保存到数据库后，取user.id，base64编码userid，拼'http://127.0.0.1:8000/active/?userid=7),往用户注册邮箱发一封邮件，邮件内容请点击激活链接，然后进入active视图函数，更新这个用户行的active字段为True
## 追加需求



## 报错
1. django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module
没有数据库驱动
解决方法一：
安装MySQLdb包，这个包底层c必须编译安装，无法直接pip安装。https://dev.mysql.com/downloads/connector/python/下载对应的exe程序。mysql-connector-python.exe。安装成功后解释器中看到mysql-connector-python  引入import MySQLdb
解决方法二(django官方推荐)：
MySQLdb安装麻烦，所以有人重写不依赖c编译的，但是语法和接口调用跟MySQLdb相同的包。pip install mysqlclient  在windows上安装会直接安装，whl文件而不需要vc编译，安装成功后会生成 xxx.pyd文件(就是.dll文件)，安装后只能手动卸载
解决方法三(推荐)：
pymysql以兼容MySQLdb方式启动。
根目录/my_login/__init__.py下加入下面代码
```python
import pymysql
pymysql.install_as_MySQLdb()
```
当你引入一个包时，先加载__init__.py文件

2. django.db.utils.InternalError: (1049, "Unknown database 'login'")
settings.py中配置的数据库name不存在，在数据库图形工具或终端中创建数据库 CREATE DATABASE login;

3. from django.urls import path 报错
原因安装的django为1.x老版本，语法跟2.x不同
4. unknown time zone
原因时区名错写 Asia/Shanghai 写成大小写字母错误的其它形式
5. 更新后的代码没效果，浏览器访问后台无日志
原因由于系统问题进程未正确结束