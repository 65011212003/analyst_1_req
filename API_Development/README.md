# API Development Examples

RESTful API examples using Python Flask, demonstrating modern API design patterns.

## Files

- **api_flask.py** - Complete REST API implementation with Flask
- **test_api.py** - API testing script with comprehensive test cases
- **requirements.txt** - Python dependencies

## Prerequisites

```bash
pip install -r requirements.txt
```

## Running the API

```bash
# Start the API server
python api_flask.py

# In another terminal, run tests
python test_api.py
```

The API will be available at: `http://localhost:5000`

## API Endpoints

### Employee Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/employees` | Get all employees (supports filtering & sorting) |
| GET | `/api/employees/<id>` | Get employee by ID |
| POST | `/api/employees` | Create new employee |
| PUT | `/api/employees/<id>` | Update employee |
| DELETE | `/api/employees/<id>` | Delete employee |
| GET | `/api/employees/department/<dept>` | Get employees by department |
| GET | `/api/employees/search` | Search employees |
| GET | `/api/statistics` | Get employee statistics |

### Query Parameters

**GET /api/employees**
- `department` - Filter by department
- `sort` - Sort by field (salary, hireDate, id)
- `order` - Sort order (asc, desc)

**GET /api/employees/search**
- `q` - Search query (name, email)
- `minSalary` - Minimum salary filter
- `maxSalary` - Maximum salary filter

## Request Examples

### Get All Employees
```bash
curl http://localhost:5000/api/employees
```

### Get Employee by ID
```bash
curl http://localhost:5000/api/employees/1
```

### Create Employee
```bash
curl -X POST http://localhost:5000/api/employees \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@company.com",
    "department": "IT",
    "salary": 85000
  }'
```

### Update Employee
```bash
curl -X PUT http://localhost:5000/api/employees/1 \
  -H "Content-Type: application/json" \
  -d '{
    "salary": 90000,
    "department": "Finance"
  }'
```

### Delete Employee
```bash
curl -X DELETE http://localhost:5000/api/employees/1
```

### Filter and Sort
```bash
curl "http://localhost:5000/api/employees?department=IT&sort=salary&order=desc"
```

### Search
```bash
curl "http://localhost:5000/api/employees/search?q=john&minSalary=70000"
```

### Get Statistics
```bash
curl http://localhost:5000/api/statistics
```

## Response Format

All responses follow this structure:

```json
{
  "data": {...},
  "message": "Success message",
  "success": true,
  "timestamp": "2024-01-01T12:00:00"
}
```

### Success Response (200)
```json
{
  "data": {
    "id": 1,
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@company.com",
    "department": "IT",
    "salary": 85000,
    "hireDate": "2024-01-01"
  },
  "message": "Employee retrieved successfully",
  "success": true,
  "timestamp": "2024-01-01T12:00:00"
}
```

### Error Response (400, 404, 500)
```json
{
  "message": "Employee not found",
  "success": false,
  "timestamp": "2024-01-01T12:00:00"
}
```

## Key Concepts Demonstrated

### RESTful Design
- ✅ Resource-based URLs
- ✅ HTTP methods (GET, POST, PUT, DELETE)
- ✅ Proper status codes
- ✅ JSON request/response
- ✅ Query parameters for filtering

### Best Practices
- ✅ Input validation
- ✅ Error handling
- ✅ CORS support
- ✅ Consistent response format
- ✅ Clear endpoint naming
- ✅ API documentation
- ✅ RESTful conventions

### HTTP Status Codes
- `200 OK` - Successful GET, PUT
- `201 Created` - Successful POST
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

### Security Considerations (for production)
- Add authentication (JWT, OAuth)
- Rate limiting
- Input sanitization
- HTTPS only
- API keys
- Request validation

## Testing

The `test_api.py` script demonstrates:
- ✅ Complete CRUD operations
- ✅ Query parameter testing
- ✅ Error handling validation
- ✅ Response verification
- ✅ Status code checking

## Python Code Features

### Flask Decorators
```python
@app.route('/api/employees', methods=['GET'])
def get_employees():
    # Handler code
```

### Request Handling
```python
# Get JSON data
data = request.json

# Get query parameters
department = request.args.get('department')
```

### Response Creation
```python
return jsonify({'data': employees}), 200
```

### Error Handling
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404
```

## Integration with Frontend

To use with the web application:

1. Update frontend JavaScript to call API endpoints
2. Replace mock data with API calls
3. Handle async operations with fetch/axios

Example:
```javascript
// Fetch employees
fetch('http://localhost:5000/api/employees')
  .then(response => response.json())
  .then(data => console.log(data));

// Create employee
fetch('http://localhost:5000/api/employees', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(employeeData)
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Next Steps

To enhance this API:
- Add authentication (JWT)
- Connect to real database (PostgreSQL, MySQL)
- Add pagination
- Implement caching (Redis)
- Add API documentation (Swagger/OpenAPI)
- Deploy to cloud (Azure, AWS)
- Add logging and monitoring
- Implement rate limiting
