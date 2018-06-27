from django.contrib import admin
from .models import UserCase, UserCaseStep


class UserCaseStepInline(admin.TabularInline):
    model = UserCaseStep
    # exclude = ('created',)
    # raw_id_fields = ('image',)
    extra = 0

    verbose_name_plural = '用例步骤'


@admin.register(UserCase)
class UserCaseAdmin(admin.ModelAdmin):
    inlines = [UserCaseStepInline, ]


@admin.register(UserCaseStep)
class UserCaseStepAdmin(admin.ModelAdmin):
    pass
