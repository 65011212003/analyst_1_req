using System;
using System.Data;
using System.Data.SqlClient;
using System.Configuration;

namespace EmployeeManagement
{
    /// <summary>
    /// Demonstrates ADO.NET database operations with C#
    /// Covers: Connection management, CRUD operations, stored procedures, transactions
    /// </summary>
    public class EmployeeRepository
    {
        private readonly string _connectionString;

        public EmployeeRepository(string connectionString)
        {
            _connectionString = connectionString;
        }

        #region Basic CRUD Operations

        /// <summary>
        /// Retrieves all employees from the database
        /// Demonstrates: SqlConnection, SqlCommand, SqlDataReader
        /// </summary>
        public void GetAllEmployees()
        {
            using (SqlConnection connection = new SqlConnection(_connectionString))
            {
                try
                {
                    connection.Open();
                    
                    string query = "SELECT EmployeeID, FirstName, LastName, Email, Department FROM Employees";
                    
                    using (SqlCommand command = new SqlCommand(query, connection))
                    {
                        using (SqlDataReader reader = command.ExecuteReader())
                        {
                            Console.WriteLine("Employee List:");
                            Console.WriteLine("ID\tName\t\t\tEmail\t\t\tDepartment");
                            Console.WriteLine(new string('-', 80));
                            
                            while (reader.Read())
                            {
                                int id = reader.GetInt32(0);
                                string firstName = reader.GetString(1);
                                string lastName = reader.GetString(2);
                                string email = reader.GetString(3);
                                string department = reader.GetString(4);
                                
                                Console.WriteLine($"{id}\t{firstName} {lastName}\t{email}\t{department}");
                            }
                        }
                    }
                }
                catch (SqlException ex)
                {
                    Console.WriteLine($"Database error: {ex.Message}");
                }
            }
        }

