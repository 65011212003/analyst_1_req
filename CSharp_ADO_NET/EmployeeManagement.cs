using System;
using System.Data;
using Microsoft.Data.Sqlite;

namespace EmployeeManagement
{
    /// <summary>
    /// Demonstrates ADO.NET database operations with C#
    /// Covers: Connection management, CRUD operations, queries, transactions
    /// </summary>
    public class EmployeeRepository
    {
        private readonly string _connectionString;

        public EmployeeRepository(string connectionString)
        {
            _connectionString = connectionString;
            InitializeDatabase();
        }

        /// <summary>
        /// Creates the database schema if it doesn't exist
        /// </summary>
        private void InitializeDatabase()
        {
            using (SqliteConnection connection = new SqliteConnection(_connectionString))
            {
                connection.Open();

                string createEmployeesTable = @"
                    CREATE TABLE IF NOT EXISTS Employees (
                        EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
                        FirstName TEXT NOT NULL,
                        LastName TEXT NOT NULL,
                        Email TEXT NOT NULL,
                        Department TEXT NOT NULL,
                        Salary REAL NOT NULL,
                        HireDate TEXT NOT NULL
                    )";

                string createLogTable = @"
                    CREATE TABLE IF NOT EXISTS DepartmentTransferLog (
                        LogID INTEGER PRIMARY KEY AUTOINCREMENT,
                        EmployeeID INTEGER NOT NULL,
                        NewDepartment TEXT NOT NULL,
                        TransferDate TEXT NOT NULL
                    )";

                using (SqliteCommand command = new SqliteCommand(createEmployeesTable, connection))
                {
                    command.ExecuteNonQuery();
                }

                using (SqliteCommand command = new SqliteCommand(createLogTable, connection))
                {
                    command.ExecuteNonQuery();
                }

                // Insert sample data if table is empty
                string countQuery = "SELECT COUNT(*) FROM Employees";
                using (SqliteCommand command = new SqliteCommand(countQuery, connection))
                {
                    long count = (long)command.ExecuteScalar();
                    if (count == 0)
                    {
                        InsertSampleData(connection);
                    }
                }
            }
        }

        private void InsertSampleData(SqliteConnection connection)
        {
            string[] sampleData = new string[]
            {
                "INSERT INTO Employees (FirstName, LastName, Email, Department, Salary, HireDate) VALUES ('Alice', 'Johnson', 'alice.johnson@company.com', 'IT', 85000, '2022-01-15')",
                "INSERT INTO Employees (FirstName, LastName, Email, Department, Salary, HireDate) VALUES ('Bob', 'Smith', 'bob.smith@company.com', 'HR', 65000, '2021-03-20')",
                "INSERT INTO Employees (FirstName, LastName, Email, Department, Salary, HireDate) VALUES ('Carol', 'Williams', 'carol.williams@company.com', 'IT', 95000, '2020-06-10')",
                "INSERT INTO Employees (FirstName, LastName, Email, Department, Salary, HireDate) VALUES ('David', 'Brown', 'david.brown@company.com', 'Finance', 78000, '2023-02-28')"
            };

            foreach (string sql in sampleData)
            {
                using (SqliteCommand command = new SqliteCommand(sql, connection))
                {
                    command.ExecuteNonQuery();
                }
            }
        }

        #region Basic CRUD Operations

        /// <summary>
        /// Retrieves all employees from the database
        /// Demonstrates: SqliteConnection, SqliteCommand, SqliteDataReader
        /// </summary>
        public void GetAllEmployees()
        {
            using (SqliteConnection connection = new SqliteConnection(_connectionString))
            {
                try
                {
                    connection.Open();
                    
                    string query = "SELECT EmployeeID, FirstName, LastName, Email, Department FROM Employees";
                    
                    using (SqliteCommand command = new SqliteCommand(query, connection))
                    {
                        using (SqliteDataReader reader = command.ExecuteReader())
                        {
                            Console.WriteLine("Employee List:");
                            Console.WriteLine("ID\tName\t\t\tEmail\t\t\t\tDepartment");
                            Console.WriteLine(new string('-', 80));
                            
                            while (reader.Read())
                            {
                                long id = reader.GetInt64(0);
                                string firstName = reader.GetString(1);
                                string lastName = reader.GetString(2);
                                string email = reader.GetString(3);
                                string department = reader.GetString(4);
                                
                                Console.WriteLine($"{id}\t{firstName} {lastName}\t\t{email}\t\t{department}");
                            }
                        }
                    }
                }
                catch (SqliteException ex)
                {
                    Console.WriteLine($"Database error: {ex.Message}");
                }
            }
        }

