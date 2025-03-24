#MAIN
from datetime import datetime
from enum import Enum
from typing import List, Dict

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

#admin

class Admin:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.users = []
        self.orders = []
        self.feedbacks = []
        
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
                user_id = len(self.users) + 1
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

    def view_all_feedback(self):
        print("\n=== All Feedback ===")
        for feedback in self.feedbacks:
            customer = next((u for u in self.users if u.id == feedback.customer_id), None)
            print(f"\nFrom: {customer.name if customer else 'Unknown'}")
            print(f"Time: {feedback.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Message: {feedback.message}")

    def admin_menu(self):
        while True:
            print("\n=== Administrator Menu ===")
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
                new_username = input("Enter new username: ")
                new_password = input("Enter new password: ")
                self.update_profile(new_username, new_password)
            elif choice == "5":
                break

    def update_profile(self, new_username: str, new_password: str):
        self.username = new_username
        self.password = new_password
        print("Profile updated successfully!")
#manager


class Manager:
    def __init__(self, username: str, password: str, name: str):
        self.username = username
        self.password = password
        self.name = name
        self.menu_items = []
        self.ingredient_requests = []

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
                item_id = len(self.menu_items) + 1
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

    def view_menu(self):
        print("\n=== Menu List ===")
        categories = set(item.category for item in self.menu_items)
        for category in categories:
            print(f"\n{category}:")
            for item in self.menu_items:
                if item.category == category:
                    print(f"ID: {item.id}, {item.name} - ${item.price:.2f}")

    def view_ingredient_requests(self):
        print("\n=== Ingredient Requests ===")
        for request in self.ingredient_requests:
            print(f"\nRequest ID: {request.id}")
            print(f"Chef ID: {request.chef_id}")
            print(f"Status: {request.status}")
            print("Ingredients:")
            for ingredient in request.ingredients:
                print(f"- {ingredient}")
            print(f"Notes: {request.notes}")
            print("-" * 30)

    def process_ingredient_request(self):
        self.view_ingredient_requests()
        request_id = int(input("Enter request ID to process: "))
        request = next((r for r in self.ingredient_requests if r.id == request_id), None)
        
        if request:
            print("1. Approve")
            print("2. Reject")
            choice = input("Enter choice (1-2): ")
            
            if choice == "1":
                request.status = "Approved"
                print("Request approved!")
            elif choice == "2":
                request.status = "Rejected"
                print("Request rejected!")
        else:
            print("Invalid request ID!")

    def manager_menu(self):
        while True:
            print(f"\n=== Manager Menu ({self.name}) ===")
            print("1. Manage Menu")
            print("2. View Ingredient Requests")
            print("3. Process Ingredient Request")
            print("4. Update Profile")
            print("5. Logout")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == "1":
                self.manage_menu()
            elif choice == "2":
                self.view_ingredient_requests()
            elif choice == "3":
                self.process_ingredient_request()
            elif choice == "4":
                self.update_profile()
            elif choice == "5":
                break

    def update_profile(self):
        print("\n=== Update Profile ===")
        self.username = input("Enter new username: ")
        self.password = input("Enter new password: ")
        self.name = input("Enter new name: ")
        print("Profile updated successfully!")
# chef

