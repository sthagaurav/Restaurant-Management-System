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