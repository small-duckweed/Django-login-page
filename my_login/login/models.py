from django.db import models
from django.utils import timezone
# Create your models here.
class User(models.Model):
    """用户表"""

    GENDER_CHOICE = (
        ('male', '男'),  # 第一项会存储到数据库中
        ('female', '女'),
        ('unknown', '未知'),
    )

    # 自增主键id，自动创建
    # max_length=20  等于 varchar(20)
    name = models.CharField('姓名', max_length=20)
    password = models.CharField('密码', max_length=20)
    hash_password = models.CharField('哈希密码', max_length=128, null=True, blank=True)
    # choices 选择项
    gender = models.CharField('性别', choices=GENDER_CHOICE, max_length=10, default=GENDER_CHOICE[2][0])
    # unique 唯一
    email = models.CharField('邮箱', max_length=100, unique=True)
    # default 默认
    # 用python内置的时间模块，django会自动减八个小时
    # 最好用django自带的timezone.now生成当前时间，注意不要加小括号
    register_time = models.DateTimeField('注册日期', default=timezone.now)
    # phone
    # last_login_time
    # # 状态字段
    # is_active

    def __str__(self):
        # 默认<class User>  重写此方法可以在调试时看到实例的name属性
        return '<class User>{}'.format(self.name)

    class Meta:
        # 自定义表名
        # db_table = ''      # 默认生成 模块名_类名的表 如：login_user
        # ordering = [''id]  # 相当于 group by
        verbose_name = "用户表"