class Chef:
    def __init__(self, username: str, password: str, name: str):
        self.username = username
        self.password = password
        self.name = name
        self.orders = []
        self.ingredient_requests = []

    def view_orders(self):
        while True:
            print("\n=== Orders ===")
            print("1. View All Orders")
            print("2. View Pending Orders")
            print("3. View In-Progress Orders")
            print("4. View Completed Orders")
            print("5. Back")
            
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
                print(f"Status: {order.status.value}")
                print(f"Time: {order.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                print("Items:")
                for item_id, quantity in order.items:
                    print(f"- Item ID: {item_id} x{quantity}")
                print("-" * 30)

    def update_order_status(self):
        print("\n=== Update Order Status ===")
        self.view_orders()
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
            print("1. Create Request")
            print("2. View My Requests")
            print("3. Back")
            
            choice = input("Enter your choice (1-3): ")
            
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
                    IngredientRequest(request_id, id, ingredients, notes, "Pending")
                )
                print("Ingredient request created successfully!")
                
            elif choice == "2":
                print("\nMy Ingredient Requests:")
                for request in self.ingredient_requests:
                    print(f"\nRequest ID: {request.id}")
                    print(f"Status: {request.status}")
                    print(f"Time: {request.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                    print("Ingredients:")
                    for ingredient in request.ingredients:
                        print(f"- {ingredient}")
                    print(f"Notes: {request.notes}")
                    print("-" * 30)
                    
            elif choice == "3":
                break

    def chef_menu(self):
        while True:
            print(f"\n=== Chef Menu ({self.name}) ===")
            print("1. View Orders")
            print("2. Update Order Status")
            print("3. Manage Ingredient Requests")
            print("4. Update Profile")
            print("5. Logout")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == "1":
                self.view_orders()
            elif choice == "2":
                self.update_order_status()
            elif choice == "3":
                self.manage_ingredient_requests()
            elif choice == "4":
                self.update_profile()
            elif choice == "5":
                break

    def update_profile(self):
        print("\n=== Update Profile ===")
        self.username = input("Enter new username: ")
        self.password = input("Enter new password: ")
        self.name = input("Enter new name: ")
        print("Profile updated successfully!")
#CUSTOMER


class Customer:
    def __init__(self, username: str, password: str, name: str):
        self.username = username
        self.password = password
        self.name = name
        self.orders = []
        self.cart = {}  # Dictionary to store cart items {item_id: quantity}

    def view_menu(self, menu_items):
        print("\n=== Menu ===")
        categories = set(item.category for item in menu_items)
        for category in categories:
            print(f"\n{category}:")
            for item in menu_items:
                if item.category == category:
                    print(f"[{item.id}] {item.name} - ${item.price:.2f}")

    def manage_cart(self, menu_items):
        while True:
            print("\n=== Cart Management ===")
            print("1. Add to Cart")
            print("2. View Cart")
            print("3. Remove from Cart")
            print("4. Checkout")
            print("5. Back")
            
            choice = input("Enter your choice (1-5): ")
            
            if choice == "1":
                self.view_menu(menu_items)
                item_id = int(input("Enter item ID: "))
                quantity = int(input("Enter quantity: "))
                
                if item_id in [item.id for item in menu_items]:
                    self.cart[item_id] = self.cart.get(item_id, 0) + quantity
                    print("Item added to cart!")
                else:
                    print("Invalid item ID!")
                    
            elif choice == "2":
                self.view_cart(menu_items)
                
            elif choice == "3":
                self.view_cart(menu_items)
                item_id = int(input("Enter item ID to remove: "))
                if item_id in self.cart:
                    del self.cart[item_id]
                    print("Item removed from cart!")
                else:
                    print("Item not in cart!")
                    
            elif choice == "4":
                self.checkout(menu_items)
                
            elif choice == "5":
                break

    def view_cart(self, menu_items):
        if not self.cart:
            print("Cart is empty!")
            return
            
        print("\n=== Your Cart ===")
        total = 0
        for item_id, quantity in self.cart.items():
            item = next((item for item in menu_items if item.id == item_id), None)
            if item:
                subtotal = item.price * quantity
                total += subtotal
                print(f"{item.name} x{quantity} - ${subtotal:.2f}")
        print(f"Total: ${total:.2f}")

    def checkout(self, menu_items):
        if not self.cart:
            print("Cart is empty!")
            return
            
        total = sum(
            next(item for item in menu_items if item.id == item_id).price * quantity
            for item_id, quantity in self.cart.items()
        )
        
        print(f"\nTotal amount: ${total:.2f}")
        confirm = input("Enter 'pay' to confirm order: ")
        
        if confirm.lower() == 'pay':
            order_id = len(self.orders) + 1
            items = [(item_id, quantity) for item_id, quantity in self.cart.items()]
            
            new_order = Order(order_id, id, items, total, OrderStatus.PENDING)
            self.orders.append(new_order)
            
            self.cart.clear()
            print("Order placed successfully!")
        else:
            print("Order cancelled!")

    def view_orders(self):
        if not self.orders:
            print("No orders found!")
            return
            
        print("\n=== Your Orders ===")
        for order in self.orders:
            print(f"\nOrder ID: {order.id}")
            print(f"Status: {order.status.value}")
            print(f"Time: {order.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print("Items:")
            for item_id, quantity in order.items:
                print(f"- Item ID: {item_id} x{quantity}")
            print(f"Total: ${order.total:.2f}")
            print("-" * 30)

    def send_feedback(self, feedbacks):
        message = input("Enter your feedback: ")
        if message.strip():
            feedback_id = len(feedbacks) + 1
            feedbacks.append(Feedback(feedback_id, id, message))
            print("Feedback sent successfully!")
        else:
            print("Feedback cannot be empty!")

    def customer_menu(self, menu_items, feedbacks):
        while True:
            print(f"\n=== Customer Menu ({self.name}) ===")
            print("1. View Menu")
            print("2. Manage Cart")
            print("3. View Orders")
            print("4. Send Feedback")
            print("5. Update Profile")
            print("6. Logout")
            
            choice = input("Enter your choice (1-6): ")
            
            if choice == "1":
                self.view_menu(menu_items)
            elif choice == "2":
                self.manage_cart(menu_items)
            elif choice == "3":
                self.view_orders()
            elif choice == "4":
                self.send_feedback(feedbacks)
            elif choice == "5":
                self.update_profile()
            elif choice == "6":
                break

    def update_profile(self):
        print("\n=== Update Profile ===")
        self.username = input("Enter new username: ")
        self.password = input("Enter new password: ")
        self.name = input("Enter new name: ")
        print("Profile updated successfully!")
#main


class RestaurantSystem:
    def __init__(self):
        self.users = []
        self.menu_items = []
        self.orders = []
        self.feedbacks = []
        self.ingredient_requests = []
        
        # Initialize with default admin account
        self.initialize_admin()

    def initialize_admin(self):
        admin = User(1, "admin", "admin123", UserRole.ADMIN, "Administrator")
        self.users.append(admin)

    def register_user(self):
        print("\n=== User Registration ===")
        username = input("Enter username: ")
        password = input("Enter password: ")
        name = input("Enter name: ")
        
        # Check if username already exists
        if any(user.username == username for user in self.users):
            print("Username already exists!")
            return None

        print("\nSelect Role:")
        print("1. Customer")
        print("2. Chef")
        print("3. Manager")
        role_choice = input("Choose role (1-3): ")

        if role_choice == "1":
            role = UserRole.CUSTOMER
        elif role_choice == "2":
            role = UserRole.CHEF
        elif role_choice == "3":
            role = UserRole.MANAGER
        else:
            print("Invalid role choice!")
            return None

        user_id = max(user.id for user in self.users) + 1
        new_user = User(user_id, username, password, role, name)
        self.users.append(new_user)
        print("Registration successful!")
        return new_user

    def login(self):
        print("\n=== Login ===")
        username = input("Enter username: ")
        password = input("Enter password: ")

        user = next((u for u in self.users if u.username == username and u.password == password), None)
        if user:
            print(f"Welcome back, {user.name}!")
            return user
        else:
            print("Invalid credentials!")
            return None

    def run(self):
        while True:
            print("\n=== Restaurant Management System ===")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            
            choice = input("Choose an option: ")
            
            if choice == "1":
                self.register_user()
                
            elif choice == "2":
                user = self.login()
                if user:
                    if user.role == UserRole.ADMIN:
                        admin = Admin(user.username, user.password)
                        admin.users = self.users
                        admin.orders = self.orders
                        admin.feedbacks = self.feedbacks
                        admin.admin_menu()
                        
                    elif user.role == UserRole.MANAGER:
                        manager = Manager(user.username, user.password, user.name)
                        manager.menu_items = self.menu_items
                        manager.ingredient_requests = self.ingredient_requests
                        manager.manager_menu()
                        
                    elif user.role == UserRole.CHEF:
                        chef = Chef(user.username, user.password, user.name)
                        chef.orders = self.orders
                        chef.ingredient_requests = self.ingredient_requests
                        chef.chef_menu()
                        
                    elif user.role == UserRole.CUSTOMER:
                        customer = Customer(user.username, user.password, user.name)
                        customer.orders = [order for order in self.orders if order.customer_id == user.id]
                        customer.customer_menu(self.menu_items, self.feedbacks)
                        
            elif choice == "3":
                print("Thank you for using the Restaurant Management System!")
                break
                
            else:
                print("Invalid choice! Please try again.")

if __name__ == "__main__":
    system = RestaurantSystem()
    system.run()