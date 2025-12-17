"""
SOLID Principles in Python
Demonstrates: Single Responsibility, Open/Closed, Liskov Substitution,
              Interface Segregation, Dependency Inversion
"""

from abc import ABC, abstractmethod
from typing import List

# ===== 1. SINGLE RESPONSIBILITY PRINCIPLE (SRP) =====
print("=" * 60)
print("1. SINGLE RESPONSIBILITY PRINCIPLE")
print("Each class should have only one reason to change")
print("=" * 60)

# ❌ BAD: Multiple responsibilities
class BadEmployee:
    """Violates SRP - handles employee data, database, and reporting"""
    
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    
    def calculate_pay(self):
        """Business logic"""
        return self.salary
    
    def save_to_database(self):
        """Database operation"""
        print(f"Saving {self.name} to database")
    
    def generate_report(self):
        """Reporting"""
        return f"Employee Report: {self.name}"

# ✅ GOOD: Separate responsibilities
class Employee:
    """Only handles employee data"""
    
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    
    def calculate_pay(self):
        return self.salary

class EmployeeRepository:
    """Only handles database operations"""
    
    def save(self, employee):
        print(f"Saving {employee.name} to database")
        return True
    
    def find_by_name(self, name):
        print(f"Finding employee: {name}")
        return None

class EmployeeReportGenerator:
    """Only handles report generation"""
    
    def generate_report(self, employee):
        return f"Employee Report: {employee.name}, Salary: ${employee.salary:,}"

# Using SRP
print("\n✅ Good design with SRP:")
emp = Employee("Alice Johnson", 75000)
repo = EmployeeRepository()
report_gen = EmployeeReportGenerator()

repo.save(emp)
print(report_gen.generate_report(emp))


# ===== 2. OPEN/CLOSED PRINCIPLE (OCP) =====
print("\n" + "=" * 60)
print("2. OPEN/CLOSED PRINCIPLE")
print("Open for extension, closed for modification")
print("=" * 60)

# ❌ BAD: Must modify class to add new shapes
class BadAreaCalculator:
    """Must modify this class for every new shape"""
    
    def calculate_area(self, shapes):
        total_area = 0
        for shape in shapes:
            if shape['type'] == 'rectangle':
                total_area += shape['width'] * shape['height']
            elif shape['type'] == 'circle':
                import math
                total_area += math.pi * shape['radius'] ** 2
            # Need to add elif for every new shape!
        return total_area

# ✅ GOOD: Extensible without modification
class Shape(ABC):
    """Abstract base class"""
    
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        import math
        return math.pi * self.radius ** 2

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height
    
    def area(self):
        return 0.5 * self.base * self.height

class AreaCalculator:
    """No modification needed for new shapes!"""
    
    def calculate_total_area(self, shapes: List[Shape]):
        return sum(shape.area() for shape in shapes)

# Using OCP
print("\n✅ Good design with OCP:")
shapes = [
    Rectangle(5, 4),
    Circle(3),
    Triangle(6, 4)
]
calculator = AreaCalculator()
total = calculator.calculate_total_area(shapes)
print(f"Total area: {total:.2f}")


# ===== 3. LISKOV SUBSTITUTION PRINCIPLE (LSP) =====
print("\n" + "=" * 60)
print("3. LISKOV SUBSTITUTION PRINCIPLE")
print("Subtypes must be substitutable for their base types")
print("=" * 60)

# ❌ BAD: Violates LSP - Square changes behavior unexpectedly
class BadRectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def set_width(self, width):
        self.width = width
    
    def set_height(self, height):
        self.height = height
    
    def area(self):
        return self.width * self.height

class BadSquare(BadRectangle):
    """Violates LSP - changes width/height behavior"""
    
    def set_width(self, width):
        self.width = width
        self.height = width  # Square must have equal sides
    
    def set_height(self, height):
        self.width = height
        self.height = height

# ✅ GOOD: Follows LSP - use composition instead
class GoodShape(ABC):
    @abstractmethod
    def area(self):
        pass

class GoodRectangle(GoodShape):
    def __init__(self, width, height):
        self._width = width
        self._height = height
    
    def area(self):
        return self._width * self._height

class GoodSquare(GoodShape):
    def __init__(self, side):
        self._side = side
    
    def area(self):
        return self._side ** 2

# Using LSP
print("\n✅ Good design with LSP:")
shapes = [
    GoodRectangle(5, 4),
    GoodSquare(5)
]
for i, shape in enumerate(shapes, 1):
    print(f"Shape {i} area: {shape.area()}")


# ===== 4. INTERFACE SEGREGATION PRINCIPLE (ISP) =====
print("\n" + "=" * 60)
print("4. INTERFACE SEGREGATION PRINCIPLE")
print("Clients shouldn't depend on interfaces they don't use")
print("=" * 60)

# ❌ BAD: Fat interface forces unnecessary implementations
class BadWorker(ABC):
    """Fat interface - not all workers need all methods"""
    
    @abstractmethod
    def work(self):
        pass
    
    @abstractmethod
    def eat(self):
        pass
    
    @abstractmethod
    def sleep(self):
        pass

class BadRobot(BadWorker):
    """Robot forced to implement eat() and sleep()"""
    
    def work(self):
        return "Robot working"
    
    def eat(self):
        raise NotImplementedError("Robots don't eat!")
    
    def sleep(self):
        raise NotImplementedError("Robots don't sleep!")

