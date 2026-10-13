from django.db import models

class Employee(models.Model):
    """
    Employee model where emp_id is the primary key.
    Stores all employee details submitted from the frontend.
    """
    emp_id = models.CharField(
        max_length=50,
        primary_key=True,
        help_text="Unique Employee ID (Primary Key)"
    )
    name = models.CharField(max_length=150, help_text="Full Name of the Employee")
    department = models.CharField(max_length=100, help_text="Department Name")
    designation = models.CharField(max_length=100, help_text="Job Designation / Title")
    email = models.EmailField(
        max_length=150,
        unique=True,
        help_text="Unique Email Address for the Employee"
    )
    phone = models.CharField(max_length=30, blank=True, null=True, help_text="Contact Phone Number")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employees_employee'
        ordering = ['emp_id']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def save(self, *args, **kwargs):
        # Normalize emp_id and email
        if self.emp_id:
            self.emp_id = self.emp_id.strip()
        if self.email:
            self.email = self.email.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.emp_id} - {self.name}"
