-- =============================================
-- Database Creation Script
-- Demonstrates: Database design, table creation, constraints, indexes
-- =============================================

-- Create database
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'EmployeeDB')
BEGIN
    CREATE DATABASE EmployeeDB;
END
GO

USE EmployeeDB;
GO

-- =============================================
-- Table Creation with Best Practices
-- =============================================

-- Employees Table
IF OBJECT_ID('dbo.Employees', 'U') IS NOT NULL
    DROP TABLE dbo.Employees;
GO

CREATE TABLE dbo.Employees
(
    EmployeeID INT IDENTITY(1,1) PRIMARY KEY,
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Email NVARCHAR(100) NOT NULL UNIQUE,
    Department NVARCHAR(50) NOT NULL,
    Salary DECIMAL(18, 2) NOT NULL CHECK (Salary > 0),
    HireDate DATE NOT NULL DEFAULT GETDATE(),
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    ModifiedDate DATETIME2 NULL,
    
    CONSTRAINT CK_Employee_Email CHECK (Email LIKE '%@%.%')
);
GO

-- Create indexes for better query performance
CREATE NONCLUSTERED INDEX IX_Employees_Department 
ON dbo.Employees(Department);
GO

CREATE NONCLUSTERED INDEX IX_Employees_HireDate 
ON dbo.Employees(HireDate DESC);
GO

-- =============================================
-- Departments Table
-- =============================================

IF OBJECT_ID('dbo.Departments', 'U') IS NOT NULL
    DROP TABLE dbo.Departments;
GO

CREATE TABLE dbo.Departments
(
    DepartmentID INT IDENTITY(1,1) PRIMARY KEY,
    DepartmentName NVARCHAR(50) NOT NULL UNIQUE,
    ManagerID INT NULL,
    Budget DECIMAL(18, 2) NOT NULL DEFAULT 0,
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE()
);
GO

-- =============================================
-- Projects Table
-- =============================================

IF OBJECT_ID('dbo.Projects', 'U') IS NOT NULL
    DROP TABLE dbo.Projects;
GO

CREATE TABLE dbo.Projects
(
    ProjectID INT IDENTITY(1,1) PRIMARY KEY,
    ProjectName NVARCHAR(100) NOT NULL,
    DepartmentID INT NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NULL,
    Budget DECIMAL(18, 2) NOT NULL,
    Status NVARCHAR(20) NOT NULL DEFAULT 'Active',
    
    CONSTRAINT FK_Projects_Departments 
        FOREIGN KEY (DepartmentID) REFERENCES dbo.Departments(DepartmentID),
    CONSTRAINT CK_Projects_Dates 
        CHECK (EndDate IS NULL OR EndDate >= StartDate),
    CONSTRAINT CK_Projects_Status 
        CHECK (Status IN ('Active', 'Completed', 'On Hold', 'Cancelled'))
);
GO

-- =============================================
-- EmployeeProjects (Many-to-Many relationship)
-- =============================================

IF OBJECT_ID('dbo.EmployeeProjects', 'U') IS NOT NULL
    DROP TABLE dbo.EmployeeProjects;
GO

CREATE TABLE dbo.EmployeeProjects
(
    EmployeeID INT NOT NULL,
    ProjectID INT NOT NULL,
    Role NVARCHAR(50) NOT NULL,
    AssignedDate DATE NOT NULL DEFAULT GETDATE(),
    HoursAllocated INT NOT NULL DEFAULT 0,
    
    PRIMARY KEY (EmployeeID, ProjectID),
    CONSTRAINT FK_EmployeeProjects_Employees 
        FOREIGN KEY (EmployeeID) REFERENCES dbo.Employees(EmployeeID),
    CONSTRAINT FK_EmployeeProjects_Projects 
        FOREIGN KEY (ProjectID) REFERENCES dbo.Projects(ProjectID)
);
GO

-- =============================================
-- Audit Log Table
-- =============================================

IF OBJECT_ID('dbo.DepartmentTransferLog', 'U') IS NOT NULL
    DROP TABLE dbo.DepartmentTransferLog;
GO

CREATE TABLE dbo.DepartmentTransferLog
(
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    EmployeeID INT NOT NULL,
    OldDepartment NVARCHAR(50) NULL,
    NewDepartment NVARCHAR(50) NOT NULL,
    TransferDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    TransferredBy NVARCHAR(100) NOT NULL DEFAULT SYSTEM_USER,
    
    CONSTRAINT FK_DepartmentTransferLog_Employees 
        FOREIGN KEY (EmployeeID) REFERENCES dbo.Employees(EmployeeID)
);
GO

-- =============================================
-- Performance Monitoring View
-- =============================================

IF OBJECT_ID('dbo.vw_EmployeePerformance', 'V') IS NOT NULL
    DROP VIEW dbo.vw_EmployeePerformance;
GO

CREATE VIEW dbo.vw_EmployeePerformance
AS
SELECT 
    e.EmployeeID,
    e.FirstName + ' ' + e.LastName AS FullName,
    e.Department,
    e.Salary,
    COUNT(ep.ProjectID) AS ActiveProjects,
    SUM(ep.HoursAllocated) AS TotalHoursAllocated,
    e.HireDate,
    DATEDIFF(YEAR, e.HireDate, GETDATE()) AS YearsEmployed
FROM dbo.Employees e
LEFT JOIN dbo.EmployeeProjects ep ON e.EmployeeID = ep.EmployeeID
LEFT JOIN dbo.Projects p ON ep.ProjectID = p.ProjectID AND p.Status = 'Active'
WHERE e.IsActive = 1
GROUP BY 
    e.EmployeeID,
    e.FirstName,
    e.LastName,
    e.Department,
    e.Salary,
    e.HireDate;
GO

PRINT 'Database schema created successfully!';