# ✅ GOOD: Segregated interfaces
class Workable(ABC):
    @abstractmethod
    def work(self):
        pass

class Eatable(ABC):
    @abstractmethod
    def eat(self):
        pass

class Sleepable(ABC):
    @abstractmethod
    def sleep(self):
        pass

class Human(Workable, Eatable, Sleepable):
    """Human implements all interfaces"""
    
    def work(self):
        return "Human working"
    
    def eat(self):
        return "Human eating"
    
    def sleep(self):
        return "Human sleeping"

class Robot(Workable):
    """Robot only implements what it needs"""
    
    def work(self):
        return "Robot working"

# Using ISP
print("\n✅ Good design with ISP:")
human = Human()
robot = Robot()

print(f"Human: {human.work()}, {human.eat()}, {human.sleep()}")
print(f"Robot: {robot.work()}")


# ===== 5. DEPENDENCY INVERSION PRINCIPLE (DIP) =====
print("\n" + "=" * 60)
print("5. DEPENDENCY INVERSION PRINCIPLE")
print("Depend on abstractions, not concretions")
print("=" * 60)

# ❌ BAD: High-level module depends on low-level module
class MySQLDatabase:
    """Concrete implementation"""
    
    def save(self, data):
        print(f"Saving to MySQL: {data}")

class BadUserService:
    """Depends on concrete MySQLDatabase"""
    
    def __init__(self):
        self.db = MySQLDatabase()  # Tight coupling!
    
    def save_user(self, user):
        self.db.save(user)

# ✅ GOOD: Both depend on abstraction
class Database(ABC):
    """Abstract interface"""
    
    @abstractmethod
    def save(self, data):
        pass

class MySQLDB(Database):
    """Concrete implementation"""
    
    def save(self, data):
        print(f"💾 Saving to MySQL: {data}")

class PostgresDB(Database):
    """Another concrete implementation"""
    
    def save(self, data):
        print(f"🐘 Saving to PostgreSQL: {data}")

class MongoDBDatabase(Database):
    """Another concrete implementation"""
    
    def save(self, data):
        print(f"🍃 Saving to MongoDB: {data}")

class UserService:
    """Depends on abstraction (Database)"""
    
    def __init__(self, database: Database):
        self.db = database  # Dependency injection!
    
    def save_user(self, user):
        self.db.save(user)

# Using DIP
print("\n✅ Good design with DIP:")
user_data = {"name": "Alice", "email": "alice@example.com"}

# Can easily switch databases
mysql_service = UserService(MySQLDB())
mysql_service.save_user(user_data)

postgres_service = UserService(PostgresDB())
postgres_service.save_user(user_data)

mongo_service = UserService(MongoDBDatabase())
mongo_service.save_user(user_data)


# ===== PRACTICAL EXAMPLE: E-COMMERCE SYSTEM =====
print("\n" + "=" * 60)
print("PRACTICAL EXAMPLE: E-Commerce with SOLID")
print("=" * 60)

# Interfaces (Dependency Inversion)
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class NotificationService(ABC):
    @abstractmethod
    def send(self, message):
        pass

# Concrete implementations
class StripePayment(PaymentProcessor):
    def process_payment(self, amount):
        return f"Processing ${amount:.2f} via Stripe"

class EmailNotification(NotificationService):
    def send(self, message):
        return f"📧 Email: {message}"

# Single Responsibility
class Order:
    """Only handles order data"""
    
    def __init__(self, order_id, items, total):
        self.order_id = order_id
        self.items = items
        self.total = total

class OrderProcessor:
    """Handles order processing logic"""
    
    def __init__(self, payment_processor: PaymentProcessor, 
                 notification_service: NotificationService):
        self.payment_processor = payment_processor
        self.notification_service = notification_service
    
    def process_order(self, order: Order):
        """Process order using injected dependencies"""
        # Process payment
        payment_result = self.payment_processor.process_payment(order.total)
        print(f"  {payment_result}")
        
        # Send notification
        notification = self.notification_service.send(
            f"Order #{order.order_id} processed successfully"
        )
        print(f"  {notification}")
        
        return True

# Using the system
print("\nProcessing orders:")
order = Order("ORD-001", ["Laptop", "Mouse"], 1029.98)

processor = OrderProcessor(
    StripePayment(),
    EmailNotification()
)

processor.process_order(order)


# ===== SUMMARY =====
print("\n" + "=" * 60)
print("SOLID PRINCIPLES SUMMARY")
print("=" * 60)
print("""
S - Single Responsibility Principle
    ✅ Each class has one reason to change
    ✅ Separate concerns: data, persistence, reporting

O - Open/Closed Principle
    ✅ Open for extension, closed for modification
    ✅ Use abstraction and polymorphism

L - Liskov Substitution Principle
    ✅ Subtypes must be substitutable for base types
    ✅ Don't break expected behavior

I - Interface Segregation Principle
    ✅ Many specific interfaces > one general interface
    ✅ Clients shouldn't depend on unused methods

D - Dependency Inversion Principle
    ✅ Depend on abstractions, not concrete classes
    ✅ Use dependency injection

Benefits:
• More maintainable code
• Easier to test
• More flexible and extensible
• Reduces coupling
• Improves code reusability
""")

if __name__ == "__main__":
    print("\n✓ SOLID Principles demonstration completed!")
