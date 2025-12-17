---
applyTo: '**'
---

# Project Coding Guidelines

## Modularity Rules

### 1. Single Responsibility Principle
- Each module should have one clear purpose
- Functions should do one thing and do it well
- Classes should have a single, well-defined responsibility

### 2. File Organization
- Keep related functionality together in the same module
- Separate concerns into different files (e.g., data access, business logic, presentation)
- Use meaningful file names that reflect their content
- Typical structure: `models/`, `services/`, `utils/`, `controllers/`

### 3. Function Design
- Functions should be small and focused (ideally < 50 lines)
- Limit function parameters (max 3-4 parameters; use objects/dataclasses for more)
- Use descriptive function names that indicate purpose
- Avoid side effects; prefer pure functions when possible

### 4. Class Design
- Keep classes focused and cohesive
- Favor composition over inheritance
- Use dependency injection for better testability
- Implement interfaces/protocols for loose coupling

### 5. Import Management
- Use absolute imports for clarity
- Group imports: standard library, third-party, local
- Avoid circular dependencies
- Import only what you need

### 6. Code Reusability
- Extract common logic into utility functions
- Create reusable components and modules
- Use constants for magic numbers and strings
- Implement generic solutions when appropriate

### 7. Separation of Concerns
- Separate business logic from data access
- Keep presentation logic separate from business logic
- Isolate external dependencies (APIs, databases)
- Use layers: presentation, business, data access

### 8. Module Coupling
- Minimize dependencies between modules
- Use interfaces/protocols to reduce coupling
- Apply the dependency inversion principle
- Favor loose coupling over tight coupling

### 9. Documentation
- Add docstrings to all public modules, classes, and functions
- Document module purpose and usage
- Include type hints for better clarity
- Provide examples where helpful

### 10. Testing
- Design modules to be testable
- Mock external dependencies
- Each module should have corresponding tests
- Keep test files parallel to source files