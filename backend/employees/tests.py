from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Employee

class EmployeeAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.emp1 = Employee.objects.create(
            emp_id="EMP001",
            name="John Doe",
            department="Engineering",
            designation="Software Engineer",
            email="john@example.com",
            phone="1234567890"
        )

    def test_create_employee_success(self):
        """Test storing a new employee record via POST /api/employees/"""
        payload = {
            "emp_id": "EMP002",
            "name": "Jane Smith",
            "department": "Human Resources",
            "designation": "HR Manager",
            "email": "jane@example.com",
            "phone": "9876543210"
        }
        response = self.client.post("/api/employees/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Employee.objects.filter(emp_id="EMP002").exists())
        saved = Employee.objects.get(emp_id="EMP002")
        self.assertEqual(saved.name, "Jane Smith")

    def test_create_employee_with_frontend_alias(self):
        """Test storing using 'employeeId' key as sent by the Flutter frontend"""
        payload = {
            "employeeId": "EMP003",
            "name": "Alex Johnson",
            "department": "Finance",
            "designation": "Financial Analyst",
            "email": "alex@example.com",
            "phone": "5551234567"
        }
        response = self.client.post("/api/employees/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Employee.objects.filter(emp_id="EMP003").exists())

    def test_store_existing_employee_updates_gracefully(self):
        """Test re-submitting with existing emp_id updates the record"""
        payload = {
            "emp_id": "EMP001",
            "name": "John Updated",
            "department": "Engineering",
            "designation": "Senior Engineer",
            "email": "john.updated@example.com",
            "phone": "1234567890"
        }
        response = self.client.post("/api/employees/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.emp1.refresh_from_db()
        self.assertEqual(self.emp1.name, "John Updated")
        self.assertEqual(self.emp1.designation, "Senior Engineer")

    def test_retrieve_employee_by_emp_id(self):
        """Test retrieving employee details by emp_id primary key via GET /api/employees/<emp_id>/"""
        response = self.client.get("/api/employees/EMP001/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data["data"]
        self.assertEqual(data["emp_id"], "EMP001")
        self.assertEqual(data["name"], "John Doe")
        self.assertEqual(data["department"], "Engineering")

    def test_retrieve_employee_not_found(self):
        """Test retrieving non-existent emp_id returns 404 with descriptive message"""
        response = self.client.get("/api/employees/NON_EXISTENT_999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_list_all_employees(self):
        """Test listing all employees via GET /api/employees/"""
        response = self.client.get("/api/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
