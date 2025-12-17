-- =============================================
-- Stored Procedures for Employee Database
-- Demonstrates: Complex queries, parameters, error handling, optimization
-- =============================================

USE EmployeeDB;
GO

-- =============================================
-- 1. Basic Stored Procedure with Input Parameter
-- =============================================

IF OBJECT_ID('dbo.usp_GetEmployeesByDepartment', 'P') IS NOT NULL
    DROP PROCEDURE dbo.usp_GetEmployeesByDepartment;
GO

CREATE PROCEDURE dbo.usp_GetEmployeesByDepartment
    @Department NVARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Input validation
    IF @Department IS NULL OR LTRIM(RTRIM(@Department)) = ''
    BEGIN
        RAISERROR('Department parameter cannot be null or empty', 16, 1);
        RETURN;
    END
    
    SELECT 
        EmployeeID,
        FirstName,
        LastName,
        Email,
        Department,
        Salary,
        HireDate,
        DATEDIFF(YEAR, HireDate, GETDATE()) AS YearsEmployed
    FROM dbo.Employees
    WHERE Department = @Department
        AND IsActive = 1
    ORDER BY LastName, FirstName;
END
GO

-- =============================================
-- 2. Stored Procedure with Output Parameter
-- =============================================

IF OBJECT_ID('dbo.usp_GetAverageSalary', 'P') IS NOT NULL
    DROP PROCEDURE dbo.usp_GetAverageSalary;
GO

CREATE PROCEDURE dbo.usp_GetAverageSalary
    @Department NVARCHAR(50),
    @AvgSalary DECIMAL(18, 2) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT @AvgSalary = AVG(Salary)
    FROM dbo.Employees
    WHERE Department = @Department
        AND IsActive = 1;
    
    -- Return employee count as result set
    SELECT 
        @Department AS Department,
        COUNT(*) AS EmployeeCount,
        @AvgSalary AS AverageSalary,
        MIN(Salary) AS MinSalary,
        MAX(Salary) AS MaxSalary
    FROM dbo.Employees
    WHERE Department = @Department
        AND IsActive = 1;
END
GO

-- =============================================
-- 3. Complex Stored Procedure with Multiple Result Sets
-- =============================================

IF OBJECT_ID('dbo.usp_GetEmployeeDetailedReport', 'P') IS NOT NULL
    DROP PROCEDURE dbo.usp_GetEmployeeDetailedReport;
GO

CREATE PROCEDURE dbo.usp_GetEmployeeDetailedReport
    @EmployeeID INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Result Set 1: Employee Information
    SELECT 
        e.EmployeeID,
        e.FirstName + ' ' + e.LastName AS FullName,
        e.Email,
        e.Department,
        e.Salary,
        e.HireDate,
        DATEDIFF(YEAR, e.HireDate, GETDATE()) AS YearsEmployed
    FROM dbo.Employees e
    WHERE e.EmployeeID = @EmployeeID;
    
    -- Result Set 2: Project Assignments
    SELECT 
        p.ProjectID,
        p.ProjectName,
        ep.Role,
        ep.HoursAllocated,
        p.Status,
        p.StartDate,
        p.EndDate
    FROM dbo.EmployeeProjects ep
    INNER JOIN dbo.Projects p ON ep.ProjectID = p.ProjectID
    WHERE ep.EmployeeID = @EmployeeID;
    
    -- Result Set 3: Department Transfer History
    SELECT 
        LogID,
        OldDepartment,
        NewDepartment,
        TransferDate,
        TransferredBy
    FROM dbo.DepartmentTransferLog
    WHERE EmployeeID = @EmployeeID
    ORDER BY TransferDate DESC;
END
GO

-- =============================================
-- 4. Stored Procedure with Transaction Handling
-- =============================================

IF OBJECT_ID('dbo.usp_TransferEmployee', 'P') IS NOT NULL
    DROP PROCEDURE dbo.usp_TransferEmployee;
GO

CREATE PROCEDURE dbo.usp_TransferEmployee
    @EmployeeID INT,
    @NewDepartment NVARCHAR(50),
    @TransferredBy NVARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @OldDepartment NVARCHAR(50);
    DECLARE @ErrorMessage NVARCHAR(4000);
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Get current department
        SELECT @OldDepartment = Department
        FROM dbo.Employees
        WHERE EmployeeID = @EmployeeID;
        
        IF @OldDepartment IS NULL
        BEGIN
            RAISERROR('Employee not found', 16, 1);
            RETURN;
        END
        
        IF @OldDepartment = @NewDepartment
        BEGIN
            RAISERROR('Employee is already in the specified department', 16, 1);
            RETURN;
        END
        
        -- Update employee department
        UPDATE dbo.Employees
        SET Department = @NewDepartment,
            ModifiedDate = GETUTCDATE()
        WHERE EmployeeID = @EmployeeID;
        
        -- Log the transfer
        INSERT INTO dbo.DepartmentTransferLog (EmployeeID, OldDepartment, NewDepartment, TransferredBy)
        VALUES (@EmployeeID, @OldDepartment, @NewDepartment, ISNULL(@TransferredBy, SYSTEM_USER));
        
        COMMIT TRANSACTION;
        
        -- Return success message
        SELECT 
            'Success' AS Status,
            'Employee transferred from ' + @OldDepartment + ' to ' + @NewDepartment AS Message;
            
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        
        SET @ErrorMessage = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO

-- =============================================
-- 5. Stored Procedure for Bulk Operations
-- =============================================

IF OBJECT_ID('dbo.usp_BulkSalaryIncrease', 'P') IS NOT NULL
    DROP PROCEDURE dbo.usp_BulkSalaryIncrease;