        /// <summary>
        /// Inserts a new employee using parameterized queries to prevent SQL injection
        /// Demonstrates: SqliteParameter, ExecuteNonQuery, SQL injection prevention
        /// </summary>
        public int InsertEmployee(string firstName, string lastName, string email, string department, decimal salary)
        {
            using (SqliteConnection connection = new SqliteConnection(_connectionString))
            {
                string query = @"INSERT INTO Employees (FirstName, LastName, Email, Department, Salary, HireDate)
                               VALUES (@FirstName, @LastName, @Email, @Department, @Salary, @HireDate);
                               SELECT last_insert_rowid();";

                using (SqliteCommand command = new SqliteCommand(query, connection))
                {
                    // Use parameters to prevent SQL injection
                    command.Parameters.AddWithValue("@FirstName", firstName);
                    command.Parameters.AddWithValue("@LastName", lastName);
                    command.Parameters.AddWithValue("@Email", email);
                    command.Parameters.AddWithValue("@Department", department);
                    command.Parameters.AddWithValue("@Salary", (double)salary);
                    command.Parameters.AddWithValue("@HireDate", DateTime.Now.ToString("yyyy-MM-dd"));

                    try
                    {
                        connection.Open();
                        long newEmployeeId = (long)command.ExecuteScalar();
                        Console.WriteLine($"Employee inserted successfully with ID: {newEmployeeId}");
                        return (int)newEmployeeId;
                    }
                    catch (SqliteException ex)
                    {
                        Console.WriteLine($"Error inserting employee: {ex.Message}");
                        return -1;
                    }
                }
            }
        }

        /// <summary>
        /// Updates employee information
        /// Demonstrates: UPDATE operations with parameters
        /// </summary>
        public bool UpdateEmployee(int employeeId, string email, string department)
        {
            using (SqliteConnection connection = new SqliteConnection(_connectionString))
            {
                string query = @"UPDATE Employees 
                               SET Email = @Email, Department = @Department 
                               WHERE EmployeeID = @EmployeeID";

                using (SqliteCommand command = new SqliteCommand(query, connection))
                {
                    command.Parameters.AddWithValue("@EmployeeID", employeeId);
                    command.Parameters.AddWithValue("@Email", email);
                    command.Parameters.AddWithValue("@Department", department);

                    try
                    {
                        connection.Open();
                        int rowsAffected = command.ExecuteNonQuery();
                        Console.WriteLine($"Updated {rowsAffected} employee(s)");
                        return rowsAffected > 0;
                    }
                    catch (SqliteException ex)
                    {
                        Console.WriteLine($"Error updating employee: {ex.Message}");
                        return false;
                    }
                }
            }
        }

        /// <summary>
        /// Deletes an employee
        /// Demonstrates: DELETE operations
        /// </summary>
        public bool DeleteEmployee(int employeeId)
        {
            using (SqliteConnection connection = new SqliteConnection(_connectionString))
            {
                string query = "DELETE FROM Employees WHERE EmployeeID = @EmployeeID";

                using (SqliteCommand command = new SqliteCommand(query, connection))
                {
                    command.Parameters.AddWithValue("@EmployeeID", employeeId);

                    try
                    {
                        connection.Open();
                        int rowsAffected = command.ExecuteNonQuery();
                        return rowsAffected > 0;
                    }
                    catch (SqliteException ex)
                    {
                        Console.WriteLine($"Error deleting employee: {ex.Message}");
                        return false;
                    }
                }
            }
        }

        #endregion

        #region Query Methods

        /// <summary>
        /// Gets employees by department using parameterized query
        /// Note: SQLite doesn't support stored procedures, so we use regular queries
        /// </summary>
        public void GetEmployeesByDepartment(string department)
        {
            using (SqliteConnection connection = new SqliteConnection(_connectionString))
            {
                string query = "SELECT FirstName, LastName, Email FROM Employees WHERE Department = @Department";
                using (SqliteCommand command = new SqliteCommand(query, connection))
                {
                    command.Parameters.AddWithValue("@Department", department);

                    try
                    {
                        connection.Open();
                        using (SqliteDataReader reader = command.ExecuteReader())
                        {
                            Console.WriteLine($"Employees in {department} Department:");
                            int count = 0;
                            while (reader.Read())
                            {
                                Console.WriteLine($"  {reader["FirstName"]} {reader["LastName"]} - {reader["Email"]}");
                                count++;
                            }
                            if (count == 0)
                            {
                                Console.WriteLine($"  No employees found in {department} department");
                            }
                        }
                    }
                    catch (SqliteException ex)
                    {
                        Console.WriteLine($"Error executing query: {ex.Message}");
                    }
                }
            }
        }

        /// <summary>
        /// Gets average salary by department
        /// Note: SQLite doesn't support stored procedures with output parameters
        /// </summary>
        public decimal GetAverageSalaryByDepartment(string department)
        {
            using (SqliteConnection connection = new SqliteConnection(_connectionString))
            {
                string query = "SELECT AVG(Salary) FROM Employees WHERE Department = @Department";
                using (SqliteCommand command = new SqliteCommand(query, connection))
                {
                    command.Parameters.AddWithValue("@Department", department);

                    try
                    {
                        connection.Open();
                        object result = command.ExecuteScalar();
                        
                        if (result != null && result != DBNull.Value)
                        {
                            decimal avgSalary = Convert.ToDecimal(result);
                            Console.WriteLine($"Average salary in {department}: ${avgSalary:N2}");
                            return avgSalary;
                        }
                        else
                        {
                            Console.WriteLine($"No employees found in {department} department");
                            return 0;
                        }
                    }
                    catch (SqliteException ex)
                    {
                        Console.WriteLine($"Error: {ex.Message}");
                        return 0;
                    }
                }
            }
        }

