from django.contrib import admin
from .models import UserCase, UserCaseStep


@admin.register(UserCase)
class UserCaseAdmin(admin.ModelAdmin):
    pass


@admin.register(UserCaseStep)
class UserCaseStepAdmin(admin.ModelAdmin):
    pass
