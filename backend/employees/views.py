from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for managing Employees:
    - POST   /api/employees/          -> Store/Create/Update an employee
    - GET    /api/employees/<emp_id>/ -> Retrieve employee by primary key (emp_id)
    - GET    /api/employees/          -> List all employees (supports ?emp_id=...)
    - PUT    /api/employees/<emp_id>/ -> Full update
    - PATCH  /api/employees/<emp_id>/ -> Partial update
    - DELETE /api/employees/<emp_id>/ -> Delete employee
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'emp_id'
    lookup_value_regex = '[^/]+'  # Support employee IDs with dashes, dots, etc.

    def get_queryset(self):
        queryset = super().get_queryset()
        emp_id = self.request.query_params.get('emp_id')
        if emp_id:
            queryset = queryset.filter(emp_id__iexact=emp_id.strip())
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Store an employee. If an employee with the same emp_id already exists,
        updates the record gracefully (upsert behavior).
        """
        data = request.data
        emp_id = data.get('emp_id') or data.get('employeeId') or data.get('employee_id')

        if emp_id and isinstance(emp_id, str):
            emp_id = emp_id.strip()
            existing_employee = Employee.objects.filter(emp_id__iexact=emp_id).first()
            if existing_employee:
                serializer = self.get_serializer(existing_employee, data=data, partial=False)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(
                    {
                        "message": f"Employee '{existing_employee.emp_id}' details updated successfully.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "message": f"Employee '{serializer.data.get('emp_id')}' stored successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve employee details by emp_id primary key.
        Provides a clear, beginner-friendly error message if not found.
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        emp_id_val = self.kwargs.get(lookup_url_kwarg, '').strip()

        # Case-insensitive primary key lookup for better user experience
        employee = Employee.objects.filter(emp_id__iexact=emp_id_val).first()
        if not employee:
            return Response(
                {"error": f"No employee record found for Employee ID: '{emp_id_val}'"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(employee)
        return Response(
            {
                "message": f"Employee '{employee.emp_id}' retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
