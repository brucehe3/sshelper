from django.db import models
from adminsortable.models import SortableMixin


class UserCase(models.Model):
    """
    测试用例
    """
    code = models.CharField('用例编号', max_length=20)
    name = models.CharField('用例名称', max_length=60)
    url = models.CharField('用例网址', max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = '测试用例'
        verbose_name_plural = '测试用例管理'

    def __str__(self):
        return "(%s)%s" % (self.code, self.name)


class UserCaseStep(models.Model):
    """
    测试用例步骤
    """
    STEP_TYPE_INPUT = 1
    STEP_TYPE_CLICK = 2
    STEP_TYPE_ASSERT = 3

    STEP_TYPE_CHOICES = (
        (1, '输入'),
        (2, '点击'),
        (3, '匹配'),
    )
    user_case = models.ForeignKey(UserCase, related_name='steps', on_delete=models.PROTECT)
    name = models.CharField('备注名', max_length=20, blank=True, null=True)
    xpath = models.CharField('XPATH', help_text='用于找到对象', max_length=100, blank=True, null=True)
    step_type = models.SmallIntegerField('类型', choices=STEP_TYPE_CHOICES, default=0)
    step_text = models.CharField('提交的值', max_length=100, blank=True, null=True)
    pause_seconds = models.PositiveSmallIntegerField('暂停时间', help_text='单位秒', default=1)
    sort_order = models.IntegerField('排序', default=0, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例步骤'
        verbose_name_plural = '用例步骤管理'
        ordering = ['sort_order']