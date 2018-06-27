from django.db import models


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


class UserCaseStep(models.Model):
    """
    测试用例步骤
    """
    STEP_TYPE_CHOICES = (
        (1, '输入'),
        (2, '点击'),
        (3, '匹配'),
    )
    user_case = models.ForeignKey(UserCase, on_delete=models.PROTECT)
    step_type = models.SmallIntegerField('类型', choices=STEP_TYPE_CHOICES, default=0)
    xpath = models.CharField('XPATH', help_text='用于找到对象', max_length=100, blank=True, null=True)
    step_text = models.CharField('提交的值', max_length=100, blank=True, null=True)
    sort_order = models.IntegerField('排序')

    class Meta:
        verbose_name = '用例步骤'
        verbose_name_plural = '用例步骤管理'