        /// <summary>
        /// Inserts a new employee using parameterized queries to prevent SQL injection
        /// Demonstrates: SqlParameter, ExecuteNonQuery, SQL injection prevention
        /// </summary>
        public int InsertEmployee(string firstName, string lastName, string email, string department, decimal salary)
        {
            using (SqlConnection connection = new SqlConnection(_connectionString))
            {
                string query = @"INSERT INTO Employees (FirstName, LastName, Email, Department, Salary, HireDate)
                               VALUES (@FirstName, @LastName, @Email, @Department, @Salary, @HireDate);
                               SELECT CAST(SCOPE_IDENTITY() as int);";

                using (SqlCommand command = new SqlCommand(query, connection))
                {
                    // Use parameters to prevent SQL injection
                    command.Parameters.AddWithValue("@FirstName", firstName);
                    command.Parameters.AddWithValue("@LastName", lastName);
                    command.Parameters.AddWithValue("@Email", email);
                    command.Parameters.AddWithValue("@Department", department);
                    command.Parameters.AddWithValue("@Salary", salary);
                    command.Parameters.AddWithValue("@HireDate", DateTime.Now);

                    try
                    {
                        connection.Open();
                        int newEmployeeId = (int)command.ExecuteScalar();
                        Console.WriteLine($"Employee inserted successfully with ID: {newEmployeeId}");
                        return newEmployeeId;
                    }
                    catch (SqlException ex)
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
            using (SqlConnection connection = new SqlConnection(_connectionString))
            {
                string query = @"UPDATE Employees 
                               SET Email = @Email, Department = @Department 
                               WHERE EmployeeID = @EmployeeID";

                using (SqlCommand command = new SqlCommand(query, connection))
                {
                    command.Parameters.AddWithValue("@EmployeeID", employeeId);
                    command.Parameters.AddWithValue("@Email", email);
                    command.Parameters.AddWithValue("@Department", department);

                    try
                    {
                        connection.Open();
                        int rowsAffected = command.ExecuteNonQuery();
                        return rowsAffected > 0;
                    }
                    catch (SqlException ex)
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
            using (SqlConnection connection = new SqlConnection(_connectionString))
            {
                string query = "DELETE FROM Employees WHERE EmployeeID = @EmployeeID";

                using (SqlCommand command = new SqlCommand(query, connection))
                {
                    command.Parameters.AddWithValue("@EmployeeID", employeeId);

                    try
                    {
                        connection.Open();
                        int rowsAffected = command.ExecuteNonQuery();
                        return rowsAffected > 0;
                    }
                    catch (SqlException ex)
                    {
                        Console.WriteLine($"Error deleting employee: {ex.Message}");
                        return false;
                    }
                }
            }
        }

        #endregion

        #region Stored Procedures

        /// <summary>
        /// Calls a stored procedure to get employee summary
        /// Demonstrates: ExecuteStoredProcedure with input parameters
        /// </summary>
        public void GetEmployeesByDepartment(string department)
        {
            using (SqlConnection connection = new SqlConnection(_connectionString))
            {
                using (SqlCommand command = new SqlCommand("usp_GetEmployeesByDepartment", connection))
                {
                    command.CommandType = CommandType.StoredProcedure;
                    command.Parameters.AddWithValue("@Department", department);

                    try
                    {
                        connection.Open();
                        using (SqlDataReader reader = command.ExecuteReader())
                        {
                            Console.WriteLine($"\nEmployees in {department} Department:");
                            while (reader.Read())
                            {
                                Console.WriteLine($"{reader["FirstName"]} {reader["LastName"]} - {reader["Email"]}");
                            }
                        }
                    }
                    catch (SqlException ex)
                    {
                        Console.WriteLine($"Error executing stored procedure: {ex.Message}");
                    }
                }
            }
        }

        /// <summary>
        /// Calls stored procedure with output parameters
        /// Demonstrates: Output parameters in stored procedures
        /// </summary>
        public decimal GetAverageSalaryByDepartment(string department)
        {
            using (SqlConnection connection = new SqlConnection(_connectionString))
            {
                using (SqlCommand command = new SqlCommand("usp_GetAverageSalary", connection))
                {
                    command.CommandType = CommandType.StoredProcedure;
                    
                    command.Parameters.AddWithValue("@Department", department);
                    
                    SqlParameter outputParam = new SqlParameter("@AvgSalary", SqlDbType.Decimal)
                    {
                        Direction = ParameterDirection.Output,
                        Precision = 18,
                        Scale = 2
                    };
                    command.Parameters.Add(outputParam);

                    try
                    {
                        connection.Open();
                        command.ExecuteNonQuery();
                        
                        decimal avgSalary = (decimal)outputParam.Value;
                        Console.WriteLine($"Average salary in {department}: ${avgSalary:N2}");
                        return avgSalary;
                    }
                    catch (SqlException ex)
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
            using (SqlConnection connection = new SqlConnection(_connectionString))
            {
                connection.Open();
                SqlTransaction transaction = connection.BeginTransaction();

                try
                {
                    // Update employee department
                    string updateQuery = "UPDATE Employees SET Department = @NewDepartment WHERE EmployeeID = @EmployeeID";
                    using (SqlCommand updateCmd = new SqlCommand(updateQuery, connection, transaction))
                    {
                        updateCmd.Parameters.AddWithValue("@NewDepartment", newDepartment);
                        updateCmd.Parameters.AddWithValue("@EmployeeID", employeeId);
                        updateCmd.ExecuteNonQuery();
                    }

                    // Log the transfer
                    string logQuery = "INSERT INTO DepartmentTransferLog (EmployeeID, NewDepartment, TransferDate) VALUES (@EmployeeID, @NewDepartment, @TransferDate)";
                    using (SqlCommand logCmd = new SqlCommand(logQuery, connection, transaction))
                    {
                        logCmd.Parameters.AddWithValue("@EmployeeID", employeeId);
                        logCmd.Parameters.AddWithValue("@NewDepartment", newDepartment);
                        logCmd.Parameters.AddWithValue("@TransferDate", DateTime.Now);
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

        #region DataAdapter and DataSet

        /// <summary>
        /// Demonstrates using DataAdapter and DataSet for disconnected data access
        /// Shows: Fill, Update, working with DataTables
        /// </summary>
        public DataTable GetEmployeesAsDataTable()
        {
            using (SqlConnection connection = new SqlConnection(_connectionString))
            {
                string query = "SELECT EmployeeID, FirstName, LastName, Email, Department, Salary FROM Employees";
                
                SqlDataAdapter adapter = new SqlDataAdapter(query, connection);
                DataTable employeeTable = new DataTable("Employees");

                try
                {
                    adapter.Fill(employeeTable);
                    Console.WriteLine($"Retrieved {employeeTable.Rows.Count} employees into DataTable");
                    return employeeTable;
                }
                catch (SqlException ex)
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
            // Connection string - replace with your actual database details
            string connectionString = "Server=localhost;Database=EmployeeDB;Integrated Security=true;";
            
            EmployeeRepository repository = new EmployeeRepository(connectionString);

            Console.WriteLine("=== ADO.NET Employee Management System ===\n");

            // Example 1: Get all employees
            Console.WriteLine("1. Getting all employees:");
            repository.GetAllEmployees();

            // Example 2: Insert new employee
            Console.WriteLine("\n2. Inserting new employee:");
            repository.InsertEmployee("John", "Doe", "john.doe@company.com", "IT", 75000);

            // Example 3: Update employee
            Console.WriteLine("\n3. Updating employee:");
            repository.UpdateEmployee(1, "newemail@company.com", "HR");

            // Example 4: Call stored procedure
            Console.WriteLine("\n4. Getting employees by department:");
            repository.GetEmployeesByDepartment("IT");

            // Example 5: Get average salary
            Console.WriteLine("\n5. Getting average salary:");
            repository.GetAverageSalaryByDepartment("IT");

            // Example 6: Transaction example
            Console.WriteLine("\n6. Department transfer (transaction):");
            repository.TransferDepartment(1, "Finance");

            // Example 7: DataTable example
            Console.WriteLine("\n7. Using DataTable:");
            DataTable dt = repository.GetEmployeesAsDataTable();

            Console.WriteLine("\nPress any key to exit...");
            Console.ReadKey();
        }
    }
}
