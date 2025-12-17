"""
Object-Oriented Programming Fundamentals
Demonstrates: Classes, Objects, Encapsulation, Inheritance, Polymorphism, Abstraction
"""

# ===== 1. CLASSES AND OBJECTS =====
print("=" * 60)
print("1. CLASSES AND OBJECTS")
print("=" * 60)

class Employee:
    """
    Basic class demonstrating class and instance attributes
    """
    # Class attribute (shared by all instances)
    company_name = "TechCorp Inc."
    employee_count = 0
    
    def __init__(self, first_name, last_name, salary):
        """Initialize employee instance"""
        # Instance attributes (unique to each object)
        self.first_name = first_name
        self.last_name = last_name
        self.salary = salary
        Employee.employee_count += 1
    
    def get_full_name(self):
        """Return full name"""
        return f"{self.first_name} {self.last_name}"
    
    def give_raise(self, amount):
        """Increase salary"""
        self.salary += amount
        return self.salary
    
    def __str__(self):
        """String representation"""
        return f"{self.get_full_name()} - ${self.salary:,}"
    
    def __repr__(self):
        """Developer-friendly representation"""
        return f"Employee('{self.first_name}', '{self.last_name}', {self.salary})"

# Creating objects (instances)
emp1 = Employee("Alice", "Johnson", 75000)
emp2 = Employee("Bob", "Smith", 82000)

print(f"\nCreated {Employee.employee_count} employees")
print(f"Employee 1: {emp1}")
print(f"Employee 2: {emp2}")

emp1.give_raise(5000)
print(f"\nAfter raise: {emp1}")


# ===== 2. ENCAPSULATION (Data Hiding) =====
print("\n" + "=" * 60)
print("2. ENCAPSULATION - PUBLIC, PROTECTED, PRIVATE")
print("=" * 60)

class BankAccount:
    """
    Demonstrates encapsulation with private attributes
    """
    
    def __init__(self, account_holder, initial_balance=0):
        self.account_holder = account_holder  # Public
        self._account_number = self._generate_account_number()  # Protected
        self.__balance = initial_balance  # Private
    
    def _generate_account_number(self):
        """Protected method - meant for internal use"""
        import random
        return f"ACC{random.randint(10000, 99999)}"
    
    def deposit(self, amount):
        """Public method to deposit money"""
        if amount > 0:
            self.__balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        """Public method to withdraw money"""
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False
    
    def get_balance(self):
        """Getter for private balance"""
        return self.__balance
    
    @property
    def balance(self):
        """Property decorator for controlled access"""
        return self.__balance
    
    @balance.setter
    def balance(self, value):
        """Setter with validation"""
        if value >= 0:
            self.__balance = value
        else:
            raise ValueError("Balance cannot be negative")
    
    def __str__(self):
        return f"Account {self._account_number}: ${self.__balance:,.2f}"

account = BankAccount("Alice Johnson", 1000)
print(f"\nInitial: {account}")

account.deposit(500)
print(f"After deposit: {account}")

account.withdraw(200)
print(f"After withdrawal: {account}")

# Using property
print(f"Balance (via property): ${account.balance:,.2f}")


# ===== 3. INHERITANCE =====
print("\n" + "=" * 60)
print("3. INHERITANCE - REUSING CODE")
print("=" * 60)

class Person:
    """Base class"""
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"Hi, I'm {self.name}, {self.age} years old"
    
    def work(self):
        return "I am working"

class Developer(Person):
    """Derived class inheriting from Person"""
    
    def __init__(self, name, age, programming_languages):
        super().__init__(name, age)  # Call parent constructor
        self.programming_languages = programming_languages
    
    def code(self):
        """Method specific to Developer"""
        langs = ', '.join(self.programming_languages)
        return f"{self.name} codes in: {langs}"
    
    def work(self):
        """Override parent method"""
        return f"I am coding in {self.programming_languages[0]}"

