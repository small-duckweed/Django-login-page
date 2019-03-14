from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
#look 很多权限验证和中间件，都在contrib里
from . import models
import hashlib

def index(request):  # django上下文传递用的request
    return render(request, 'index.html')  # look templates文件夹在login这个包里，

def login(request):
    if request.method == 'GET':
        # 用户初次进入展示登录表单
        return render(request, 'login.html')
    elif request.method == 'POST':

        # 给前端传参
        context = {
            'message': ''
        }

        # 用户提交表单
        username = request.POST.get('username')
        password = request.POST.get('password')  # 从前端name属性中取值

        # 验证账户名密码
        user = models.User.objects.filter(name=username).first()
        if user:
            if _hash_password(password) == user.hash_password:  #look hash密码判断写法
            # if user.password == password:  #look 明文密码判断
                context['message'] = '登录成功'
                # look 服务器设置sessionid和其它用户信息。sessionid（服务器给访问它的游览器的身份证）自动生成的。
                # look request.session对象就是django_session表，['is_login']这种键值对的存储，其实就是存在了django_session表里的session_data字段，这个字段是哈希加密的，解密后就是一个键值对的字典
                request.session['is_login'] = True
                request.session['username'] = user.name
                request.session['userid'] = user.id
                return redirect('/index/')  # 返回的响应中包含set-cookie(sessionid='adadaDAD')，游览器收到响应后会把sessionid存到cookie中。
            else:
                context['message'] = '密码不正确'
                return render(request, 'login.html', context=context)
        else:
            context['message'] = '未注册'
            return render(request, 'login.html', context=context)


def register(request):
    if request.method == 'GET':
        # 注册表单
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')


        # 简单后端表单验证（正则最合适）
        # not优先级是比较低的，没有and高
        # if not username.strip() and password.strip() and email.strip():
        #     print('某个字段为空')
        #     return render('/register', context={'message': '某个字段为空'})
        # if len(username) > 20 or len(password) > 20:
        #     print('用户名或密码长度不能超过20')
        #     # 排除特殊字符串eval() \q & $
        #     return render('/register', context={'message': '字段不能超过20'})


        # 写数据库
        user = models.User.objects.filter(email=email).first()
        if user:
            # 用户已注册
            return render(request, 'register.html', context={'message': '用户已注册'})

        # 加密密码

        hash_password = _hash_password(password)

        try:
            # 'insert into login_user (name,password,email) values (%s, %s, %s)'%('','','')
            user = models.User(name=username, hash_password=hash_password, password=password, email=email)
            user.save()  # django的orm保存成功了，不会返回什么，保存失败会报错，所以想看它是否保存成功需要加 try except
            print('保存成功')
            return render(request, 'login.html', context={'message': '注册成功，请登录'})
        except Exception as e:
            print('保存失败', e)  # 比起用
            return redirect("/register")

        # else:  # look 如果except没有报错，那么就会执行else
        #     print('保存成功')
        #     return redirect('/login/')

def logout(request):
    """ 登出 """
    # 如果session没有的话，用session["is_login"]会报键错误
    # （老师把这句话删了）未登录时不让走登录
    # if not request.session.get('is_login'):
    #     return redirect('/index/')

    # 清除session 登出
    request.session.flush()   # 清除此用户session对应的所有sessiondata
    # del request.session['user_id']  # 清除某个session键值对
    return redirect('/index/')


def _hash_password(password):  # _开头表示内部使用
    """哈希加密用户注册密码"""
    sha = hashlib.sha256()
    sha.update(password.encode(encoding='utf-8'))
    return sha.hexdigest()

# def _hash_password(password):  # _开头表示内部使用
#     """哈希加密用户注册密码  加盐版课下完成"""
#     salt = ""
#     for i in range(4):
#         salt += chr(random.randint(65, ))
#     sha = hashlib.sha256()
#     sha.update(password.encode(encoding='utf-8'))
#     return sha.hexdigest()


# 查询数据库
# 'select * from login_user where username={} and password={}'%(username, password)
# first() ORM取一个值
# rs = models.User.objects.filter(name=username, password=password).first()
# if not rs: # look   not 空值  为True