        #endregion

        #region Transactions

        /// <summary>
        /// Demonstrates transaction handling with ADO.NET
        /// Shows: BeginTransaction, Commit, Rollback
        /// </summary>
        public bool TransferDepartment(int employeeId, string newDepartment)
        {
            using (SqliteConnection connection = new SqliteConnection(_connectionString))
            {
                connection.Open();
                SqliteTransaction transaction = connection.BeginTransaction();

                try
                {
                    // Update employee department
                    string updateQuery = "UPDATE Employees SET Department = @NewDepartment WHERE EmployeeID = @EmployeeID";
                    using (SqliteCommand updateCmd = new SqliteCommand(updateQuery, connection, transaction))
                    {
                        updateCmd.Parameters.AddWithValue("@NewDepartment", newDepartment);
                        updateCmd.Parameters.AddWithValue("@EmployeeID", employeeId);
                        updateCmd.ExecuteNonQuery();
                    }

                    // Log the transfer
                    string logQuery = "INSERT INTO DepartmentTransferLog (EmployeeID, NewDepartment, TransferDate) VALUES (@EmployeeID, @NewDepartment, @TransferDate)";
                    using (SqliteCommand logCmd = new SqliteCommand(logQuery, connection, transaction))
                    {
                        logCmd.Parameters.AddWithValue("@EmployeeID", employeeId);
                        logCmd.Parameters.AddWithValue("@NewDepartment", newDepartment);
                        logCmd.Parameters.AddWithValue("@TransferDate", DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
                        logCmd.ExecuteNonQuery();
                    }

                    // Commit transaction
                    transaction.Commit();
                    Console.WriteLine("Department transfer completed successfully.");
                    return true;
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error during transfer: {ex.Message}");
                    try
                    {
                        transaction.Rollback();
                        Console.WriteLine("Transaction rolled back.");
                    }
                    catch (Exception rollbackEx)
                    {
                        Console.WriteLine($"Rollback error: {rollbackEx.Message}");
                    }
                    return false;
                }
            }
        }

        #endregion

        #region DataTable

        /// <summary>
        /// Demonstrates working with DataTables
        /// Shows: Manual DataTable population from DataReader
        /// </summary>
        public DataTable? GetEmployeesAsDataTable()
        {
            using (SqliteConnection connection = new SqliteConnection(_connectionString))
            {
                string query = "SELECT EmployeeID, FirstName, LastName, Email, Department, Salary FROM Employees";
                DataTable employeeTable = new DataTable("Employees");

                try
                {
                    connection.Open();
                    
                    using (SqliteCommand command = new SqliteCommand(query, connection))
                    {
                        using (SqliteDataReader reader = command.ExecuteReader())
                        {
                            employeeTable.Load(reader);
                        }
                    }
                    
                    Console.WriteLine($"Retrieved {employeeTable.Rows.Count} employees into DataTable");
                    
                    // Display the data
                    foreach (DataRow row in employeeTable.Rows)
                    {
                        Console.WriteLine($"  {row["EmployeeID"]}: {row["FirstName"]} {row["LastName"]} - {row["Department"]}");
                    }
                    
                    return employeeTable;
                }
                catch (SqliteException ex)
                {
                    Console.WriteLine($"Error: {ex.Message}");
                    return null;
                }
            }
        }

        #endregion
    }

    /// <summary>
    /// Main program to demonstrate all ADO.NET features
    /// </summary>
    class Program
    {
        static void Main(string[] args)
        {
            // SQLite connection string - creates a local database file
            string connectionString = "Data Source=EmployeeDB.db";
            
            EmployeeRepository repository = new EmployeeRepository(connectionString);

            Console.WriteLine("=== ADO.NET Employee Management System (SQLite) ===\n");

            // Example 1: Get all employees
            Console.WriteLine("1. Getting all employees:");
            repository.GetAllEmployees();

            // Example 2: Insert new employee
            Console.WriteLine("\n2. Inserting new employee:");
            repository.InsertEmployee("John", "Doe", "john.doe@company.com", "IT", 75000);

            // Example 3: Update employee
            Console.WriteLine("\n3. Updating employee:");
            repository.UpdateEmployee(1, "alice.updated@company.com", "Engineering");

            // Example 4: Get employees by department
            Console.WriteLine("\n4. Getting employees by department:");
            repository.GetEmployeesByDepartment("IT");

            // Example 5: Get average salary
            Console.WriteLine("\n5. Getting average salary:");
            repository.GetAverageSalaryByDepartment("IT");

            // Example 6: Transaction example
            Console.WriteLine("\n6. Department transfer (transaction):");
            repository.TransferDepartment(2, "Finance");

            // Example 7: DataTable example
            Console.WriteLine("\n7. Using DataTable:");
            DataTable? dt = repository.GetEmployeesAsDataTable();

            Console.WriteLine("\n=== All operations completed successfully! ===");
            Console.WriteLine("\nPress any key to exit...");
            Console.ReadKey();
        }
    }
}
