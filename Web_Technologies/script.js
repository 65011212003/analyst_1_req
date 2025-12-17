/**
 * Employee Management Dashboard - JavaScript
 * Demonstrates: DOM manipulation, event handling, API calls, data visualization
 */

// ===== Application State =====
const appState = {
    employees: [],
    currentPage: 1,
    itemsPerPage: 10,
    currentFilter: {
        department: '',
        searchTerm: '',
        sortBy: 'name'
    },
    editingEmployeeId: null
};

// ===== Sample Data (In production, this would come from API) =====
const sampleEmployees = [
    { id: 1, firstName: 'Sarah', lastName: 'Johnson', email: 'sarah.j@company.com', department: 'IT', salary: 95000, hireDate: '2020-01-15' },
    { id: 2, firstName: 'Michael', lastName: 'Chen', email: 'michael.c@company.com', department: 'IT', salary: 87000, hireDate: '2020-03-22' },
    { id: 3, firstName: 'Emily', lastName: 'Rodriguez', email: 'emily.r@company.com', department: 'HR', salary: 72000, hireDate: '2019-07-10' },
    { id: 4, firstName: 'David', lastName: 'Kim', email: 'david.k@company.com', department: 'Finance', salary: 98000, hireDate: '2018-11-05' },
    { id: 5, firstName: 'Jessica', lastName: 'Thompson', email: 'jessica.t@company.com', department: 'Marketing', salary: 76000, hireDate: '2021-02-18' },
    { id: 6, firstName: 'Robert', lastName: 'Martinez', email: 'robert.m@company.com', department: 'IT', salary: 105000, hireDate: '2017-05-30' },
    { id: 7, firstName: 'Amanda', lastName: 'Taylor', email: 'amanda.t@company.com', department: 'Operations', salary: 82000, hireDate: '2020-08-12' },
    { id: 8, firstName: 'James', lastName: 'Anderson', email: 'james.a@company.com', department: 'Finance', salary: 91000, hireDate: '2019-04-25' },
    { id: 9, firstName: 'Lisa', lastName: 'Wilson', email: 'lisa.w@company.com', department: 'HR', salary: 68000, hireDate: '2021-06-01' },
    { id: 10, firstName: 'Christopher', lastName: 'Brown', email: 'chris.b@company.com', department: 'IT', salary: 79000, hireDate: '2022-01-10' }
];

// ===== DOM Ready =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('Employee Management System initialized');
    
    // Initialize app
    initializeApp();
    
    // Set up event listeners
    setupEventListeners();
    
    // Load initial data
    loadEmployees();
    
    // Update dashboard
    updateDashboard();
});

// ===== Initialization =====
function initializeApp() {
    // Load sample data
    appState.employees = [...sampleEmployees];
    
    // Set up navigation
    setupNavigation();
}

function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remove active class from all links and sections
            navLinks.forEach(l => l.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            
            // Add active class to clicked link
            link.classList.add('active');
            
            // Show corresponding section
            const targetSection = link.getAttribute('href').substring(1);
            const section = document.getElementById(targetSection);
            if (section) {
                section.classList.add('active');
            }
        });
    });
}

// ===== Event Listeners =====
function setupEventListeners() {
    // Add Employee button
    const btnAddEmployee = document.getElementById('btnAddEmployee');
    if (btnAddEmployee) {
        btnAddEmployee.addEventListener('click', () => openEmployeeModal());
    }
    
    // Search
    const btnSearch = document.getElementById('btnSearch');
    const searchInput = document.getElementById('searchInput');
    if (btnSearch) {
        btnSearch.addEventListener('click', performSearch);
    }
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') performSearch();
        });
    }
    
    // Filters
    const filterDepartment = document.getElementById('filterDepartment');
    const sortBy = document.getElementById('sortBy');
    
    if (filterDepartment) {
        filterDepartment.addEventListener('change', (e) => {
            appState.currentFilter.department = e.target.value;
            filterAndDisplayEmployees();
        });
    }
    
    if (sortBy) {
        sortBy.addEventListener('change', (e) => {
            appState.currentFilter.sortBy = e.target.value;
            filterAndDisplayEmployees();
        });
    }
    
    // Pagination
    const btnPrevPage = document.getElementById('btnPrevPage');
    const btnNextPage = document.getElementById('btnNextPage');
    
    if (btnPrevPage) {
        btnPrevPage.addEventListener('click', () => changePage(-1));
    }
    if (btnNextPage) {
        btnNextPage.addEventListener('click', () => changePage(1));
    }
    
    // Modal
    const modal = document.getElementById('employeeModal');
    const closeModal = modal?.querySelector('.close');
    const btnCancel = document.getElementById('btnCancel');
    const employeeForm = document.getElementById('employeeForm');
    
    if (closeModal) {
        closeModal.addEventListener('click', () => closeEmployeeModal());
    }
    if (btnCancel) {
        btnCancel.addEventListener('click', () => closeEmployeeModal());
    }
    if (employeeForm) {
        employeeForm.addEventListener('submit', handleEmployeeFormSubmit);
    }
    
    // Close modal when clicking outside
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeEmployeeModal();
            }
        });
    }
}

