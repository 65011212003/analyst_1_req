# C# ADO.NET Examples

This folder demonstrates C# programming with ADO.NET for database access.

## What You'll Learn

- **SqlConnection** - Managing database connections
- **SqlCommand** - Executing SQL queries and commands
- **SqlDataReader** - Reading data efficiently
- **SqlParameter** - Preventing SQL injection
- **Stored Procedures** - Calling and using output parameters
- **Transactions** - Ensuring data integrity
- **DataAdapter & DataSet** - Disconnected data access

## Prerequisites

- Visual Studio 2019 or later
- SQL Server (LocalDB, Express, or full version)
- .NET Framework 4.7.2 or .NET 6+

## Setup

1. Create the database using the SQL scripts in `SQL_Database` folder
2. Update the connection string in the code
3. Build and run the project

## Key Concepts

### Connection Management
```csharp
using (SqlConnection connection = new SqlConnection(connectionString))
{
    connection.Open();
    // Your code here
} // Connection automatically closed
```

### Parameterized Queries (SQL Injection Prevention)
```csharp
command.Parameters.AddWithValue("@Email", email);
```

### Stored Procedures
```csharp
command.CommandType = CommandType.StoredProcedure;
```

### Transactions
```csharp
SqlTransaction transaction = connection.BeginTransaction();
try {
    // Operations
    transaction.Commit();
} catch {
    transaction.Rollback();
}
```

## Best Practices Demonstrated

1. ✅ Always use `using` statements for proper disposal
2. ✅ Use parameterized queries to prevent SQL injection
3. ✅ Handle exceptions appropriately
4. ✅ Use transactions for related operations
5. ✅ Close connections as soon as possible
6. ✅ Use stored procedures for complex operations
