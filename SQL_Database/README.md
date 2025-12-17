# SQL Database Examples

Comprehensive SQL Server database scripts covering schema design, stored procedures, and query optimization.

## Files

### 1. 01_CreateDatabase.sql
- Database and table creation
- Primary and foreign keys
- Constraints and validation
- Indexes for performance
- Views for reporting

### 2. 02_SampleData.sql
- Sample data insertion
- Realistic test datasets
- Employee, department, and project data

### 3. 03_StoredProcedures.sql
- Basic to advanced stored procedures
- Input/output parameters
- Transaction handling
- Error handling
- Dynamic SQL
- Bulk operations

### 4. 04_QueryOptimization.sql
- Index strategies
- Query performance tuning
- CTEs and window functions
- Execution plan analysis
- Best practices

## Setup Instructions

Run the scripts in order:

```sql
-- 1. Create database and schema
:r 01_CreateDatabase.sql

-- 2. Load sample data
:r 02_SampleData.sql

-- 3. Create stored procedures
:r 03_StoredProcedures.sql

-- 4. Apply optimization strategies
:r 04_QueryOptimization.sql
```

## Key Concepts Covered

### Database Design
- ✅ Normalization (3NF)
- ✅ Referential integrity
- ✅ Constraints and validation
- ✅ Indexes for performance
- ✅ Audit logging

### Stored Procedures
- ✅ Input/output parameters
- ✅ Multiple result sets
- ✅ Transaction management
- ✅ Error handling (TRY-CATCH)
- ✅ Dynamic SQL
- ✅ Business logic encapsulation

### Query Optimization
- ✅ Index strategies (clustered, non-clustered, filtered, covering)
- ✅ Avoiding common pitfalls
- ✅ CTEs for readability
- ✅ Window functions for analytics
- ✅ Efficient paging
- ✅ Execution plan analysis

### Advanced Features
- ✅ Window functions (ROW_NUMBER, RANK, SUM OVER)
- ✅ Common Table Expressions (CTEs)
- ✅ Indexed views
- ✅ Partitioning concepts
- ✅ Statistics management

## Testing Stored Procedures

```sql
-- Test basic procedure
EXEC usp_GetEmployeesByDepartment @Department = 'IT';

-- Test with output parameter
DECLARE @AvgSal DECIMAL(18,2);
EXEC usp_GetAverageSalary @Department = 'IT', @AvgSalary = @AvgSal OUTPUT;
PRINT 'Average Salary: ' + CAST(@AvgSal AS VARCHAR(20));

-- Test transaction procedure
EXEC usp_TransferEmployee @EmployeeID = 1, @NewDepartment = 'Finance';

-- Test dynamic search
EXEC usp_DynamicEmployeeSearch 
    @Department = 'IT', 
    @MinSalary = 70000, 
    @SortColumn = 'Salary', 
    @SortDirection = 'DESC';
```

## Performance Monitoring

```sql
-- Check existing indexes
SELECT 
    OBJECT_NAME(i.object_id) AS TableName,
    i.name AS IndexName,
    i.type_desc,
    i.is_unique
FROM sys.indexes i
WHERE OBJECT_NAME(i.object_id) LIKE 'Employees%';

-- View execution statistics
SET STATISTICS TIME ON;
SET STATISTICS IO ON;

-- Your query here
SELECT * FROM Employees WHERE Department = 'IT';

-- View actual execution plan (Ctrl+M in SSMS)
```

## Best Practices Demonstrated

1. ✅ Use parameterized queries to prevent SQL injection
2. ✅ Implement proper error handling
3. ✅ Use transactions for data integrity
4. ✅ Create appropriate indexes
5. ✅ Avoid SELECT * in production code
6. ✅ Use meaningful names for objects
7. ✅ Include comments and documentation
8. ✅ Regular statistics updates
9. ✅ Monitor and optimize slow queries
10. ✅ Use stored procedures for complex logic

## Common Patterns

### Transaction Pattern
```sql
BEGIN TRY
    BEGIN TRANSACTION;
    -- Your operations
    COMMIT TRANSACTION;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;
    -- Error handling
END CATCH
```

### Output Parameter Pattern
```sql
CREATE PROCEDURE usp_Example
    @InputParam INT,
    @OutputParam INT OUTPUT
AS
BEGIN
    SELECT @OutputParam = COUNT(*) FROM Table WHERE ID = @InputParam;
END
```

### CTE Pattern
```sql
WITH TempResults AS (
    SELECT ... FROM ...
)
SELECT * FROM TempResults WHERE ...;
```

## Learning Resources

- Microsoft SQL Server Documentation
- Execution Plan Analysis
- Index Tuning Advisor
- Query Store (SQL Server 2016+)