// ===== Dashboard Functions =====
function updateDashboard() {
    const employees = appState.employees;
    
    // Update statistics
    document.getElementById('totalEmployees').textContent = employees.length;
    document.getElementById('totalProjects').textContent = Math.floor(Math.random() * 15) + 5;
    
    const avgSalary = employees.reduce((sum, emp) => sum + emp.salary, 0) / employees.length;
    document.getElementById('avgSalary').textContent = `$${Math.round(avgSalary).toLocaleString()}`;
    
    const departments = [...new Set(employees.map(emp => emp.department))];
    document.getElementById('totalDepts').textContent = departments.length;
    
    // Update recent activity
    updateRecentActivity();
}

function updateRecentActivity() {
    const activityList = document.getElementById('activityList');
    if (!activityList) return;
    
    const activities = [
        { icon: '➕', text: 'New employee Sarah Johnson added to IT', time: '2 hours ago' },
        { icon: '✏️', text: 'Salary updated for Michael Chen', time: '5 hours ago' },
        { icon: '🔄', text: 'Department transfer: Emily Rodriguez to HR', time: '1 day ago' },
        { icon: '📊', text: 'Q4 performance report generated', time: '2 days ago' }
    ];
    
    activityList.innerHTML = activities.map(activity => `
        <div class="activity-item">
            <div class="activity-icon">${activity.icon}</div>
            <div class="activity-text">
                <p>${activity.text}</p>
                <small style="color: var(--secondary-color)">${activity.time}</small>
            </div>
        </div>
    `).join('');
}

// ===== Employee Management Functions =====
function loadEmployees() {
    // In production, this would be an API call
    // fetch('/api/employees')
    //     .then(response => response.json())
    //     .then(data => { appState.employees = data; });
    
    filterAndDisplayEmployees();
}

function filterAndDisplayEmployees() {
    let filtered = [...appState.employees];
    
    // Apply department filter
    if (appState.currentFilter.department) {
        filtered = filtered.filter(emp => 
            emp.department === appState.currentFilter.department
        );
    }
    
    // Apply search filter
    if (appState.currentFilter.searchTerm) {
        const searchLower = appState.currentFilter.searchTerm.toLowerCase();
        filtered = filtered.filter(emp =>
            emp.firstName.toLowerCase().includes(searchLower) ||
            emp.lastName.toLowerCase().includes(searchLower) ||
            emp.email.toLowerCase().includes(searchLower)
        );
    }
    
    // Apply sorting
    filtered.sort((a, b) => {
        switch (appState.currentFilter.sortBy) {
            case 'name':
                return a.lastName.localeCompare(b.lastName);
            case 'salary':
                return b.salary - a.salary;
            case 'hireDate':
                return new Date(b.hireDate) - new Date(a.hireDate);
            default:
                return 0;
        }
    });
    
    displayEmployees(filtered);
}

function displayEmployees(employees) {
    const tbody = document.getElementById('employeeTableBody');
    if (!tbody) return;
    
    // Calculate pagination
    const start = (appState.currentPage - 1) * appState.itemsPerPage;
    const end = start + appState.itemsPerPage;
    const paginatedEmployees = employees.slice(start, end);
    
    // Render table rows
    tbody.innerHTML = paginatedEmployees.map(emp => `
        <tr>
            <td>${emp.id}</td>
            <td>${emp.firstName} ${emp.lastName}</td>
            <td>${emp.email}</td>
            <td><span class="badge badge-${emp.department.toLowerCase()}">${emp.department}</span></td>
            <td>$${emp.salary.toLocaleString()}</td>
            <td>${formatDate(emp.hireDate)}</td>
            <td>
                <button class="btn-action btn-edit" onclick="editEmployee(${emp.id})">✏️</button>
                <button class="btn-action btn-delete" onclick="deleteEmployee(${emp.id})">🗑️</button>
            </td>
        </tr>
    `).join('');
    
    // Update pagination info
    updatePaginationInfo(employees.length);
}

function updatePaginationInfo(totalItems) {
    const totalPages = Math.ceil(totalItems / appState.itemsPerPage);
    const pageInfo = document.getElementById('pageInfo');
    const btnPrevPage = document.getElementById('btnPrevPage');
    const btnNextPage = document.getElementById('btnNextPage');
    
    if (pageInfo) {
        pageInfo.textContent = `Page ${appState.currentPage} of ${totalPages || 1}`;
    }
    
    if (btnPrevPage) {
        btnPrevPage.disabled = appState.currentPage === 1;
    }
    if (btnNextPage) {
        btnNextPage.disabled = appState.currentPage >= totalPages;
    }
}