GO

CREATE PROCEDURE dbo.usp_BulkSalaryIncrease
    @Department NVARCHAR(50) = NULL,
    @PercentageIncrease DECIMAL(5, 2),
    @MinPerformanceScore DECIMAL(3, 2) = 0.0
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @RowsAffected INT;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Validate percentage
        IF @PercentageIncrease <= 0 OR @PercentageIncrease > 50
        BEGIN
            RAISERROR('Percentage increase must be between 0 and 50', 16, 1);
            RETURN;
        END
        
        -- Update salaries
        UPDATE dbo.Employees
        SET Salary = Salary * (1 + @PercentageIncrease / 100),
            ModifiedDate = GETUTCDATE()
        WHERE IsActive = 1
            AND (@Department IS NULL OR Department = @Department);
        
        SET @RowsAffected = @@ROWCOUNT;
        
        COMMIT TRANSACTION;
        
        -- Return summary
        SELECT 
            @RowsAffected AS EmployeesUpdated,
            @PercentageIncrease AS PercentageIncrease,
            @Department AS Department;
            
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;
        
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        RAISERROR(@ErrorMessage, 16, 1);
    END CATCH
END
GO

-- =============================================
-- 6. Stored Procedure with Dynamic SQL (Advanced)
-- =============================================

IF OBJECT_ID('dbo.usp_DynamicEmployeeSearch', 'P') IS NOT NULL
    DROP PROCEDURE dbo.usp_DynamicEmployeeSearch;
GO

CREATE PROCEDURE dbo.usp_DynamicEmployeeSearch
    @Department NVARCHAR(50) = NULL,
    @MinSalary DECIMAL(18, 2) = NULL,
    @MaxSalary DECIMAL(18, 2) = NULL,
    @SortColumn NVARCHAR(50) = 'LastName',
    @SortDirection NVARCHAR(4) = 'ASC'
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @SQL NVARCHAR(MAX);
    DECLARE @Where NVARCHAR(MAX) = ' WHERE IsActive = 1 ';
    DECLARE @OrderBy NVARCHAR(100);
    
    -- Build WHERE clause dynamically
    IF @Department IS NOT NULL
        SET @Where = @Where + ' AND Department = @Department ';
    
    IF @MinSalary IS NOT NULL
        SET @Where = @Where + ' AND Salary >= @MinSalary ';
    
    IF @MaxSalary IS NOT NULL
        SET @Where = @Where + ' AND Salary <= @MaxSalary ';
    
    -- Validate and build ORDER BY clause
    IF @SortColumn NOT IN ('FirstName', 'LastName', 'Salary', 'HireDate', 'Department')
        SET @SortColumn = 'LastName';
    
    IF @SortDirection NOT IN ('ASC', 'DESC')
        SET @SortDirection = 'ASC';
    
    SET @OrderBy = ' ORDER BY ' + QUOTENAME(@SortColumn) + ' ' + @SortDirection;
    
    -- Build complete SQL
    SET @SQL = '
        SELECT 
            EmployeeID,
            FirstName,
            LastName,
            Email,
            Department,
            Salary,
            HireDate
        FROM dbo.Employees '
        + @Where + @OrderBy;
    
    -- Execute dynamic SQL with parameters
    EXEC sp_executesql 
        @SQL,
        N'@Department NVARCHAR(50), @MinSalary DECIMAL(18, 2), @MaxSalary DECIMAL(18, 2)',
        @Department = @Department,
        @MinSalary = @MinSalary,
        @MaxSalary = @MaxSalary;
END
GO

-- =============================================
-- 7. Reporting Stored Procedure with Aggregations
-- =============================================

IF OBJECT_ID('dbo.usp_GetDepartmentSummary', 'P') IS NOT NULL
    DROP PROCEDURE dbo.usp_GetDepartmentSummary;
GO

CREATE PROCEDURE dbo.usp_GetDepartmentSummary
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        e.Department,
        COUNT(DISTINCT e.EmployeeID) AS TotalEmployees,
        AVG(e.Salary) AS AverageSalary,
        MIN(e.Salary) AS MinSalary,
        MAX(e.Salary) AS MaxSalary,
        SUM(e.Salary) AS TotalPayroll,
        COUNT(DISTINCT ep.ProjectID) AS ActiveProjects,
        CASE 
            WHEN AVG(e.Salary) > 90000 THEN 'High'
            WHEN AVG(e.Salary) > 70000 THEN 'Medium'
            ELSE 'Low'
        END AS SalaryBracket
    FROM dbo.Employees e
    LEFT JOIN dbo.EmployeeProjects ep ON e.EmployeeID = ep.EmployeeID
    LEFT JOIN dbo.Projects p ON ep.ProjectID = p.ProjectID AND p.Status = 'Active'
    WHERE e.IsActive = 1
    GROUP BY e.Department
    ORDER BY TotalPayroll DESC;
END
GO

PRINT 'All stored procedures created successfully!';
PRINT '';
PRINT 'Available Stored Procedures:';
PRINT '1. usp_GetEmployeesByDepartment - Get employees by department';
PRINT '2. usp_GetAverageSalary - Calculate average salary with output parameter';
PRINT '3. usp_GetEmployeeDetailedReport - Comprehensive employee report';
PRINT '4. usp_TransferEmployee - Transfer employee with transaction';
PRINT '5. usp_BulkSalaryIncrease - Bulk salary update';
PRINT '6. usp_DynamicEmployeeSearch - Dynamic search with sorting';
PRINT '7. usp_GetDepartmentSummary - Department analytics';
