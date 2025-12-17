"""
Design Patterns in Python
Demonstrates: Singleton, Factory, Observer, Strategy, Decorator patterns
"""

# ===== 1. SINGLETON PATTERN =====
print("=" * 60)
print("1. SINGLETON PATTERN - Only One Instance")
print("=" * 60)

class DatabaseConnection:
    """Singleton: Ensures only one database connection exists"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            print("Creating new database connection...")
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.connection_string = "Server=localhost;Database=MyDB"
            self._initialized = True
    
    def query(self, sql):
        return f"Executing: {sql}"

# Test singleton
db1 = DatabaseConnection()
db2 = DatabaseConnection()

print(f"\ndb1 is db2? {db1 is db2}")  # True - same instance
print(f"db1 ID: {id(db1)}")
print(f"db2 ID: {id(db2)}")


# ===== 2. FACTORY PATTERN =====
print("\n" + "=" * 60)
print("2. FACTORY PATTERN - Object Creation")
print("=" * 60)

from abc import ABC, abstractmethod

class Notification(ABC):
    """Abstract product"""
    
    @abstractmethod
    def send(self, message):
        pass

class EmailNotification(Notification):
    """Concrete product: Email"""
    
    def send(self, message):
        return f"📧 Email sent: {message}"

class SMSNotification(Notification):
    """Concrete product: SMS"""
    
    def send(self, message):
        return f"📱 SMS sent: {message}"

class PushNotification(Notification):
    """Concrete product: Push"""
    
    def send(self, message):
        return f"🔔 Push notification sent: {message}"

class NotificationFactory:
    """Factory: Creates notification objects"""
    
    @staticmethod
    def create_notification(notification_type):
        """Factory method"""
        notifications = {
            'email': EmailNotification,
            'sms': SMSNotification,
            'push': PushNotification
        }
        
        notification_class = notifications.get(notification_type.lower())
        if notification_class:
            return notification_class()
        raise ValueError(f"Unknown notification type: {notification_type}")

# Using the factory
print("\nUsing Notification Factory:")
for notification_type in ['email', 'sms', 'push']:
    notifier = NotificationFactory.create_notification(notification_type)
    print(f"  {notifier.send('Hello, user!')}")


# ===== 3. OBSERVER PATTERN =====
print("\n" + "=" * 60)
print("3. OBSERVER PATTERN - Event Notification")
print("=" * 60)

class Subject:
    """Subject that observers watch"""
    
    def __init__(self):
        self._observers = []
        self._state = None
    
    def attach(self, observer):
        """Add observer"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        """Remove observer"""
        self._observers.remove(observer)
    
    def notify(self):
        """Notify all observers"""
        for observer in self._observers:
            observer.update(self)
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        self._state = value
        self.notify()

class Observer(ABC):
    """Abstract observer"""
    
    @abstractmethod
    def update(self, subject):
        pass

class EmailAlert(Observer):
    """Concrete observer: Email alerts"""
    
    def update(self, subject):
        print(f"  📧 Email Alert: State changed to {subject.state}")

class SMSAlert(Observer):
    """Concrete observer: SMS alerts"""
    
    def update(self, subject):
        print(f"  📱 SMS Alert: State changed to {subject.state}")

class LogAlert(Observer):
    """Concrete observer: Logging"""
    
    def update(self, subject):
        print(f"  📝 Log: State changed to {subject.state}")

# Using observer pattern
print("\nStock Price Monitoring:")
stock = Subject()

# Attach observers
email_alert = EmailAlert()
sms_alert = SMSAlert()
log_alert = LogAlert()

stock.attach(email_alert)
stock.attach(sms_alert)
stock.attach(log_alert)

# Change state - all observers notified
print("\nUpdating stock price to $150:")
stock.state = "$150"

print("\nUpdating stock price to $175:")
stock.state = "$175"


# ===== 4. STRATEGY PATTERN =====
print("\n" + "=" * 60)
print("4. STRATEGY PATTERN - Interchangeable Algorithms")
print("=" * 60)

class PaymentStrategy(ABC):
    """Abstract strategy"""
    
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentStrategy):
    """Concrete strategy: Credit Card"""
    
    def __init__(self, card_number):
        self.card_number = card_number
    
    def pay(self, amount):
        return f"💳 Paid ${amount:.2f} using Credit Card ending in {self.card_number[-4:]}"

class PayPalPayment(PaymentStrategy):
    """Concrete strategy: PayPal"""
    
    def __init__(self, email):
        self.email = email
    
    def pay(self, amount):
        return f"🌐 Paid ${amount:.2f} using PayPal ({self.email})"

class CryptoPayment(PaymentStrategy):
    """Concrete strategy: Cryptocurrency"""
    
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address
    
    def pay(self, amount):
        return f"₿ Paid ${amount:.2f} using Crypto (Wallet: {self.wallet_address[:8]}...)"

class ShoppingCart:
    """Context that uses strategy"""
    
    def __init__(self):
        self.items = []
        self.payment_strategy = None
    
    def add_item(self, item, price):
        self.items.append((item, price))
    
    def get_total(self):
        return sum(price for _, price in self.items)
    
    def set_payment_strategy(self, strategy):
        self.payment_strategy = strategy
    
    def checkout(self):
        if not self.payment_strategy:
            return "Please select a payment method"
        
        total = self.get_total()
        return self.payment_strategy.pay(total)

# Using strategy pattern
cart = ShoppingCart()
cart.add_item("Laptop", 999.99)
cart.add_item("Mouse", 29.99)
cart.add_item("Keyboard", 79.99)

print(f"\nCart Total: ${cart.get_total():.2f}")

print("\nPaying with different strategies:")
# Pay with credit card
cart.set_payment_strategy(CreditCardPayment("1234567890123456"))
print(f"  {cart.checkout()}")

# Pay with PayPal
cart.set_payment_strategy(PayPalPayment("user@example.com"))
print(f"  {cart.checkout()}")

# Pay with crypto
cart.set_payment_strategy(CryptoPayment("1A2B3C4D5E6F7G8H"))
print(f"  {cart.checkout()}")


# ===== 5. DECORATOR PATTERN =====
print("\n" + "=" * 60)
print("5. DECORATOR PATTERN - Adding Functionality")
print("=" * 60)

class Coffee(ABC):
    """Abstract component"""
    
    @abstractmethod
    def get_cost(self):
        pass
    
    @abstractmethod
    def get_description(self):
        pass

class SimpleCoffee(Coffee):
    """Concrete component"""
    
    def get_cost(self):
        return 2.00
    
    def get_description(self):
        return "Simple Coffee"

class CoffeeDecorator(Coffee):
    """Base decorator"""
    
    def __init__(self, coffee):
        self._coffee = coffee
    
    def get_cost(self):
        return self._coffee.get_cost()
    
    def get_description(self):
        return self._coffee.get_description()

class MilkDecorator(CoffeeDecorator):
    """Concrete decorator: Milk"""
    
    def get_cost(self):
        return self._coffee.get_cost() + 0.50
    
    def get_description(self):
        return self._coffee.get_description() + ", Milk"

class SugarDecorator(CoffeeDecorator):
    """Concrete decorator: Sugar"""
    
    def get_cost(self):
        return self._coffee.get_cost() + 0.25
    
    def get_description(self):
        return self._coffee.get_description() + ", Sugar"

class WhippedCreamDecorator(CoffeeDecorator):
    """Concrete decorator: Whipped Cream"""
    
    def get_cost(self):
        return self._coffee.get_cost() + 0.75
    
    def get_description(self):
        return self._coffee.get_description() + ", Whipped Cream"

# Using decorator pattern
print("\nBuilding custom coffee:")

# Simple coffee
coffee = SimpleCoffee()
print(f"{coffee.get_description()}: ${coffee.get_cost():.2f}")

# Coffee with milk
coffee = MilkDecorator(SimpleCoffee())
print(f"{coffee.get_description()}: ${coffee.get_cost():.2f}")

# Coffee with milk and sugar
coffee = SugarDecorator(MilkDecorator(SimpleCoffee()))
print(f"{coffee.get_description()}: ${coffee.get_cost():.2f}")

# Fancy coffee with everything
coffee = WhippedCreamDecorator(SugarDecorator(MilkDecorator(SimpleCoffee())))
print(f"{coffee.get_description()}: ${coffee.get_cost():.2f}")


# ===== 6. BUILDER PATTERN =====
print("\n" + "=" * 60)
print("6. BUILDER PATTERN - Complex Object Construction")
print("=" * 60)

class Computer:
    """Product being built"""
    
    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = None
    
    def __str__(self):
        parts = []
        if self.cpu:
            parts.append(f"CPU: {self.cpu}")
        if self.ram:
            parts.append(f"RAM: {self.ram}GB")
        if self.storage:
            parts.append(f"Storage: {self.storage}GB")
        if self.gpu:
            parts.append(f"GPU: {self.gpu}")
        return f"Computer({', '.join(parts)})"

class ComputerBuilder:
    """Builder for creating computers"""
    
    def __init__(self):
        self.computer = Computer()
    
    def set_cpu(self, cpu):
        self.computer.cpu = cpu
        return self  # Enable method chaining
    
    def set_ram(self, ram):
        self.computer.ram = ram
        return self
    
    def set_storage(self, storage):
        self.computer.storage = storage
        return self
    
    def set_gpu(self, gpu):
        self.computer.gpu = gpu
        return self
    
    def build(self):
        return self.computer

# Using builder pattern
print("\nBuilding custom computers:")

# Gaming PC
gaming_pc = (ComputerBuilder()
             .set_cpu("Intel i9")
             .set_ram(32)
             .set_storage(1000)
             .set_gpu("RTX 4090")
             .build())
print(f"Gaming PC: {gaming_pc}")

# Office PC
office_pc = (ComputerBuilder()
             .set_cpu("Intel i5")
             .set_ram(16)
             .set_storage(512)
             .build())
print(f"Office PC: {office_pc}")


# ===== SUMMARY =====
print("\n" + "=" * 60)
print("DESIGN PATTERNS SUMMARY")
print("=" * 60)
print("""
1. ✅ Singleton: Ensure only one instance exists
2. ✅ Factory: Create objects without specifying exact class
3. ✅ Observer: Notify multiple objects of state changes
4. ✅ Strategy: Encapsulate interchangeable algorithms
5. ✅ Decorator: Add functionality to objects dynamically
6. ✅ Builder: Construct complex objects step-by-step

Design Pattern Categories:
• Creational: Singleton, Factory, Builder
• Structural: Decorator, Adapter, Facade
• Behavioral: Observer, Strategy, Command
""")

if __name__ == "__main__":
    print("\n✓ Design Patterns demonstration completed!")
