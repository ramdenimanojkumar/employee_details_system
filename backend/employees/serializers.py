from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Employee model.
    Seamlessly supports both 'emp_id' and 'employeeId' field names
    for compatibility with the Flutter frontend.
    """
    employeeId = serializers.CharField(source='emp_id', required=False, read_only=False)

    class Meta:
        model = Employee
        fields = [
            'emp_id',
            'employeeId',
            'name',
            'department',
            'designation',
            'email',
            'phone',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def to_internal_value(self, data):
        # Convert QueryDict or immutable dict to mutable dict
        if hasattr(data, 'dict'):
            mutable_data = data.dict()
        elif hasattr(data, 'copy'):
            mutable_data = data.copy()
        else:
            mutable_data = dict(data)

        # Allow frontend to supply either 'employeeId' or 'emp_id' or 'employee_id'
        if not mutable_data.get('emp_id'):
            if mutable_data.get('employeeId'):
                mutable_data['emp_id'] = mutable_data['employeeId']
            elif mutable_data.get('employee_id'):
                mutable_data['emp_id'] = mutable_data['employee_id']

        if 'emp_id' in mutable_data and isinstance(mutable_data['emp_id'], str):
            mutable_data['emp_id'] = mutable_data['emp_id'].strip()

        if 'email' in mutable_data and isinstance(mutable_data['email'], str):
            mutable_data['email'] = mutable_data['email'].strip().lower()

        return super().to_internal_value(mutable_data)

    def validate_emp_id(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Employee ID cannot be empty.")
        return value.strip()

    def validate_email(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Email address is required.")
        return value.strip().lower()

    def validate(self, attrs):
        emp_id = attrs.get('emp_id')
        if not emp_id and self.instance:
            emp_id = self.instance.emp_id

        email = attrs.get('email')
        if email:
            # Check if another employee already has this email
            query = Employee.objects.filter(email__iexact=email)
            if emp_id:
                query = query.exclude(emp_id__iexact=emp_id)
            conflict = query.first()
            if conflict:
                raise serializers.ValidationError({
                    "email": f"Email '{email}' is already registered to employee ID '{conflict.emp_id}'. Both Employee ID and Email must be unique."
                })

        return super().validate(attrs)
