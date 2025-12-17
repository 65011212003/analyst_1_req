-- =============================================
-- Query Optimization Examples and Best Practices
-- Demonstrates: Indexes, execution plans, query tuning
-- =============================================

USE EmployeeDB;
GO

-- =============================================
-- 1. Index Creation for Performance
-- =============================================

PRINT 'Creating Indexes for Query Optimization...';
PRINT '';

-- Composite index for common queries
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Employees_Dept_Salary')
BEGIN
    CREATE NONCLUSTERED INDEX IX_Employees_Dept_Salary
    ON dbo.Employees(Department, Salary)
    INCLUDE (FirstName, LastName, Email);
    PRINT '✓ Created composite index on Department and Salary';
END

-- Filtered index for active employees only
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Employees_Active')
BEGIN
    CREATE NONCLUSTERED INDEX IX_Employees_Active
    ON dbo.Employees(IsActive, Department)
    WHERE IsActive = 1;
    PRINT '✓ Created filtered index for active employees';
END

-- Covering index for common SELECT queries
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_Projects_Status_Dates')
BEGIN
    CREATE NONCLUSTERED INDEX IX_Projects_Status_Dates
    ON dbo.Projects(Status, StartDate, EndDate)
    INCLUDE (ProjectName, Budget, DepartmentID);
    PRINT '✓ Created covering index for project queries';
END

GO

-- =============================================
-- 2. Query Optimization Examples
-- =============================================

PRINT '';
PRINT 'Query Optimization Examples:';
PRINT '';

-- BAD: Using SELECT *
-- GOOD: Selecting only needed columns
PRINT '-- Optimization 1: Select only needed columns';
SELECT 
    EmployeeID,
    FirstName,
    LastName,
    Department,
    Salary
FROM dbo.Employees
WHERE Department = 'IT';
GO

-- BAD: Using functions in WHERE clause
-- GOOD: Avoid functions on indexed columns
PRINT '-- Optimization 2: Avoid functions on indexed columns';
-- Bad example (commented):
-- SELECT * FROM Employees WHERE YEAR(HireDate) = 2020

-- Good example:
SELECT 
    EmployeeID,
    FirstName,
    LastName,
    HireDate
FROM dbo.Employees
WHERE HireDate >= '2020-01-01' AND HireDate < '2021-01-01';
GO

-- BAD: Multiple subqueries
-- GOOD: Using JOIN instead of subqueries
PRINT '-- Optimization 3: Use JOINs instead of subqueries when possible';
SELECT 
    e.EmployeeID,
    e.FirstName + ' ' + e.LastName AS FullName,
    e.Department,
    COUNT(ep.ProjectID) AS ProjectCount
FROM dbo.Employees e
LEFT JOIN dbo.EmployeeProjects ep ON e.EmployeeID = ep.EmployeeID
GROUP BY e.EmployeeID, e.FirstName, e.LastName, e.Department
HAVING COUNT(ep.ProjectID) > 0;
GO

-- =============================================
-- 3. Common Table Expressions (CTEs) for Readability
-- =============================================

PRINT '-- Optimization 4: Using CTEs for complex queries';

WITH EmployeeSalaryStats AS (
    SELECT 
        Department,
        AVG(Salary) AS DeptAvgSalary,
        MAX(Salary) AS DeptMaxSalary
    FROM dbo.Employees
    WHERE IsActive = 1
    GROUP BY Department
),
EmployeeRanking AS (
    SELECT 
        e.EmployeeID,
        e.FirstName,
        e.LastName,
        e.Department,
        e.Salary,
        ROW_NUMBER() OVER (PARTITION BY e.Department ORDER BY e.Salary DESC) AS SalaryRank
    FROM dbo.Employees e
    WHERE e.IsActive = 1
)
SELECT 
    er.Department,
    er.FirstName + ' ' + er.LastName AS TopEarner,
    er.Salary AS TopSalary,
    ess.DeptAvgSalary,
    er.Salary - ess.DeptAvgSalary AS DifferenceFromAvg
FROM EmployeeRanking er
INNER JOIN EmployeeSalaryStats ess ON er.Department = ess.Department
WHERE er.SalaryRank = 1
ORDER BY er.Salary DESC;
GO

-- =============================================
-- 4. Window Functions for Analytics
-- =============================================

PRINT '-- Optimization 5: Using window functions for analytics';

SELECT 
    EmployeeID,
    FirstName + ' ' + LastName AS FullName,
    Department,
    Salary,
    -- Running total of salaries by department
    SUM(Salary) OVER (PARTITION BY Department ORDER BY EmployeeID) AS RunningTotal,
    -- Average salary in department
    AVG(Salary) OVER (PARTITION BY Department) AS DeptAvgSalary,
    -- Rank within department
    RANK() OVER (PARTITION BY Department ORDER BY Salary DESC) AS DeptSalaryRank,
    -- Percentage of department total
    CAST(Salary * 100.0 / SUM(Salary) OVER (PARTITION BY Department) AS DECIMAL(5,2)) AS PctOfDeptTotal
