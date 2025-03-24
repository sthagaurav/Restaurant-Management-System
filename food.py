import datetime
import json
import os
from typing import List, Dict

from datetime import datetime
from enum import Enum
from typing import List, Dict

# Enums and Classes
class UserRole(Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    CHEF = "Chef"
    CUSTOMER = "Customer"

class OrderStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

class User:
    def __init__(self, id: int, username: str, password: str, role: UserRole, name: str):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.name = name

class MenuItem:
    def __init__(self, id: int, name: str, category: str, price: float):
        self.id = id
        self.name = name
        self.category = category
        self.price = price

class Order:
    def __init__(self, id: int, customer_id: int, items: List[tuple], total: float, status: OrderStatus):
        self.id = id
        self.customer_id = customer_id
        self.items = items  # List of tuples (item_id, quantity)
        self.total = total
        self.status = status
        self.timestamp = datetime.now()

class Feedback:
    def __init__(self, id: int, customer_id: int, message: str):
        self.id = id
        self.customer_id = customer_id
        self.message = message
        self.timestamp = datetime.now()

class IngredientRequest:
    def __init__(self, id: int, chef_id: int, ingredients: list, notes: str, status: str):
        self.id = id
        self.chef_id = chef_id
        self.ingredients = ingredients
        self.notes = notes
        self.status = status
        self.timestamp = datetime.now()

# Restaurant Management System
class RestaurantSystem:
    def __init__(self):
        # Initialize sample data
        self.users = [
            User(1, "admin", "admin123", UserRole.ADMIN, "Admin User"),
            User(2, "manager", "manager123", UserRole.MANAGER, "Manager User"),
            User(3, "chef", "chef123", UserRole.CHEF, "Chef User"),
            User(4, "customer", "customer123", UserRole.CUSTOMER, "Customer User")
        ]
        
        self.menu_items = [
            MenuItem(1, "Margherita Pizza", "Pizza", 12.99),
            MenuItem(2, "Pepperoni Pizza", "Pizza", 14.99),
            MenuItem(3, "Chicken Burger", "Burgers", 8.99),
            MenuItem(4, "Veggie Burger", "Burgers", 7.99)
        ]
        
        self.orders = []
        self.feedbacks = []
        self.ingredient_requests = []
        self.customer_carts = {}  # Dictionary to store customer carts

    def login(self) -> User:
        attempts = 0
        while attempts < 3:
            print("\n=== Login ===")
            username = input("Username: ")
            password = input("Password: ")
            
            user = next((u for u in self.users if u.username == username and u.password == password), None)
            
            if user:
                print(f"\nWelcome, {user.name}!")
                return user
            
            attempts += 1
            remaining = 3 - attempts
            print(f"Invalid credentials! {remaining} attempts remaining.")
        
        print("Maximum login attempts exceeded. System will now exit.")
        return None

    # Admin Functions
    def admin_menu(self, admin: User):
        while True:
            print(f"\n=== Administrator Menu ({admin.name}) ===")
            print("1. Manage Staff")
            print("2. View Sales Report")
            print("3. View Feedback")
            print("4. Update Profile")
            print("5. Logout")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == "1":
                self.manage_staff()
            elif choice == "2":
                self.view_sales_report()
            elif choice == "3":
                self.view_all_feedback()
            elif choice == "4":
                self.update_user_profile(admin)
            elif choice == "5":
                break

    def manage_staff(self):
        while True:
            print("\n=== Staff Management ===")
            print("1. Add Staff")
            print("2. Edit Staff")
            print("3. Delete Staff")
            print("4. View Staff")
            print("5. Back")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == "1":
                username = input("Enter username: ")
                password = input("Enter password: ")
                name = input("Enter name: ")
                print("Select role:")
                print("1. Manager")
                print("2. Chef")
                role_choice = input("Enter choice (1-2): ")
                
                role = UserRole.MANAGER if role_choice == "1" else UserRole.CHEF
                user_id = max(u.id for u in self.users) + 1
                self.users.append(User(user_id, username, password, role, name))
                print("Staff added successfully!")
                
            elif choice == "2":
                self.view_staff()
                user_id = int(input("Enter staff ID to edit: "))
                user = next((u for u in self.users if u.id == user_id), None)
                if user and user.role != UserRole.ADMIN:
                    user.username = input("Enter new username: ")
                    user.password = input("Enter new password: ")
                    user.name = input("Enter new name: ")
                    print("Staff updated successfully!")
                else:
                    print("Invalid staff ID!")
                    
            elif choice == "3":
                self.view_staff()
                user_id = int(input("Enter staff ID to delete: "))
                self.users = [u for u in self.users if u.id != user_id or u.role == UserRole.ADMIN]
                print("Staff deleted successfully!")
                
            elif choice == "4":
                self.view_staff()
                
            elif choice == "5":
                break

    def view_staff(self):
        print("\n=== Staff List ===")
        for user in self.users:
            if user.role != UserRole.CUSTOMER:
                print(f"ID: {user.id}, Name: {user.name}, Role: {user.role.value}")

    def view_sales_report(self):
        total_sales = sum(order.total for order in self.orders)
        print(f"\nTotal Sales: ${total_sales:.2f}")
        
        # Group by chef
        chef_sales = {}
        for order in self.orders:
            if order.status == OrderStatus.COMPLETED:
                chef_sales[order.chef_id] = chef_sales.get(order.chef_id, 0) + order.total
        
        print("\nSales by Chef:")
        for chef_id, sales in chef_sales.items():
            chef = next((u for u in self.users if u.id == chef_id), None)
            if chef:
                print(f"{chef.name}: ${sales:.2f}")

    # Manager Functions
    def manager_menu(self, manager: User):
        while True:
            print(f"\n=== Manager Menu ({manager.name}) ===")
            print("1. Manage Menu")
            print("2. View Ingredient Requests")
            print("3. Update Profile")
            print("4. Logout")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == "1":
                self.manage_menu()
            elif choice == "2":
                self.view_ingredient_requests()
            elif choice == "3":
                self.update_user_profile(manager)
            elif choice == "4":
                break

    def manage_menu(self):
        while True:
            print("\n=== Menu Management ===")
            print("1. Add Item")
            print("2. Edit Item")
            print("3. Delete Item")
            print("4. View Menu")
            print("5. Back")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == "1":
                name = input("Enter item name: ")
                category = input("Enter category: ")
                price = float(input("Enter price: "))
                item_id = max(item.id for item in self.menu_items) + 1
                self.menu_items.append(MenuItem(item_id, name, category, price))
                print("Menu item added successfully!")
                
            elif choice == "2":
                self.view_menu()
                item_id = int(input("Enter item ID to edit: "))
                item = next((item for item in self.menu_items if item.id == item_id), None)
                if item:
                    item.name = input("Enter new name: ")
                    item.category = input("Enter new category: ")
                    item.price = float(input("Enter new price: "))
                    print("Menu item updated successfully!")
                else:
                    print("Invalid item ID!")
                    
            elif choice == "3":
                self.view_menu()
                item_id = int(input("Enter item ID to delete: "))
                self.menu_items = [item for item in self.menu_items if item.id != item_id]
                print("Menu item deleted successfully!")
                
            elif choice == "4":
                self.view_menu()
                
            elif choice == "5":
                break

    # Chef Functions
    def chef_menu(self, chef: User):
        while True:
            print(f"\n=== Chef Menu ({chef.name}) ===")
            print("1. View Orders")
            print("2. Update Order Status")
            print("3. Manage Ingredient Requests")
            print("4. Update Profile")
            print("5. Logout")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == "1":
                self.view_orders(chef)
            elif choice == "2":
                self.update_order_status(chef)
            elif choice == "3":
                self.manage_ingredient_requests(chef)
            elif choice == "4":
                self.update_user_profile(chef)
            elif choice == "5":
                break

    def view_orders(self, chef: User = None):
        print("\n=== Orders ===")
        for order in self.orders:
            if not chef or order.chef_id == chef.id:
                customer = next((u for u in self.users if u.id == order.customer_id), None)
                print(f"\nOrder ID: {order.id}")
                print(f"Customer: {customer.name if customer else 'Unknown'}")
                print(f"Status: {order.status.value}")
                print("Items:")
                for item_id, quantity in order.items:
                    item = next((i for i in self.menu_items if i.id == item_id), None)
                    if item:
                        print(f"- {item.name} x{quantity}")
                print(f"Total: ${order.total:.2f}")

    def update_order_status(self, chef: User):
        self.view_orders(chef)
        order_id = int(input("Enter order ID: "))
        order = next((o for o in self.orders if o.id == order_id), None)
        
        if order:
            print("1. Mark as In Progress")
            print("2. Mark as Completed")
            choice = input("Enter choice (1-2): ")
            
            if choice == "1":
                order.status = OrderStatus.IN_PROGRESS
            elif choice == "2":
                order.status = OrderStatus.COMPLETED
            print("Order status updated!")
        else:
            print("Invalid order ID!")

    # Customer Functions
    def customer_menu(self, customer: User):
        if customer.id not in self.customer_carts:
            self.customer_carts[customer.id] = {}
            
        while True:
            print(f"\n=== Customer Menu ({customer.name}) ===")
            print("1. View Menu & Order")
            print("2. View Orders")
            print("3. Send Feedback")
            print("4. Update Profile")
            print("5. Logout")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == "1":
                self.manage_customer_order(customer)
            elif choice == "2":
                self.view_customer_orders(customer)
            elif choice == "3":
                self.send_feedback(customer)
            elif choice == "4":
                self.update_user_profile(customer)
            elif choice == "5":
                break

    def manage_customer_order(self, customer: User):
        cart = self.customer_carts[customer.id]
        
        while True:
            print("\n=== Order Management ===")
            print("1. View Menu")
            print("2. Add to Cart")
            print("3. View Cart")
            print("4. Remove from Cart")
            print("5. Checkout")
            print("6. Back")
            
            choice = input("Enter your choice (1-6): ")
            
            if choice == "1":
                self.view_menu()
            elif choice == "2":
                self.view_menu()
                item_id = int(input("Enter item ID: "))
                quantity = int(input("Enter quantity: "))
                
                if item_id in [item.id for item in self.menu_items]:
                    cart[item_id] = cart.get(item_id, 0) + quantity
                    print("Item added to cart!")
                else:
                    print("Invalid item ID!")
            elif choice == "3":
                self.view_cart(customer)
            elif choice == "4":
                self.view_cart(customer)
                item_id = int(input("Enter item ID to remove: "))
                if item_id in cart:
                    del cart[item_id]
                    print("Item removed from cart!")
                else:
                    print("Item not in cart!")
            elif choice == "5":
                self.checkout(customer)
            elif choice == "6":
                break

    def view_menu(self):
        print("\n=== Menu ===")
        categories = set(item.category for item in self.menu_items)
        for category in categories:
            print(f"\n{category}:")
            for item in self.menu_items:
                if item.category == category:
                    print(f"[{item.id}] {item.name} - ${item.price:.2f}")

    def view_cart(self, customer: User):
        cart = self.customer_carts[customer.id]
        if not cart:
            print("Cart is empty!")
            return
            
        print("\n=== Your Cart ===")
        total = 0
        for item_id, quantity in cart.items():
            item = next((item for item in self.menu_items if item.id == item_id), None)
            if item:
                subtotal = item.price * quantity
                total += subtotal
                print(f"{item.name} x{quantity} - ${subtotal:.2f}")
        print(f"Total: ${total:.2f}")

        if not cart:
            print("Cart is empty!")
            return
            
        total = sum(
            next(item for item in self.menu_items if item.id == item_id).price * quantity
            for item_id, quantity in cart.items()
        )
        
        print(f"Total amount: ${total:.2f}")
        confirm = input("Enter 'pay' to confirm order: ")
        
        if confirm.lower() == 'pay':
            order_id = len(self.orders) + 1
            items = [(item_id, quantity) for item_id, quantity in cart.items()]
            
            new_order = Order(order_id, customer.id, items, total, OrderStatus.PENDING)
            self.orders.append(new_order)
            
            cart.clear()
            print("Order placed successfully!")
        else:
            print("Order cancelled!")

    def view_customer_orders(self, customer: User):
        print("\n=== Your Orders ===")
        customer_orders = [order for order in self.orders if order.customer_id == customer.id]
        
        if not customer_orders:
            print("No orders found!")
            return
            
        for order in customer_orders:
            print(f"\nOrder ID: {order.id}")
            print(f"Status: {order.status.value}")
            print("Items:")
            for item_id, quantity in order.items:
                item = next((i for i in self.menu_items if i.id == item_id), None)
                if item:
                    print(f"- {item.name} x{quantity}")
            print(f"Total: ${order.total:.2f}")

    def send_feedback(self, customer: User):
        message = input("Enter your feedback: ")
        if message.strip():
            feedback_id = len(self.feedbacks) + 1
            self.feedbacks.append(Feedback(feedback_id, customer.id, message))
            print("Feedback sent successfully!")
        else:
            print("Feedback cannot be empty!")

    def view_all_feedback(self):
        print("\n=== All Feedback ===")
        for feedback in self.feedbacks:
            customer = next((u for u in self.users if u.id == feedback.customer_id), None)
            print(f"\nFrom: {customer.name if customer else 'Unknown'}")
            print(f"Time: {feedback.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Message: {feedback.message}")

    def update_user_profile(self, user: User):
        print("\n=== Update Profile ===")
        user.username = input("Enter new username: ")
        user.password = input("Enter new password: ")
        user.name = input("Enter new name: ")
        print("Profile updated successfully!")

def main():
    system = RestaurantSystem()
    
    while True:
        user = system.login()
        if not user:
            break
            
        if user.role == UserRole.ADMIN:
            system.admin_menu(user)
        elif user.role == UserRole.MANAGER:
            system.manager_menu(user)
        elif user.role == UserRole.CHEF:
            system.chef_menu(user)
        elif user.role == UserRole.CUSTOMER:
            system.customer_menu(user)

if __name__ == "__main__":
    main()

class Staff:
    def __init__(self, id: int, name: str, role: str, salary: float):
        self.id = id
        self.name = name
        self.role = role
        self.salary = salary

class Sale:
    def __init__(self, id: int, chef_id: int, amount: float, date: str):
        self.id = id
        self.chef_id = chef_id
        self.amount = amount
        self.date = date

class Feedback:
    def __init__(self, id: int, customer_name: str, message: str, date: str):
        self.id = id
        self.customer_name = customer_name
        self.message = message
        self.date = date

class Admin:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.staff_list: List[Staff] = []
        self.sales_list: List[Sale] = []
        self.feedback_list: List[Feedback] = []
        self.load_data()

    def load_data(self):
        # Load staff data
        if os.path.exists('staff.json'):
            with open('staff.json', 'r') as f:
                staff_data = json.load(f)
                self.staff_list = [Staff(**s) for s in staff_data]

        # Load sales data
        if os.path.exists('sales.json'):
            with open('sales.json', 'r') as f:
                sales_data = json.load(f)
                self.sales_list = [Sale(**s) for s in sales_data]

        # Load feedback data
        if os.path.exists('feedback.json'):
            with open('feedback.json', 'r') as f:
                feedback_data = json.load(f)
                self.feedback_list = [Feedback(**f) for f in feedback_data]

    def save_data(self):
        # Save staff data
        with open('staff.json', 'w') as f:
            json.dump([vars(s) for s in self.staff_list], f)

        # Save sales data
        with open('sales.json', 'w') as f:
            json.dump([vars(s) for s in self.sales_list], f)

        # Save feedback data
        with open('feedback.json', 'w') as f:
            json.dump([vars(f) for f in self.feedback_list], f)

    def add_staff(self, name: str, role: str, salary: float):
        staff_id = len(self.staff_list) + 1
        new_staff = Staff(staff_id, name, role, salary)
        self.staff_list.append(new_staff)
        self.save_data()
        print(f"Staff {name} added successfully!")

    def edit_staff(self, staff_id: int, name: str, role: str, salary: float):
        for staff in self.staff_list:
            if staff.id == staff_id:
                staff.name = name
                staff.role = role
                staff.salary = salary
                self.save_data()
                print(f"Staff {name} updated successfully!")
                return
        print("Staff not found!")

    def delete_staff(self, staff_id: int):
        self.staff_list = [s for s in self.staff_list if s.id != staff_id]
        self.save_data()
        print("Staff deleted successfully!")

    def view_sales_report(self, month: int = None, chef_id: int = None):
        filtered_sales = self.sales_list

        if month:
            filtered_sales = [
                s for s in filtered_sales 
                if datetime.datetime.strptime(s.date, '%Y-%m-%d').month == month
            ]

        if chef_id:
            filtered_sales = [s for s in filtered_sales if s.chef_id == chef_id]

        total_sales = sum(s.amount for s in filtered_sales)
        print("\n=== Sales Report ===")
        print(f"Total Sales: ${total_sales:.2f}")
        for sale in filtered_sales:
            chef = next((s for s in self.staff_list if s.id == sale.chef_id), None)
            chef_name = chef.name if chef else "Unknown"
            print(f"Date: {sale.date}, Chef: {chef_name}, Amount: ${sale.amount:.2f}")

    def view_feedback(self):
        print("\n=== Customer Feedback ===")
        for feedback in self.feedback_list:
            print(f"\nFrom: {feedback.customer_name}")
            print(f"Date: {feedback.date}")
            print(f"Message: {feedback.message}")

    def update_profile(self, new_username: str, new_password: str):
        self.username = new_username
        self.password = new_password
        print("Profile updated successfully!")

def main():
    admin = Admin("admin", "admin123")
    
    while True:
        print("\n=== Administrator Menu ===")
        print("1. Manage Staff")
        print("2. View Sales Report")
        print("3. View Feedback")
        print("4. Update Profile")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            print("\n=== Staff Management ===")
            print("1. Add Staff")
            print("2. Edit Staff")
            print("3. Delete Staff")
            print("4. View Staff")
            
            staff_choice = input("Enter your choice (1-4): ")
            
            if staff_choice == "1":
                name = input("Enter staff name: ")
                role = input("Enter role (Manager/Chef): ")
                salary = float(input("Enter salary: "))
                admin.add_staff(name, role, salary)
            
            elif staff_choice == "2":
                staff_id = int(input("Enter staff ID: "))
                name = input("Enter new name: ")
                role = input("Enter new role (Manager/Chef): ")
                salary = float(input("Enter new salary: "))
                admin.edit_staff(staff_id, name, role, salary)
            
            elif staff_choice == "3":
                staff_id = int(input("Enter staff ID: "))
                admin.delete_staff(staff_id)
            
            elif staff_choice == "4":
                print("\n=== Staff List ===")
                for staff in admin.staff_list:
                    print(f"ID: {staff.id}, Name: {staff.name}, Role: {staff.role}, Salary: ${staff.salary:.2f}")
        
        elif choice == "2":
            month = input("Enter month (1-12) or press Enter for all: ")
            chef_id = input("Enter chef ID or press Enter for all: ")
            
            month = int(month) if month.strip() else None
            chef_id = int(chef_id) if chef_id.strip() else None
            
            admin.view_sales_report(month, chef_id)
        
        elif choice == "3":
            admin.view_feedback()
        
        elif choice == "4":
            new_username = input("Enter new username: ")
            new_password = input("Enter new password: ")
            admin.update_profile(new_username, new_password)
        
        elif choice == "5":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()

#MAnager
class Customer:
    def __init__(self, id: int, name: str, phone: str, email: str):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email

class MenuItem:
    def __init__(self, id: int, name: str, category: str, price: float):
        self.id = id
        self.name = name
        self.category = category
        self.price = price

class IngredientRequest:
    def __init__(self, id: int, chef_name: str, ingredients: list, status: str):
        self.id = id
        self.chef_name = chef_name
        self.ingredients = ingredients
        self.status = status

class Manager:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.customers = []
        self.menu_items = []
        self.ingredient_requests = []
        
        # Add some sample data
        self.add_sample_data()

    def add_sample_data(self):
        # Sample customers
        self.customers = [
            Customer(1, "John Doe", "1234567890", "john@email.com"),
            Customer(2, "Jane Smith", "9876543210", "jane@email.com")
        ]
        
        # Sample menu items
        self.menu_items = [
            MenuItem(1, "Margherita Pizza", "Pizza", 12.99),
            MenuItem(2, "Chicken Burger", "Burgers", 8.99)
        ]
        
        # Sample ingredient requests
        self.ingredient_requests = [
            IngredientRequest(1, "Chef Mike", ["Tomatoes", "Cheese", "Flour"], "Pending"),
            IngredientRequest(2, "Chef Sarah", ["Chicken", "Lettuce", "Buns"], "Approved")
        ]

    def manage_customers(self):
        while True:
            print("\n=== Customer Management ===")
            print("1. Add Customer")
            print("2. Edit Customer")
            print("3. Delete Customer")
            print("4. View All Customers")
            print("5. Back to Main Menu")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == "1":
                name = input("Enter customer name: ")
                phone = input("Enter phone number: ")
                email = input("Enter email: ")
                customer_id = len(self.customers) + 1
                self.customers.append(Customer(customer_id, name, phone, email))
                print("Customer added successfully!")
                
            elif choice == "2":
                customer_id = int(input("Enter customer ID to edit: "))
                for customer in self.customers:
                    if customer.id == customer_id:
                        customer.name = input("Enter new name: ")
                        customer.phone = input("Enter new phone: ")
                        customer.email = input("Enter new email: ")
                        print("Customer updated successfully!")
                        break
                else:
                    print("Customer not found!")
                    
            elif choice == "3":
                customer_id = int(input("Enter customer ID to delete: "))
                self.customers = [c for c in self.customers if c.id != customer_id]
                print("Customer deleted successfully!")
                
            elif choice == "4":
                print("\n=== Customer List ===")
                for customer in self.customers:
                    print(f"ID: {customer.id}, Name: {customer.name}")
                    print(f"Phone: {customer.phone}, Email: {customer.email}")
                    print("-" * 30)
                    
            elif choice == "5":
                break

    def manage_menu(self):
        while True:
            print("\n=== Menu Management ===")
            print("1. Add Menu Item")
            print("2. Edit Menu Item")
            print("3. Delete Menu Item")
            print("4. View Menu")
            print("5. Back to Main Menu")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == "1":
                name = input("Enter item name: ")
                category = input("Enter category: ")
                price = float(input("Enter price: "))
                item_id = len(self.menu_items) + 1
                self.menu_items.append(MenuItem(item_id, name, category, price))
                print("Menu item added successfully!")
                
            elif choice == "2":
                item_id = int(input("Enter item ID to edit: "))
                for item in self.menu_items:
                    if item.id == item_id:
                        item.name = input("Enter new name: ")
                        item.category = input("Enter new category: ")
                        item.price = float(input("Enter new price: "))
                        print("Menu item updated successfully!")
                        break
                else:
                    print("Menu item not found!")
                    
            elif choice == "3":
                item_id = int(input("Enter item ID to delete: "))
                self.menu_items = [i for i in self.menu_items if i.id != item_id]
                print("Menu item deleted successfully!")
                
            elif choice == "4":
                print("\n=== Menu List ===")
                categories = set(item.category for item in self.menu_items)
                for category in categories:
                    print(f"\n{category}:")
                    for item in self.menu_items:
                        if item.category == category:
                            print(f"ID: {item.id}, {item.name} - ${item.price:.2f}")
                    
            elif choice == "5":
                break

    def view_ingredient_requests(self):
        print("\n=== Ingredient Requests ===")
        for request in self.ingredient_requests:
            print(f"\nRequest ID: {request.id}")
            print(f"Chef: {request.chef_name}")
            print(f"Status: {request.status}")
            print("Ingredients:")
            for ingredient in request.ingredients:
                print(f"- {ingredient}")
            print("-" * 30)

    def update_profile(self):
        print("\n=== Update Profile ===")
        self.username = input("Enter new username: ")
        self.password = input("Enter new password: ")
        print("Profile updated successfully!")

def main():
    manager = Manager("manager", "manager123")
    
    while True:
        print("\n=== Manager Menu ===")
        print("1. Manage Customers")
        print("2. Manage Menu")
        print("3. View Ingredient Requests")
        print("4. Update Profile")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            manager.manage_customers()
        elif choice == "2":
            manager.manage_menu()
        elif choice == "3":
            manager.view_ingredient_requests()
        elif choice == "4":
            manager.update_profile()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
#chef
from datetime import datetime
from enum import Enum

class OrderStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

class Order:
    def __init__(self, id: int, customer_name: str, items: list, status: OrderStatus, timestamp: datetime):
        self.id = id
        self.customer_name = customer_name
        self.items = items  # List of tuples (item_name, quantity)
        self.status = status
        self.timestamp = timestamp

class IngredientRequest:
    def __init__(self, id: int, ingredients: list, notes: str, status: str):
        self.id = id
        self.ingredients = ingredients
        self.notes = notes
        self.status = status
        self.timestamp = datetime.now()

class Chef:
    def __init__(self, username: str, password: str, name: str):
        self.username = username
        self.password = password
        self.name = name
        self.orders = []
        self.ingredient_requests = []
        
        # Add sample data
        self.add_sample_data()

    def add_sample_data(self):
        # Sample orders
        self.orders = [
            Order(1, "John Doe", [("Margherita Pizza", 2), ("Garlic Bread", 1)], 
                 OrderStatus.PENDING, datetime.now()),
            Order(2, "Jane Smith", [("Chicken Burger", 1), ("Fries", 1)], 
                 OrderStatus.IN_PROGRESS, datetime.now())
        ]
        
        # Sample ingredient requests
        self.ingredient_requests = [
            IngredientRequest(1, ["Tomatoes", "Mozzarella"], "Running low on stock", "Pending"),
            IngredientRequest(2, ["Chicken", "Lettuce"], "Needed for tomorrow", "Approved")
        ]

    def view_orders(self):
        while True:
            print("\n=== Orders ===")
            print("1. View All Orders")
            print("2. View Pending Orders")
            print("3. View In-Progress Orders")
            print("4. View Completed Orders")
            print("5. Back to Main Menu")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == "5":
                break
                
            orders_to_show = self.orders
            if choice == "2":
                orders_to_show = [o for o in self.orders if o.status == OrderStatus.PENDING]
            elif choice == "3":
                orders_to_show = [o for o in self.orders if o.status == OrderStatus.IN_PROGRESS]
            elif choice == "4":
                orders_to_show = [o for o in self.orders if o.status == OrderStatus.COMPLETED]
                
            if not orders_to_show:
                print("No orders found!")
                continue
                
            print("\nOrder List:")
            for order in orders_to_show:
                print(f"\nOrder ID: {order.id}")
                print(f"Customer: {order.customer_name}")
                print(f"Status: {order.status.value}")
                print(f"Time: {order.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                print("Items:")
                for item, quantity in order.items:
                    print(f"- {item} x{quantity}")
                print("-" * 30)

    def update_order_status(self):
        print("\n=== Update Order Status ===")
        order_id = int(input("Enter order ID: "))
        
        order = next((o for o in self.orders if o.id == order_id), None)
        if not order:
            print("Order not found!")
            return
            
        print(f"\nCurrent Status: {order.status.value}")
        print("1. Mark as In Progress")
        print("2. Mark as Completed")
        
        choice = input("Enter your choice (1-2): ")
        if choice == "1":
            order.status = OrderStatus.IN_PROGRESS
            print("Order marked as In Progress!")
        elif choice == "2":
            order.status = OrderStatus.COMPLETED
            print("Order marked as Completed!")
        else:
            print("Invalid choice!")

    def manage_ingredient_requests(self):
        while True:
            print("\n=== Ingredient Requests ===")
            print("1. Add Request")
            print("2. Edit Request")
            print("3. Delete Request")
            print("4. View All Requests")
            print("5. Back to Main Menu")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == "1":
                print("\nNew Ingredient Request")
                ingredients = []
                while True:
                    ingredient = input("Enter ingredient (or press Enter to finish): ")
                    if not ingredient:
                        break
                    ingredients.append(ingredient)
                
                notes = input("Enter notes: ")
                request_id = len(self.ingredient_requests) + 1
                self.ingredient_requests.append(
                    IngredientRequest(request_id, ingredients, notes, "Pending")
                )
                print("Ingredient request added successfully!")
                
            elif choice == "2":
                request_id = int(input("Enter request ID to edit: "))
                request = next((r for r in self.ingredient_requests if r.id == request_id), None)
                if request:
                    print("Enter new ingredients (press Enter to finish):")
                    new_ingredients = []
                    while True:
                        ingredient = input("Enter ingredient: ")
                        if not ingredient:
                            break
                        new_ingredients.append(ingredient)
                    
                    request.ingredients = new_ingredients
                    request.notes = input("Enter new notes: ")
                    print("Request updated successfully!")
                else:
                    print("Request not found!")
                    
            elif choice == "3":
                request_id = int(input("Enter request ID to delete: "))
                self.ingredient_requests = [r for r in self.ingredient_requests if r.id != request_id]
                print("Request deleted successfully!")
                
            elif choice == "4":
                print("\nIngredient Requests:")
                for request in self.ingredient_requests:
                    print(f"\nRequest ID: {request.id}")
                    print(f"Status: {request.status}")
                    print(f"Time: {request.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                    print("Ingredients:")
                    for ingredient in request.ingredients:
                        print(f"- {ingredient}")
                    print(f"Notes: {request.notes}")
                    print("-" * 30)
                    
            elif choice == "5":
                break

    def update_profile(self):
        print("\n=== Update Profile ===")
        self.username = input("Enter new username: ")
        self.password = input("Enter new password: ")
        self.name = input("Enter new name: ")
        print("Profile updated successfully!")

def main():
    chef = Chef("chef1", "chef123", "Chef Gordon")
    
    while True:
        print(f"\n=== Chef Menu ({chef.name}) ===")
        print("1. View Orders")
        print("2. Update Order Status")
        print("3. Manage Ingredient Requests")
        print("4. Update Profile")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            chef.view_orders()
        elif choice == "2":
            chef.update_order_status()
        elif choice == "3":
            chef.manage_ingredient_requests()
        elif choice == "4":
            chef.update_profile()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
#customer
from datetime import datetime
from enum import Enum
from typing import List, Dict

class OrderStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

class MenuItem:
    def __init__(self, id: int, name: str, category: str, price: float):
        self.id = id
        self.name = name
        self.category = category
        self.price = price

class Order:
    def __init__(self, id: int, customer_id: int, items: List[tuple], total: float, status: OrderStatus):
        self.id = id
        self.customer_id = customer_id
        self.items = items  # List of tuples (item_id, quantity)
        self.total = total
        self.status = status
        self.timestamp = datetime.now()

class Feedback:
    def __init__(self, id: int, customer_id: int, message: str):
        self.id = id
        self.customer_id = customer_id
        self.message = message
        self.timestamp = datetime.now()

class Customer:
    def __init__(self, id: int, username: str, password: str, name: str, phone: str):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.phone = phone
        
        # Shopping cart to store temporary orders
        self.cart: Dict[int, int] = {}  # item_id: quantity
        
        # Initialize sample data
        self.menu_items = [
            MenuItem(1, "Margherita Pizza", "Pizza", 12.99),
            MenuItem(2, "Pepperoni Pizza", "Pizza", 14.99),
            MenuItem(3, "Chicken Burger", "Burgers", 8.99),
            MenuItem(4, "Veggie Burger", "Burgers", 7.99),
            MenuItem(5, "French Fries", "Sides", 3.99),
            MenuItem(6, "Coca Cola", "Beverages", 1.99)
        ]
        
        self.orders = []
        self.feedback_list = []

    def view_menu(self):
        print("\n=== Restaurant Menu ===")
        categories = set(item.category for item in self.menu_items)
        
        for category in categories:
            print(f"\n{category}:")
            category_items = [item for item in self.menu_items if item.category == category]
            for item in category_items:
                print(f"[{item.id}] {item.name} - ${item.price:.2f}")

    def manage_cart(self):
        while True:
            print("\n=== Shopping Cart ===")
            print("1. Add Item")
            print("2. Edit Quantity")
            print("3. Remove Item")
            print("4. View Cart")
            print("5. Clear Cart")
            print("6. Proceed to Checkout")
            print("7. Back to Main Menu")
            
            choice = input("Enter your choice (1-7): ")
            
            if choice == "1":
                self.view_menu()
                try:
                    item_id = int(input("\nEnter item ID to add: "))
                    quantity = int(input("Enter quantity: "))
                    
                    if item_id in [item.id for item in self.menu_items] and quantity > 0:
                        self.cart[item_id] = self.cart.get(item_id, 0) + quantity
                        print("Item added to cart!")
                    else:
                        print("Invalid item ID or quantity!")
                except ValueError:
                    print("Please enter valid numbers!")
                    
            elif choice == "2":
                self.view_cart()
                try:
                    item_id = int(input("\nEnter item ID to edit: "))
                    if item_id in self.cart:
                        quantity = int(input("Enter new quantity: "))
                        if quantity > 0:
                            self.cart[item_id] = quantity
                            print("Quantity updated!")
                        else:
                            del self.cart[item_id]
                            print("Item removed from cart!")
                    else:
                        print("Item not found in cart!")
                except ValueError:
                    print("Please enter valid numbers!")
                    
            elif choice == "3":
                self.view_cart()
                try:
                    item_id = int(input("\nEnter item ID to remove: "))
                    if item_id in self.cart:
                        del self.cart[item_id]
                        print("Item removed from cart!")
                    else:
                        print("Item not found in cart!")
                except ValueError:
                    print("Please enter valid numbers!")
                    
            elif choice == "4":
                self.view_cart()
                
            elif choice == "5":
                self.cart.clear()
                print("Cart cleared!")
                
            elif choice == "6":
                if self.cart:
                    self.checkout()
                else:
                    print("Cart is empty!")
                    
            elif choice == "7":
                break

    def view_cart(self):
        if not self.cart:
            print("\nYour cart is empty!")
            return
            
        print("\n=== Your Cart ===")
        total = 0
        for item_id, quantity in self.cart.items():
            item = next(item for item in self.menu_items if item.id == item_id)
            subtotal = item.price * quantity
            total += subtotal
            print(f"{item.name} x{quantity} - ${subtotal:.2f}")
        print(f"\nTotal: ${total:.2f}")

    def checkout(self):
        total = sum(
            next(item for item in self.menu_items if item.id == item_id).price * quantity
            for item_id, quantity in self.cart.items()
        )
        
        print(f"\nTotal amount to pay: ${total:.2f}")
        payment = input("Enter 'pay' to confirm payment: ")
        
        if payment.lower() == 'pay':
            order_id = len(self.orders) + 1
            items = [(item_id, quantity) for item_id, quantity in self.cart.items()]
            
            new_order = Order(order_id, self.id, items, total, OrderStatus.PENDING)
            self.orders.append(new_order)
            
            self.cart.clear()
            print("Order placed successfully!")
            print(f"Your order ID is: {order_id}")
        else:
            print("Payment cancelled!")

    def view_orders(self):
        if not self.orders:
            print("\nYou have no orders!")
            return
            
        print("\n=== Your Orders ===")
        for order in self.orders:
            print(f"\nOrder ID: {order.id}")
            print(f"Status: {order.status.value}")
            print(f"Time: {order.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print("Items:")
            for item_id, quantity in order.items:
                item = next(item for item in self.menu_items if item.id == item_id)
                print(f"- {item.name} x{quantity}")
            print(f"Total: ${order.total:.2f}")
            print("-" * 30)

    def send_feedback(self):
        print("\n=== Send Feedback ===")
        message = input("Enter your feedback message: ")
        
        if message.strip():
            feedback_id = len(self.feedback_list) + 1
            feedback = Feedback(feedback_id, self.id, message)
            self.feedback_list.append(feedback)
            print("Thank you for your feedback!")
        else:
            print("Feedback message cannot be empty!")

    def update_profile(self):
        print("\n=== Update Profile ===")
        self.username = input("Enter new username: ")
        self.password = input("Enter new password: ")
        self.name = input("Enter new name: ")
        self.phone = input("Enter new phone: ")
        print("Profile updated successfully!")

def main():
    # Create a sample customer
    customer = Customer(1, "customer1", "pass123", "John Doe", "1234567890")
    
    while True:
        print(f"\n=== Welcome, {customer.name}! ===")
        print("1. View Menu & Order Food")
        print("2. View Orders")
        print("3. Send Feedback")
        print("4. Update Profile")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            customer.manage_cart()
        elif choice == "2":
            customer.view_orders()
        elif choice == "3":
            customer.send_feedback()
        elif choice == "4":
            customer.update_profile()
        elif choice == "5":
            print("Thank you for visiting! Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()