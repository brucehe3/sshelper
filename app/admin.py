from django.contrib import admin
from django import forms
from django.contrib import messages
import django_rq

from .models import UserCase, UserCaseStep, UserCaseResult
from . import tasks
from adminsortable2.admin import SortableInlineAdminMixin
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class UserCaseStepInline(SortableInlineAdminMixin, admin.TabularInline):
    model = UserCaseStep
    # exclude = ('created',)
    # raw_id_fields = ('image',)
    extra = 0

    verbose_name_plural = '用例步骤'


@admin.register(UserCase)
class UserCaseAdmin(admin.ModelAdmin):

    inlines = [UserCaseStepInline, ]

    list_display = ('code', 'name',)

    actions = ('add_result',)

    def add_result(self, request, queryset):
        for q in queryset:
            result = UserCaseResult()
            result.user_case = q
            result.save()

            django_rq.enqueue(tasks.running_test_case, result.id)

        self.message_user(request, "选择的用例提交成功，等待执行测试 请进入【用例输出管理】查看执行结果")

    add_result.short_description = "选择用例进行测试"

    def save_model(self, request, obj, form, change):

        case_xml = ''
        if obj.case_xml:
            case_xml = obj.case_xml
            obj.case_xml = ''

        super().save_model(request, obj, form, change)

        if case_xml:
            try:
                # 导入
                self.parse_case_xml(obj, case_xml)
            except ValueError as e:
                self.message_user(request, str(e), level=messages.ERROR)

    def parse_case_xml(self, obj, case_xml):
        # 取出排序最大值
        last_step = UserCaseStep.objects.filter(user_case=obj).first()
        last_sort_order = 0
        if last_step:
            last_sort_order = last_step.sort_order

        elements = ET.fromstring(case_xml)

        for element in elements.iterfind('selenese'):
            command = element.find('command').text
            target = element.find('target').text
            value = element.find('value').text

            if not (command and target):
                # 没有实际操作  跳过
                continue

            last_sort_order += 1
            step = UserCaseStep()
            step.name = '导入脚本步骤' + str(last_sort_order)
            step.user_case = obj
            step_type = UserCaseStep.get_step_type(command)
            if not step_type:
                raise ValueError('含有未知的操作步骤')
            step.step_type = step_type
            step.sort_order = last_sort_order
            step.xpath = target
            step.step_text = value
            if step.step_type == UserCaseStep.STEP_TYPE_OPEN:
                step.pause_seconds = 5
            step.save()


@admin.register(UserCaseResult)
class UserCaseResultAdmin(admin.ModelAdmin):

    list_display = ('user_case', 'status', 'fail_reason', 'created',)

    def has_add_permission(self, request):
        return False