FROM dbo.Employees
WHERE IsActive = 1
ORDER BY Department, Salary DESC;
GO

-- =============================================
-- 5. Optimized Paging Query
-- =============================================

PRINT '-- Optimization 6: Efficient paging with OFFSET-FETCH';

DECLARE @PageNumber INT = 1;
DECLARE @PageSize INT = 10;

SELECT 
    EmployeeID,
    FirstName,
    LastName,
    Department,
    Salary,
    HireDate
FROM dbo.Employees
WHERE IsActive = 1
ORDER BY EmployeeID
OFFSET (@PageNumber - 1) * @PageSize ROWS
FETCH NEXT @PageSize ROWS ONLY;
GO

-- =============================================
-- 6. Indexed View for Frequently Accessed Aggregations
-- =============================================

PRINT '-- Optimization 7: Creating indexed view for performance';

-- Drop view if exists
IF OBJECT_ID('dbo.vw_DepartmentStats', 'V') IS NOT NULL
    DROP VIEW dbo.vw_DepartmentStats;
GO

CREATE VIEW dbo.vw_DepartmentStats
WITH SCHEMABINDING
AS
SELECT 
    Department,
    COUNT_BIG(*) AS EmployeeCount,
    SUM(Salary) AS TotalPayroll,
    AVG(Salary) AS AvgSalary
FROM dbo.Employees
WHERE IsActive = 1
GROUP BY Department;
GO

-- Create unique clustered index on the view
CREATE UNIQUE CLUSTERED INDEX IX_vw_DepartmentStats
ON dbo.vw_DepartmentStats(Department);
GO

-- =============================================
-- 7. Query Performance Analysis
-- =============================================

PRINT '';
PRINT '-- Optimization 8: Enable execution plan and statistics';
PRINT 'Run these commands to analyze query performance:';
PRINT 'SET STATISTICS TIME ON;';
PRINT 'SET STATISTICS IO ON;';
PRINT 'SET SHOWPLAN_TEXT ON; -- or use actual execution plan in SSMS';
PRINT '';

-- =============================================
-- 8. Partitioning Example (for large tables)
-- =============================================

PRINT '-- Optimization 9: Table partitioning for very large tables';
PRINT '-- (Commented example - requires specific setup)';

/*
-- Create partition function
CREATE PARTITION FUNCTION pf_YearlyPartition (DATE)
AS RANGE RIGHT FOR VALUES 
    ('2020-01-01', '2021-01-01', '2022-01-01', '2023-01-01', '2024-01-01');

-- Create partition scheme
CREATE PARTITION SCHEME ps_YearlyPartition
AS PARTITION pf_YearlyPartition
ALL TO ([PRIMARY]);

-- Create partitioned table
CREATE TABLE dbo.EmployeeHistory
(
    HistoryID INT IDENTITY(1,1),
    EmployeeID INT,
    ChangeDate DATE,
    ChangeType NVARCHAR(50),
    OldValue NVARCHAR(MAX),
    NewValue NVARCHAR(MAX)
) ON ps_YearlyPartition(ChangeDate);
*/

-- =============================================
-- 9. Statistics Update
-- =============================================

PRINT '-- Optimization 10: Update statistics for accurate query plans';

-- Update statistics on all tables
UPDATE STATISTICS dbo.Employees WITH FULLSCAN;
UPDATE STATISTICS dbo.Projects WITH FULLSCAN;
UPDATE STATISTICS dbo.EmployeeProjects WITH FULLSCAN;

PRINT '✓ Statistics updated';

-- =============================================
-- 10. Best Practices Summary
-- =============================================

PRINT '';
PRINT '==============================================';
PRINT 'SQL QUERY OPTIMIZATION BEST PRACTICES';
PRINT '==============================================';
PRINT '1. ✓ Create appropriate indexes (but not too many)';
PRINT '2. ✓ Select only required columns (avoid SELECT *)';
PRINT '3. ✓ Avoid functions on indexed columns in WHERE';
PRINT '4. ✓ Use JOINs instead of subqueries when possible';
PRINT '5. ✓ Use CTEs for complex, readable queries';
PRINT '6. ✓ Leverage window functions for analytics';
PRINT '7. ✓ Implement proper paging with OFFSET-FETCH';
PRINT '8. ✓ Consider indexed views for frequent aggregations';
PRINT '9. ✓ Update statistics regularly';
PRINT '10. ✓ Monitor execution plans and optimize accordingly';
PRINT '11. ✓ Use filtered indexes for specific scenarios';
PRINT '12. ✓ Partition very large tables';
PRINT '==============================================';
