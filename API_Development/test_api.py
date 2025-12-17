"""
API Testing Script
Demonstrates: Testing REST API endpoints, HTTP requests, response validation
"""

import requests
import json
from pprint import pprint

# Base URL for the API
BASE_URL = 'http://localhost:5000/api'

class APITester:
    """Test client for Employee Management API"""
    
    def __init__(self, base_url):
        self.base_url = base_url
        
    def print_response(self, response, title="Response"):
        """Pretty print API response"""
        print("\n" + "=" * 60)
        print(f"{title}")
        print("=" * 60)
        print(f"Status Code: {response.status_code}")
        print(f"Response:")
        pprint(response.json())
    
    def test_get_all_employees(self):
        """Test GET /api/employees"""
        print("\n🧪 Testing: GET all employees")
        response = requests.get(f"{self.base_url}/employees")
        self.print_response(response, "GET All Employees")
        return response
    
    def test_get_employee_by_id(self, employee_id):
        """Test GET /api/employees/<id>"""
        print(f"\n🧪 Testing: GET employee by ID {employee_id}")
        response = requests.get(f"{self.base_url}/employees/{employee_id}")
        self.print_response(response, f"GET Employee ID {employee_id}")
        return response
    
    def test_create_employee(self, employee_data):
        """Test POST /api/employees"""
        print("\n🧪 Testing: POST create new employee")
        response = requests.post(
            f"{self.base_url}/employees",
            json=employee_data,
            headers={'Content-Type': 'application/json'}
        )
        self.print_response(response, "POST Create Employee")
        return response
    
    def test_update_employee(self, employee_id, update_data):
        """Test PUT /api/employees/<id>"""
        print(f"\n🧪 Testing: PUT update employee {employee_id}")
        response = requests.put(
            f"{self.base_url}/employees/{employee_id}",
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        self.print_response(response, f"PUT Update Employee {employee_id}")
        return response
    
    def test_delete_employee(self, employee_id):
        """Test DELETE /api/employees/<id>"""
        print(f"\n🧪 Testing: DELETE employee {employee_id}")
        response = requests.delete(f"{self.base_url}/employees/{employee_id}")
        self.print_response(response, f"DELETE Employee {employee_id}")
        return response
    
    def test_get_by_department(self, department):
        """Test GET /api/employees/department/<dept>"""
        print(f"\n🧪 Testing: GET employees in {department}")
        response = requests.get(f"{self.base_url}/employees/department/{department}")
        self.print_response(response, f"GET Employees in {department}")
        return response
    
    def test_get_statistics(self):
        """Test GET /api/statistics"""
        print("\n🧪 Testing: GET statistics")
        response = requests.get(f"{self.base_url}/statistics")
        self.print_response(response, "GET Statistics")
        return response
    
    def test_search_employees(self, query, min_salary=None, max_salary=None):
        """Test GET /api/employees/search"""
        print(f"\n🧪 Testing: SEARCH employees with query '{query}'")
        params = {'q': query}
        if min_salary:
            params['minSalary'] = min_salary
        if max_salary:
            params['maxSalary'] = max_salary
        
        response = requests.get(f"{self.base_url}/employees/search", params=params)
        self.print_response(response, "SEARCH Employees")
        return response
    
    def test_filtering_and_sorting(self):
        """Test GET /api/employees with filters and sorting"""
        print("\n🧪 Testing: GET employees with filters and sorting")
        params = {
            'department': 'IT',
            'sort': 'salary',
            'order': 'desc'
        }
        response = requests.get(f"{self.base_url}/employees", params=params)
        self.print_response(response, "GET Filtered & Sorted Employees")
        return response

def run_all_tests():
    """Run comprehensive API tests"""
    print("\n" + "=" * 60)
    print("EMPLOYEE MANAGEMENT API - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print("Make sure the API server is running on http://localhost:5000")
    print("=" * 60)
    
    tester = APITester(BASE_URL)
    
    try:
        # Test 1: Get all employees
        tester.test_get_all_employees()
        
        # Test 2: Get specific employee
        tester.test_get_employee_by_id(1)
        
        # Test 3: Get by department
        tester.test_get_by_department('IT')
        
        # Test 4: Get statistics
        tester.test_get_statistics()
        
        # Test 5: Create new employee
        new_employee = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'john.doe@company.com',
            'department': 'Finance',
            'salary': 88000,
            'hireDate': '2024-01-01'
        }
        create_response = tester.test_create_employee(new_employee)
        
        # Get the new employee ID from response
        if create_response.status_code == 201:
            new_employee_id = create_response.json()['data']['id']
            
            # Test 6: Update the employee
            update_data = {
                'salary': 92000,
                'department': 'IT'
            }
            tester.test_update_employee(new_employee_id, update_data)
            
            # Test 7: Verify update
            tester.test_get_employee_by_id(new_employee_id)
            
            # Test 8: Delete the employee
            tester.test_delete_employee(new_employee_id)
            
            # Test 9: Verify deletion
            tester.test_get_employee_by_id(new_employee_id)
        
        # Test 10: Search employees
        tester.test_search_employees('sarah')
        
        # Test 11: Search with salary range
        tester.test_search_employees('', min_salary=80000, max_salary=100000)
        
        # Test 12: Filtering and sorting
        tester.test_filtering_and_sorting()
        
        # Test 13: Error handling - invalid ID
        tester.test_get_employee_by_id(9999)
        
        # Test 14: Error handling - invalid data
        invalid_employee = {
            'firstName': 'Invalid',
            'lastName': 'Employee',
            'email': 'not-an-email',  # Invalid email
            'department': 'InvalidDept',  # Invalid department
            'salary': -5000  # Negative salary
        }
        tester.test_create_employee(invalid_employee)
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API server")
        print("Make sure the API is running: python api_flask.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    run_all_tests()
