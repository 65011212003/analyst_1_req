-- =============================================
-- Sample Data Insertion Script
-- =============================================

USE EmployeeDB;
GO

-- Insert Departments
SET IDENTITY_INSERT dbo.Departments ON;
GO

INSERT INTO dbo.Departments (DepartmentID, DepartmentName, Budget)
VALUES 
    (1, 'IT', 500000),
    (2, 'HR', 200000),
    (3, 'Finance', 350000),
    (4, 'Marketing', 300000),
    (5, 'Operations', 400000);
GO

SET IDENTITY_INSERT dbo.Departments OFF;
GO

-- Insert Employees
SET IDENTITY_INSERT dbo.Employees ON;
GO

INSERT INTO dbo.Employees (EmployeeID, FirstName, LastName, Email, Department, Salary, HireDate)
VALUES 
    (1, 'Sarah', 'Johnson', 'sarah.johnson@company.com', 'IT', 95000, '2020-01-15'),
    (2, 'Michael', 'Chen', 'michael.chen@company.com', 'IT', 87000, '2020-03-22'),
    (3, 'Emily', 'Rodriguez', 'emily.rodriguez@company.com', 'HR', 72000, '2019-07-10'),
    (4, 'David', 'Kim', 'david.kim@company.com', 'Finance', 98000, '2018-11-05'),
    (5, 'Jessica', 'Thompson', 'jessica.thompson@company.com', 'Marketing', 76000, '2021-02-18'),
    (6, 'Robert', 'Martinez', 'robert.martinez@company.com', 'IT', 105000, '2017-05-30'),
    (7, 'Amanda', 'Taylor', 'amanda.taylor@company.com', 'Operations', 82000, '2020-08-12'),
    (8, 'James', 'Anderson', 'james.anderson@company.com', 'Finance', 91000, '2019-04-25'),
    (9, 'Lisa', 'Wilson', 'lisa.wilson@company.com', 'HR', 68000, '2021-06-01'),
    (10, 'Christopher', 'Brown', 'christopher.brown@company.com', 'IT', 79000, '2022-01-10');
GO

SET IDENTITY_INSERT dbo.Employees OFF;
GO

-- Insert Projects
SET IDENTITY_INSERT dbo.Projects ON;
GO

INSERT INTO dbo.Projects (ProjectID, ProjectName, DepartmentID, StartDate, EndDate, Budget, Status)
VALUES 
    (1, 'Cloud Migration', 1, '2024-01-01', '2024-12-31', 250000, 'Active'),
    (2, 'ERP Implementation', 3, '2024-03-01', NULL, 500000, 'Active'),
    (3, 'Employee Wellness Program', 2, '2024-02-15', '2024-11-30', 75000, 'Active'),
    (4, 'Digital Marketing Campaign', 4, '2024-04-01', '2024-09-30', 150000, 'Active'),
    (5, 'Process Automation', 5, '2023-06-01', '2024-06-01', 200000, 'Active');
GO

SET IDENTITY_INSERT dbo.Projects OFF;
GO

-- Insert Employee-Project Assignments
INSERT INTO dbo.EmployeeProjects (EmployeeID, ProjectID, Role, AssignedDate, HoursAllocated)
VALUES 
    (1, 1, 'Project Lead', '2024-01-01', 800),
    (2, 1, 'Developer', '2024-01-01', 600),
    (6, 1, 'Senior Developer', '2024-01-01', 700),
    (4, 2, 'Project Manager', '2024-03-01', 500),
    (8, 2, 'Financial Analyst', '2024-03-01', 400),
    (3, 3, 'HR Lead', '2024-02-15', 300),
    (9, 3, 'HR Coordinator', '2024-02-15', 250),
    (5, 4, 'Marketing Manager', '2024-04-01', 450),
    (7, 5, 'Operations Lead', '2024-01-01', 600);
GO

PRINT 'Sample data inserted successfully!';
PRINT 'Employees: 10';
PRINT 'Departments: 5';
PRINT 'Projects: 5';
PRINT 'Employee-Project Assignments: 9';
