"""
REST API Example using Flask
Demonstrates: RESTful API design, HTTP methods, JSON responses, error handling
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# In-memory database (in production, use actual database)
employees_db = [
    {
        'id': 1,
        'firstName': 'Sarah',
        'lastName': 'Johnson',
        'email': 'sarah.johnson@company.com',
        'department': 'IT',
        'salary': 95000,
        'hireDate': '2020-01-15'
    },
    {
        'id': 2,
        'firstName': 'Michael',
        'lastName': 'Chen',
        'email': 'michael.chen@company.com',
        'department': 'IT',
        'salary': 87000,
        'hireDate': '2020-03-22'
    },
    {
        'id': 3,
        'firstName': 'Emily',
        'lastName': 'Rodriguez',
        'email': 'emily.rodriguez@company.com',
        'department': 'HR',
        'salary': 72000,
        'hireDate': '2019-07-10'
    }
]

# Counter for generating new IDs
next_id = 4

# =============================================
# Helper Functions
# =============================================

def find_employee(employee_id):
    """Find employee by ID"""
    return next((emp for emp in employees_db if emp['id'] == employee_id), None)

def validate_employee_data(data, is_update=False):
    """Validate employee data"""
    errors = []
    
    required_fields = ['firstName', 'lastName', 'email', 'department', 'salary']
    
    if not is_update:
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
    
    if 'email' in data and '@' not in data['email']:
        errors.append("Invalid email format")
    
    if 'salary' in data and (not isinstance(data['salary'], (int, float)) or data['salary'] < 0):
        errors.append("Salary must be a positive number")
    
    valid_departments = ['IT', 'HR', 'Finance', 'Marketing', 'Operations']
    if 'department' in data and data['department'] not in valid_departments:
        errors.append(f"Department must be one of: {', '.join(valid_departments)}")
    
    return errors

def create_response(data=None, message=None, status_code=200):
    """Create standardized API response"""
    response = {}
    
    if data is not None:
        response['data'] = data
    
    if message:
        response['message'] = message
    
    response['success'] = 200 <= status_code < 300
    response['timestamp'] = datetime.now().isoformat()
    
    return jsonify(response), status_code

# =============================================
# API Endpoints
# =============================================

@app.route('/')
def home():
    """API Documentation"""
    return jsonify({
        'name': 'Employee Management API',
        'version': '1.0.0',
        'description': 'RESTful API for employee management',
        'endpoints': {
            'GET /api/employees': 'Get all employees',
            'GET /api/employees/<id>': 'Get employee by ID',
            'POST /api/employees': 'Create new employee',
            'PUT /api/employees/<id>': 'Update employee',
            'DELETE /api/employees/<id>': 'Delete employee',
            'GET /api/employees/department/<dept>': 'Get employees by department',
            'GET /api/statistics': 'Get statistics'
        }
    })

@app.route('/api/employees', methods=['GET'])
def get_employees():
    """
    GET /api/employees
    Query parameters:
    - department: Filter by department
    - sort: Sort by field (salary, hireDate)
    - order: Sort order (asc, desc)
    """
    employees = employees_db.copy()
    
    # Filter by department
    department = request.args.get('department')
    if department:
        employees = [emp for emp in employees if emp['department'] == department]
    
    # Sort
    sort_by = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')
    
    if sort_by in ['salary', 'hireDate', 'id']:
        employees.sort(
            key=lambda x: x.get(sort_by, 0),
            reverse=(order == 'desc')
        )
    
    return create_response(
        data=employees,
        message=f"Retrieved {len(employees)} employees"
    )

@app.route('/api/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    """GET /api/employees/<id> - Get single employee"""
    employee = find_employee(employee_id)
    
    if not employee:
        return create_response(
            message=f"Employee with ID {employee_id} not found",
            status_code=404
        )
    
    return create_response(data=employee)

@app.route('/api/employees', methods=['POST'])
def create_employee():
    """
    POST /api/employees
    Create new employee
    Request body: JSON with employee data
    """
    global next_id
    
    if not request.json:
        return create_response(
            message="Request body must be JSON",
            status_code=400
        )
    
    # Validate data
    errors = validate_employee_data(request.json)
    if errors:
        return create_response(
            data={'errors': errors},
            message="Validation failed",
            status_code=400
        )
    
    # Create new employee
    new_employee = {
        'id': next_id,
        'firstName': request.json['firstName'],
        'lastName': request.json['lastName'],
        'email': request.json['email'],
        'department': request.json['department'],
        'salary': request.json['salary'],
        'hireDate': request.json.get('hireDate', datetime.now().strftime('%Y-%m-%d'))
    }
    
    employees_db.append(new_employee)
    next_id += 1
    
    return create_response(
        data=new_employee,
        message="Employee created successfully",
        status_code=201
    )

@app.route('/api/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """PUT /api/employees/<id> - Update employee"""
    employee = find_employee(employee_id)
    
    if not employee:
        return create_response(
            message=f"Employee with ID {employee_id} not found",
            status_code=404
        )
    
    if not request.json:
        return create_response(
            message="Request body must be JSON",
            status_code=400
        )
    
    # Validate data
    errors = validate_employee_data(request.json, is_update=True)
    if errors:
        return create_response(
            data={'errors': errors},
            message="Validation failed",
            status_code=400
        )
    
    # Update employee
    for key, value in request.json.items():
        if key != 'id':  # Don't allow ID changes
            employee[key] = value
    
    return create_response(
        data=employee,
        message="Employee updated successfully"
    )

@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """DELETE /api/employees/<id> - Delete employee"""
    employee = find_employee(employee_id)
    
    if not employee:
        return create_response(
            message=f"Employee with ID {employee_id} not found",
            status_code=404
        )
    
    employees_db.remove(employee)
    
    return create_response(
        message=f"Employee {employee_id} deleted successfully"
    )

@app.route('/api/employees/department/<department>', methods=['GET'])
def get_employees_by_department(department):
    """GET /api/employees/department/<dept> - Get employees by department"""
    employees = [emp for emp in employees_db if emp['department'] == department]
    
    if not employees:
        return create_response(
            data=[],
            message=f"No employees found in {department} department"
        )
    
    return create_response(
        data=employees,
        message=f"Found {len(employees)} employees in {department}"
    )

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """GET /api/statistics - Get employee statistics"""
    if not employees_db:
        return create_response(
            data={
                'totalEmployees': 0,
                'averageSalary': 0,
                'departmentCounts': {},
                'salaryRange': {'min': 0, 'max': 0}
            }
        )
    
    # Calculate statistics
    salaries = [emp['salary'] for emp in employees_db]
    departments = {}
    
    for emp in employees_db:
        dept = emp['department']
        departments[dept] = departments.get(dept, 0) + 1
    
    statistics = {
        'totalEmployees': len(employees_db),
        'averageSalary': sum(salaries) / len(salaries),
        'departmentCounts': departments,
        'salaryRange': {
            'min': min(salaries),
            'max': max(salaries)
        },
        'departmentStats': []
    }
    
    # Department-specific stats
    for dept in set(emp['department'] for emp in employees_db):
        dept_employees = [emp for emp in employees_db if emp['department'] == dept]
        dept_salaries = [emp['salary'] for emp in dept_employees]
        
        statistics['departmentStats'].append({
            'department': dept,
            'count': len(dept_employees),
            'averageSalary': sum(dept_salaries) / len(dept_salaries),
            'totalPayroll': sum(dept_salaries)
        })
    
    return create_response(data=statistics)

@app.route('/api/employees/search', methods=['GET'])
def search_employees():
    """
    GET /api/employees/search
    Query parameters:
    - q: Search query (searches name and email)
    - minSalary: Minimum salary
    - maxSalary: Maximum salary
    """
    query = request.args.get('q', '').lower()
    min_salary = request.args.get('minSalary', type=float)
    max_salary = request.args.get('maxSalary', type=float)
    
    results = employees_db.copy()
    
    # Text search
    if query:
        results = [
            emp for emp in results
            if query in emp['firstName'].lower() or
               query in emp['lastName'].lower() or
               query in emp['email'].lower()
        ]
    
    # Salary range
    if min_salary is not None:
        results = [emp for emp in results if emp['salary'] >= min_salary]
    
    if max_salary is not None:
        results = [emp for emp in results if emp['salary'] <= max_salary]
    
    return create_response(
        data=results,
        message=f"Found {len(results)} employees matching criteria"
    )

# =============================================
# Error Handlers
# =============================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return create_response(
        message="Resource not found",
        status_code=404
    )

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return create_response(
        message="Internal server error",
        status_code=500
    )

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return create_response(
        message="Bad request",
        status_code=400
    )

# =============================================
# Run Application
# =============================================

if __name__ == '__main__':
    print("=" * 60)
    print("Employee Management API")
    print("=" * 60)
    print("API is running on: http://localhost:5000")
    print("Documentation: http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, port=5000)