function changePage(direction) {
    appState.currentPage += direction;
    if (appState.currentPage < 1) appState.currentPage = 1;
    filterAndDisplayEmployees();
}

function performSearch() {
    const searchInput = document.getElementById('searchInput');
    appState.currentFilter.searchTerm = searchInput.value;
    appState.currentPage = 1;
    filterAndDisplayEmployees();
}

// ===== CRUD Operations =====
function editEmployee(id) {
    const employee = appState.employees.find(emp => emp.id === id);
    if (!employee) return;
    
    appState.editingEmployeeId = id;
    
    // Populate form
    document.getElementById('firstName').value = employee.firstName;
    document.getElementById('lastName').value = employee.lastName;
    document.getElementById('email').value = employee.email;
    document.getElementById('department').value = employee.department;
    document.getElementById('salary').value = employee.salary;
    document.getElementById('hireDate').value = employee.hireDate;
    
    // Change modal title
    document.getElementById('modalTitle').textContent = 'Edit Employee';
    
    openEmployeeModal();
}

function deleteEmployee(id) {
    if (!confirm('Are you sure you want to delete this employee?')) return;
    
    appState.employees = appState.employees.filter(emp => emp.id !== id);
    filterAndDisplayEmployees();
    updateDashboard();
    showToast('Employee deleted successfully', 'success');
}

function openEmployeeModal() {
    const modal = document.getElementById('employeeModal');
    if (modal) {
        modal.classList.add('active');
    }
}

function closeEmployeeModal() {
    const modal = document.getElementById('employeeModal');
    const form = document.getElementById('employeeForm');
    
    if (modal) {
        modal.classList.remove('active');
    }
    if (form) {
        form.reset();
    }
    
    appState.editingEmployeeId = null;
    document.getElementById('modalTitle').textContent = 'Add New Employee';
}

function handleEmployeeFormSubmit(e) {
    e.preventDefault();
    
    const formData = {
        firstName: document.getElementById('firstName').value,
        lastName: document.getElementById('lastName').value,
        email: document.getElementById('email').value,
        department: document.getElementById('department').value,
        salary: parseFloat(document.getElementById('salary').value),
        hireDate: document.getElementById('hireDate').value
    };
    
    if (appState.editingEmployeeId) {
        // Update existing employee
        const index = appState.employees.findIndex(emp => emp.id === appState.editingEmployeeId);
        if (index !== -1) {
            appState.employees[index] = { ...appState.employees[index], ...formData };
            showToast('Employee updated successfully', 'success');
        }
    } else {
        // Add new employee
        const newEmployee = {
            id: Math.max(...appState.employees.map(emp => emp.id)) + 1,
            ...formData
        };
        appState.employees.push(newEmployee);
        showToast('Employee added successfully', 'success');
    }
    
    closeEmployeeModal();
    filterAndDisplayEmployees();
    updateDashboard();
}

// ===== Utility Functions =====
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    if (!toast) return;
    
    toast.querySelector('.toast-message').textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ===== API Simulation (for demonstration) =====
class EmployeeAPI {
    static async getAllEmployees() {
        // Simulate API delay
        return new Promise(resolve => {
            setTimeout(() => resolve(sampleEmployees), 500);
        });
    }
    
    static async getEmployeeById(id) {
        return new Promise(resolve => {
            const employee = sampleEmployees.find(emp => emp.id === id);
            setTimeout(() => resolve(employee), 300);
        });
    }
    
    static async createEmployee(employeeData) {
        return new Promise(resolve => {
            const newEmployee = { id: Date.now(), ...employeeData };
            setTimeout(() => resolve(newEmployee), 400);
        });
    }
    
    static async updateEmployee(id, employeeData) {
        return new Promise(resolve => {
            const updated = { id, ...employeeData };
            setTimeout(() => resolve(updated), 400);
        });
    }
    
    static async deleteEmployee(id) {
        return new Promise(resolve => {
            setTimeout(() => resolve({ success: true }), 300);
        });
    }
    
    static async getDepartmentStats() {
        return new Promise(resolve => {
            const stats = this.calculateDepartmentStats();
            setTimeout(() => resolve(stats), 400);
        });
    }
    
    static calculateDepartmentStats() {
        const departments = {};
        sampleEmployees.forEach(emp => {
            if (!departments[emp.department]) {
                departments[emp.department] = { count: 0, totalSalary: 0 };
            }
            departments[emp.department].count++;
            departments[emp.department].totalSalary += emp.salary;
        });
        
        return Object.entries(departments).map(([dept, data]) => ({
            department: dept,
            employeeCount: data.count,
            averageSalary: Math.round(data.totalSalary / data.count)
        }));
    }
}

// ===== Export for testing =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { EmployeeAPI, appState, formatDate };
}

console.log('JavaScript loaded successfully!');
