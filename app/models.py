from django.db import models
from django.utils import timezone
from adminsortable.models import SortableMixin


class UserCase(models.Model):
    """
    测试用例
    """
    code = models.CharField('用例编号', max_length=20)
    name = models.CharField('用例名称', max_length=60)
    # url = models.CharField('用例网址', max_length=100, blank=True, null=True)
    case_xml = models.TextField('导入脚本内容', help_text='', blank=True, null=True)

    class Meta:
        verbose_name = '测试用例'
        verbose_name_plural = '测试用例管理'

    def __str__(self):
        return "(%s)%s" % (self.code, self.name)


class UserCaseResult(models.Model):

    STATUS_CHOICES = (
        (0, '未开始'),
        (1, '进行中'),
        (2, '失败'),
        (3, '成功')
    )
    user_case = models.ForeignKey(UserCase, verbose_name='用例名称', related_name='results', on_delete=models.PROTECT)
    assert_num = models.SmallIntegerField('测试点', default=0)
    assert_success_num = models.SmallIntegerField('测试通过数', default=0)
    fail_reason = models.TextField('失败描述', blank=True, null=True)
    status = models.PositiveSmallIntegerField('状态', choices=STATUS_CHOICES, default=0)
    created = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '用例输出'
        verbose_name_plural = '用例输出管理'

    def __str__(self):
        return self.user_case.name


class UserCaseResultStep(models.Model):

    STATUS_CHOICES = (
        (0, '失败'),
        (1, '成功')
    )
    user_case_result = models.ForeignKey(UserCaseResult, verbose_name='用例结果输出', on_delete=models.PROTECT)
    step_name = models.CharField('备注名', max_length=20, blank=True, null=True)
    status = models.PositiveSmallIntegerField('状态', choices=STATUS_CHOICES, default=0)
    remark = models.CharField('备注', max_length=250, blank=True, null=True)
    screenshot = models.TextField('截图', blank=True, null=True)

    class Meta:
        verbose_name = '用例输出步骤'


class UserCaseStep(models.Model):
    """
    测试用例步骤
    """
    STEP_TYPE_INPUT = 1
    STEP_TYPE_CLICK = 2
    STEP_TYPE_ASSERT = 3
    STEP_TYPE_OPEN = 4

    @classmethod
    def get_step_type(cls, command):
        if command == 'open':
            return cls.STEP_TYPE_OPEN
        elif command == 'click' or command == 'doubleClick':
            return cls.STEP_TYPE_CLICK
        elif command == 'type':
            return cls.STEP_TYPE_INPUT

    STEP_TYPE_CHOICES = (
        (STEP_TYPE_INPUT, '输入'),
        (STEP_TYPE_CLICK, '点击'),
        (STEP_TYPE_ASSERT, '匹配'),
        (STEP_TYPE_OPEN, '打开'),
    )
    user_case = models.ForeignKey(UserCase, related_name='steps', on_delete=models.PROTECT)
    name = models.CharField('备注名', max_length=20, blank=True, null=True)
    xpath = models.CharField('目标', help_text='用于找到对象', max_length=100, blank=True, null=True)
    step_type = models.SmallIntegerField('类型', choices=STEP_TYPE_CHOICES, default=0)
    step_text = models.CharField('输入值', max_length=100, blank=True, null=True)
    pause_seconds = models.PositiveSmallIntegerField('暂停时间', help_text='单位秒', default=0)
    sort_order = models.IntegerField('排序', default=0, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例步骤'
        verbose_name_plural = '用例步骤管理'
        ordering = ['sort_order']