class Manager(Person):
    """Another derived class"""
    
    def __init__(self, name, age, team_size):
        super().__init__(name, age)
        self.team_size = team_size
    
    def work(self):
        """Override parent method"""
        return f"I am managing {self.team_size} people"
    
    def conduct_meeting(self):
        return f"{self.name} is conducting a team meeting"

# Creating instances
dev = Developer("Alice", 28, ["Python", "JavaScript", "Go"])
mgr = Manager("Bob", 35, 8)

print(f"\nDeveloper: {dev.introduce()}")
print(f"  {dev.code()}")
print(f"  {dev.work()}")

print(f"\nManager: {mgr.introduce()}")
print(f"  {mgr.conduct_meeting()}")
print(f"  {mgr.work()}")


# ===== 4. POLYMORPHISM =====
print("\n" + "=" * 60)
print("4. POLYMORPHISM - SAME INTERFACE, DIFFERENT BEHAVIOR")
print("=" * 60)

class Shape:
    """Base class for shapes"""
    
    def area(self):
        """To be overridden by subclasses"""
        raise NotImplementedError("Subclass must implement area()")
    
    def perimeter(self):
        """To be overridden by subclasses"""
        raise NotImplementedError("Subclass must implement perimeter()")

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
    
    def __str__(self):
        return f"Rectangle({self.width}x{self.height})"

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        import math
        return 2 * math.pi * self.radius
    
    def __str__(self):
        return f"Circle(r={self.radius})"

class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    def area(self):
        # Heron's formula
        s = self.perimeter() / 2
        return (s * (s - self.a) * (s - self.b) * (s - self.c)) ** 0.5
    
    def perimeter(self):
        return self.a + self.b + self.c
    
    def __str__(self):
        return f"Triangle({self.a}, {self.b}, {self.c})"

# Polymorphism in action - same method call, different behavior
shapes = [
    Rectangle(5, 4),
    Circle(3),
    Triangle(3, 4, 5)
]

print("\nCalculating areas and perimeters for different shapes:")
for shape in shapes:
    print(f"{shape}")
    print(f"  Area: {shape.area():.2f}")
    print(f"  Perimeter: {shape.perimeter():.2f}")


# ===== 5. ABSTRACTION =====
print("\n" + "=" * 60)
print("5. ABSTRACTION - ABSTRACT BASE CLASSES")
print("=" * 60)

from abc import ABC, abstractmethod

class Vehicle(ABC):
    """Abstract base class - cannot be instantiated"""
    
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    @abstractmethod
    def start_engine(self):
        """Abstract method - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def stop_engine(self):
        """Abstract method"""
        pass
    
    def get_info(self):
        """Concrete method - can be used as is"""
        return f"{self.brand} {self.model}"

class Car(Vehicle):
    """Concrete implementation of Vehicle"""
    
    def __init__(self, brand, model, num_doors):
        super().__init__(brand, model)
        self.num_doors = num_doors
    
    def start_engine(self):
        return f"Car engine started: Vroom! 🚗"
    
    def stop_engine(self):
        return f"Car engine stopped"

class Motorcycle(Vehicle):
    """Another concrete implementation"""
    
    def __init__(self, brand, model, engine_cc):
        super().__init__(brand, model)
        self.engine_cc = engine_cc
    
    def start_engine(self):
        return f"Motorcycle engine started: VROOOM! 🏍️"
    
    def stop_engine(self):
        return f"Motorcycle engine stopped"

# Create instances
car = Car("Toyota", "Camry", 4)
bike = Motorcycle("Harley-Davidson", "Street 750", 750)

vehicles = [car, bike]

print("\nDemonstrating abstraction:")
for vehicle in vehicles:
    print(f"\n{vehicle.get_info()}")
    print(f"  {vehicle.start_engine()}")
    print(f"  {vehicle.stop_engine()}")


# ===== 6. MULTIPLE INHERITANCE =====
print("\n" + "=" * 60)
print("6. MULTIPLE INHERITANCE")
print("=" * 60)

class Flyable:
    """Mixin for flying capability"""
    
    def fly(self):
        return "Flying in the air ✈️"

class Swimmable:
    """Mixin for swimming capability"""
    
    def swim(self):
        return "Swimming in water 🏊"

class Duck(Flyable, Swimmable):
    """Duck can both fly and swim"""
    
    def __init__(self, name):
        self.name = name
    
    def quack(self):
        return f"{self.name} says: Quack! 🦆"

class Penguin(Swimmable):
    """Penguin can only swim"""
    
    def __init__(self, name):
        self.name = name
    
    def waddle(self):
        return f"{self.name} waddles 🐧"

duck = Duck("Donald")
penguin = Penguin("Pingu")

print(f"\nDuck ({duck.name}):")
print(f"  {duck.fly()}")
print(f"  {duck.swim()}")
print(f"  {duck.quack()}")

print(f"\nPenguin ({penguin.name}):")
print(f"  {penguin.swim()}")
print(f"  {penguin.waddle()}")


# ===== 7. CLASS METHODS AND STATIC METHODS =====
print("\n" + "=" * 60)
print("7. CLASS METHODS AND STATIC METHODS")
print("=" * 60)

class Date:
    """Demonstrates class methods and static methods"""
    
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    @classmethod
    def from_string(cls, date_string):
        """Alternative constructor using class method"""
        year, month, day = map(int, date_string.split('-'))
        return cls(year, month, day)
    
    @staticmethod
    def is_leap_year(year):
        """Static method - doesn't need instance or class"""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    def __str__(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"

