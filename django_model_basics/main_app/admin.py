from django.contrib import admin

from main_app.models import Employee, Department


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class EmployeeAdmin(admin.ModelAdmin):
    pass
