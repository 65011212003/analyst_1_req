# Object-Oriented Programming (OOP) Examples

Comprehensive demonstrations of OOP concepts, design patterns, and SOLID principles in Python.

## 📚 Contents

### 1. **oop_fundamentals.py**
Core OOP concepts with practical examples:
- ✅ **Classes & Objects** - Blueprint and instances
- ✅ **Encapsulation** - Data hiding (public, protected, private)
- ✅ **Inheritance** - Code reuse through parent-child relationships
- ✅ **Polymorphism** - Same interface, different implementations
- ✅ **Abstraction** - Abstract base classes
- ✅ **Multiple Inheritance** - Inheriting from multiple classes
- ✅ **Class/Static Methods** - Alternative constructors and utilities
- ✅ **Composition** - Building complex objects from simpler ones

### 2. **design_patterns.py**
Common design patterns implementation:
- ✅ **Singleton Pattern** - Ensure only one instance exists
- ✅ **Factory Pattern** - Create objects without specifying exact class
- ✅ **Observer Pattern** - Notify multiple objects of state changes
- ✅ **Strategy Pattern** - Encapsulate interchangeable algorithms
- ✅ **Decorator Pattern** - Add functionality dynamically
- ✅ **Builder Pattern** - Construct complex objects step-by-step

### 3. **solid_principles.py**
SOLID principles for better software design:
- ✅ **Single Responsibility** - One reason to change
- ✅ **Open/Closed** - Open for extension, closed for modification
- ✅ **Liskov Substitution** - Subtypes must be substitutable
- ✅ **Interface Segregation** - Specific interfaces over general ones
- ✅ **Dependency Inversion** - Depend on abstractions

## 🚀 Running the Examples

### Prerequisites
```bash
# Python 3.7 or higher required
python --version
```

### Run Individual Files
```bash
# OOP Fundamentals
python oop_fundamentals.py

# Design Patterns
python design_patterns.py

# SOLID Principles
python solid_principles.py
```

## 💡 Key Concepts Explained

### Classes vs Objects
```python
# Class is a blueprint
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

# Object is an instance
emp1 = Employee("Alice", 75000)
emp2 = Employee("Bob", 82000)
```

### Encapsulation Levels
```python
class Example:
    def __init__(self):
        self.public = "Accessible anywhere"
        self._protected = "Accessible in class and subclasses"
        self.__private = "Accessible only in this class"
```

### Inheritance Hierarchy
```
      Person
        |
    +---+---+
    |       |
Developer  Manager
```

### Polymorphism Example
```python
# Same method, different behavior
shapes = [Rectangle(5, 4), Circle(3), Triangle(3, 4, 5)]
for shape in shapes:
    print(shape.area())  # Each shape calculates area differently
```

## 🎯 Design Patterns Categories

### Creational Patterns
- **Singleton**: One instance only
- **Factory**: Object creation interface
- **Builder**: Step-by-step construction

### Structural Patterns
- **Decorator**: Add functionality dynamically
- **Adapter**: Make incompatible interfaces work
- **Facade**: Simplified interface

### Behavioral Patterns
- **Observer**: Event notification system
- **Strategy**: Interchangeable algorithms
- **Command**: Encapsulate requests

## 📖 SOLID Benefits

| Principle | Benefit |
|-----------|---------|
| **S**ingle Responsibility | Easier to maintain |
| **O**pen/Closed | Extensible without modification |
| **L**iskov Substitution | Predictable behavior |
| **I**nterface Segregation | Focused interfaces |
| **D**ependency Inversion | Loose coupling, testable |

## 🏗️ Best Practices

### 1. Favor Composition Over Inheritance
```python
# Instead of: class Car(Engine, GPS, Radio)
# Use: 
class Car:
    def __init__(self, engine, gps, radio):
        self.engine = engine
        self.gps = gps
        self.radio = radio
```

### 2. Use Abstract Base Classes
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
```

### 3. Dependency Injection
```python
class UserService:
    def __init__(self, database: Database):
        self.db = database  # Injected dependency
```

### 4. Properties for Controlled Access
```python
class BankAccount:
    @property
    def balance(self):
        return self.__balance
    
    @balance.setter
    def balance(self, value):
        if value >= 0:
            self.__balance = value
```

## 🔍 Common Use Cases

### When to Use Inheritance
- Clear "is-a" relationship
- Code reuse across related classes
- Example: `Dog is-a Animal`

### When to Use Composition
- "has-a" relationship
- More flexibility needed
- Example: `Car has-a Engine`

### When to Use Interfaces/Abstract Classes
- Define contracts
- Ensure consistent implementation
- Enable polymorphism

## 📚 Learning Path

1. **Start with Fundamentals**
   - Classes and objects
   - Methods and attributes
   - Basic encapsulation

2. **Master Core Principles**
   - Inheritance
   - Polymorphism
   - Abstraction

3. **Learn Design Patterns**
   - Start with common patterns (Factory, Singleton)
   - Understand when to apply each

4. **Apply SOLID Principles**
   - Refactor existing code
   - Design new features with SOLID in mind

## 🎓 Real-World Applications

### E-Commerce System
- **Product** class hierarchy (inheritance)
- **PaymentProcessor** interface (abstraction)
- **ShoppingCart** composition (has-a products)
- **OrderProcessor** with dependency injection

### Banking Application
- **Account** base class
- **SavingsAccount**, **CheckingAccount** (inheritance)
- **Transaction** observer pattern
- Encapsulation for sensitive data

### Game Development
- **Character** base class
- **Weapon**, **Armor** composition
- **Strategy** pattern for AI behavior
- **Factory** for creating enemies

## 🛠️ Tools and IDE Support

### VS Code Extensions
- Python extension (IntelliSense)
- Pylance (type checking)
- Code snippets for classes

### Type Hints
```python
from typing import List, Optional

class Repository:
    def find_all(self) -> List[Employee]:
        pass
    
    def find_by_id(self, id: int) -> Optional[Employee]:
        pass
```

## 📊 Performance Considerations

- **Inheritance depth**: Keep hierarchies shallow (2-3 levels)
- **Multiple inheritance**: Use carefully (consider mixins)
- **Property overhead**: Minimal for most use cases
- **Composition**: Slightly more memory, but more flexible

## 🔗 Related Resources

- [Python Official Docs - Classes](https://docs.python.org/3/tutorial/classes.html)
- [Design Patterns: Gang of Four](https://refactoring.guru/design-patterns)
- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

## ✅ Skills Demonstrated

- ✅ Advanced Python OOP concepts
- ✅ Design pattern implementation
- ✅ SOLID principles application
- ✅ Code organization and structure
- ✅ Abstract thinking and modeling
- ✅ Software architecture best practices

---

**Note**: These examples are designed for learning and demonstration. In production code, add comprehensive error handling, logging, and documentation.
