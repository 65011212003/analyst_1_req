"""
Python Database Connectivity Examples
Demonstrates: SQL Server connection, CRUD operations, pandas integration
"""

import pyodbc
import pandas as pd
from datetime import datetime

class DatabaseConnector:
    """
    Demonstrates database connectivity with Python
    Uses: pyodbc for SQL Server connectivity
    """
    
    def __init__(self, server, database, trusted_connection=True):
        """Initialize database connection"""
        if trusted_connection:
            self.connection_string = (
                f'DRIVER={{SQL Server}};'
                f'SERVER={server};'
                f'DATABASE={database};'
                f'Trusted_Connection=yes;'
            )
        else:
            # Use this for username/password authentication
            # self.connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID=username;PWD=password'
            pass
        
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = pyodbc.connect(self.connection_string)
            print("✓ Database connection established successfully!")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("✓ Database connection closed")
    
    def execute_query(self, query, params=None):
        """
        Execute a SELECT query and return results as DataFrame
        Demonstrates: Cursor operations, parameterized queries
        """
        try:
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Fetch all results
            columns = [column[0] for column in cursor.description]
            results = cursor.fetchall()
            
            # Convert to DataFrame
            df = pd.DataFrame.from_records(results, columns=columns)
            
            cursor.close()
            return df
        
        except Exception as e:
            print(f"Query execution error: {e}")
            return None
    
    def execute_non_query(self, query, params=None):
        """
        Execute INSERT, UPDATE, DELETE queries
        Demonstrates: Data modification, transactions
        """
        try:
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            self.connection.commit()
            rows_affected = cursor.rowcount
            
            cursor.close()
            return rows_affected
        
        except Exception as e:
            self.connection.rollback()
            print(f"Query execution error: {e}")
            return 0
    
    def call_stored_procedure(self, proc_name, params=None):
        """
        Call a stored procedure
        Demonstrates: Stored procedure execution
        """
        try:
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(f"EXEC {proc_name} {','.join(['?'] * len(params))}", params)
            else:
                cursor.execute(f"EXEC {proc_name}")
            
            # Fetch results if any
            if cursor.description:
                columns = [column[0] for column in cursor.description]
                results = cursor.fetchall()
                df = pd.DataFrame.from_records(results, columns=columns)
                cursor.close()
                return df
            else:
                cursor.close()
                return None
        
        except Exception as e:
            print(f"Stored procedure error: {e}")
            return None
    
    def bulk_insert_from_dataframe(self, df, table_name):
        """
        Bulk insert data from a pandas DataFrame
        Demonstrates: Efficient data loading
        """
        try:
            cursor = self.connection.cursor()
            
            # Create INSERT statement
            columns = ', '.join(df.columns)
            placeholders = ', '.join(['?'] * len(df.columns))
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            # Convert DataFrame to list of tuples
            data = [tuple(row) for row in df.values]
            
            # Execute batch insert
            cursor.executemany(insert_query, data)
            self.connection.commit()
            
            print(f"✓ Inserted {len(data)} rows into {table_name}")
            cursor.close()
            return len(data)
        
        except Exception as e:
            self.connection.rollback()
            print(f"Bulk insert error: {e}")
            return 0

# Example usage
def demonstrate_database_operations():
    """Demonstrate various database operations"""
    
    print("=" * 60)
    print("PYTHON DATABASE CONNECTIVITY DEMONSTRATION")
    print("=" * 60)
    
    # Initialize connector
    db = DatabaseConnector(
        server='localhost',
        database='EmployeeDB',
        trusted_connection=True
    )
    
    if not db.connect():
        return
    
    try:
        # Example 1: Simple SELECT query
        print("\n1. Fetching all employees:")
        query = "SELECT TOP 5 EmployeeID, FirstName, LastName, Department, Salary FROM Employees"
        employees = db.execute_query(query)
        print(employees)
        
        # Example 2: Parameterized query
        print("\n2. Fetching employees by department:")
        query = "SELECT * FROM Employees WHERE Department = ?"
        it_employees = db.execute_query(query, ('IT',))
        print(f"Found {len(it_employees)} IT employees")
        
        # Example 3: Aggregate query with pandas
        print("\n3. Department salary statistics:")
        query = """
            SELECT 
                Department,
                COUNT(*) as EmployeeCount,
                AVG(Salary) as AvgSalary,
                MIN(Salary) as MinSalary,
                MAX(Salary) as MaxSalary
            FROM Employees
            GROUP BY Department
        """
        dept_stats = db.execute_query(query)
        print(dept_stats)
        
        # Example 4: Data analysis with pandas
        print("\n4. Analyzing salary distribution:")
        all_employees = db.execute_query("SELECT * FROM Employees")
        
        if all_employees is not None:
            print(f"\nTotal employees: {len(all_employees)}")
            print(f"Average salary: ${all_employees['Salary'].mean():,.2f}")
            print(f"Median salary: ${all_employees['Salary'].median():,.2f}")
            
            # Salary by department
            salary_by_dept = all_employees.groupby('Department')['Salary'].agg(['mean', 'count'])
            print("\nSalary by department:")
            print(salary_by_dept)
        
        # Example 5: INSERT operation
        print("\n5. Inserting new employee:")
        insert_query = """
            INSERT INTO Employees (FirstName, LastName, Email, Department, Salary, HireDate)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = ('John', 'Doe', 'john.doe@company.com', 'IT', 85000, datetime.now())
        rows = db.execute_non_query(insert_query, params)
        print(f"✓ Inserted {rows} row(s)")
        
        # Example 6: UPDATE operation
        print("\n6. Updating employee salary:")
        update_query = "UPDATE Employees SET Salary = Salary * 1.05 WHERE Department = ?"
        rows = db.execute_non_query(update_query, ('IT',))
        print(f"✓ Updated {rows} row(s)")
        
        # Example 7: Calling stored procedure
        print("\n7. Calling stored procedure:")
        proc_result = db.call_stored_procedure('usp_GetEmployeesByDepartment', ('IT',))
        if proc_result is not None:
            print(f"✓ Retrieved {len(proc_result)} employees from stored procedure")
        
    finally:
        db.disconnect()

if __name__ == "__main__":
    demonstrate_database_operations()