# Regular instantiation
date1 = Date(2024, 12, 17)
print(f"\nRegular instantiation: {date1}")

# Using class method
date2 = Date.from_string("2024-06-15")
print(f"From class method: {date2}")

# Using static method
print(f"Is 2024 a leap year? {Date.is_leap_year(2024)}")
print(f"Is 2023 a leap year? {Date.is_leap_year(2023)}")


# ===== 8. COMPOSITION OVER INHERITANCE =====
print("\n" + "=" * 60)
print("8. COMPOSITION - HAS-A RELATIONSHIP")
print("=" * 60)

class Engine:
    """Component class"""
    
    def __init__(self, horsepower, fuel_type):
        self.horsepower = horsepower
        self.fuel_type = fuel_type
    
    def start(self):
        return f"Starting {self.horsepower}HP {self.fuel_type} engine"
    
    def __str__(self):
        return f"{self.horsepower}HP {self.fuel_type} engine"

class GPS:
    """Another component class"""
    
    def get_route(self, destination):
        return f"Calculating route to {destination}"

class AutoCar:
    """Composition: Car HAS-A engine and GPS"""
    
    def __init__(self, brand, model, engine, gps=None):
        self.brand = brand
        self.model = model
        self.engine = engine  # Composition
        self.gps = gps  # Optional composition
    
    def start(self):
        return f"{self.brand} {self.model}: {self.engine.start()}"
    
    def navigate_to(self, destination):
        if self.gps:
            return self.gps.get_route(destination)
        return "No GPS available"
    
    def __str__(self):
        return f"{self.brand} {self.model} with {self.engine}"

# Create components
v6_engine = Engine(280, "Gasoline")
modern_gps = GPS()

# Compose them into a car
my_car = AutoCar("Honda", "Accord", v6_engine, modern_gps)

print(f"\nMy car: {my_car}")
print(f"  {my_car.start()}")
print(f"  {my_car.navigate_to('San Francisco')}")


# ===== SUMMARY =====
print("\n" + "=" * 60)
print("OOP PRINCIPLES SUMMARY")
print("=" * 60)
print("""
1. ✅ Classes & Objects: Blueprint and instances
2. ✅ Encapsulation: Data hiding with public/protected/private
3. ✅ Inheritance: Code reuse through parent-child relationship
4. ✅ Polymorphism: Same interface, different implementations
5. ✅ Abstraction: Abstract base classes with @abstractmethod
6. ✅ Multiple Inheritance: Inheriting from multiple classes
7. ✅ Class/Static Methods: Alternative constructors and utilities
8. ✅ Composition: Building complex objects from simpler ones
""")

if __name__ == "__main__":
    print("\n✓ OOP Fundamentals demonstration completed!")
