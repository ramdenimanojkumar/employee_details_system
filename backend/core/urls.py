"""
URL Configuration for Employee Details System backend.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def api_root_info(request):
    return JsonResponse({
        "status": "online",
        "message": "Employee Details System Backend API",
        "endpoints": {
            "employees_list_or_create": "/api/employees/",
            "employee_detail": "/api/employees/<emp_id>/",
            "admin_panel": "/admin/"
        }
    })

urlpatterns = [
    path('', api_root_info, name='api-root-info'),
    path('admin/', admin.site.urls),
    path('api/', include('employees.urls')),
]
