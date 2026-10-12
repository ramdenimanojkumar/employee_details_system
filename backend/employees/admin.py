from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('emp_id', 'name', 'department', 'designation', 'email', 'phone', 'created_at')
    search_fields = ('emp_id', 'name', 'department', 'email')
    list_filter = ('department', 'designation', 'created_at')
    ordering = ('emp_id',)
