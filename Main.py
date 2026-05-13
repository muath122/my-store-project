import datetime

# --- CLASS DEFINITIONS ---

class Product:
    def __init__(self, ID, name, price, stock):
        self.ID = ID
        self.name = name
        self.price = float(price)
        self.stock = int(stock)

    def update_stock(self, quantity):
        """Reduces the available stock when a purchase is made."""
        self.stock -= quantity

# إضافة كلاس الـ Bundle (مطلوب في المستوى المتقدم)
class Bundle(Product):
    def __init__(self, ID, name, component_ids, stock, all_products):
        super().__init__(ID, name, 0, stock)
        self.component_ids = component_ids
        # حساب السعر تلقائياً (خصم 20% من مجموع المكونات)
        total = 0
        for p_id in component_ids:
            for p in all_products:
                if p.ID.lower() == p_id.lower():
                    total += p.price
        self.price = total * 0.8

class Customer:
    def __init__(self, ID, name, value=0.0):
        self.ID = ID
        self.name = name
        self.value = float(value) # لحفظ إجمالي المشتريات

    def get_discount(self, total_price):
        """Standard customers receive 0% discount."""
        return 0, total_price

class Member(Customer):
    def __init__(self, ID, name, value=0.0):
        super().__init__(ID, name, value)

    def get_discount(self, total_price):
        """Members receive a fixed 5% discount."""
        rate = 0.05
        return rate, total_price * (1 - rate)

# إضافة كلاس الـ VIP (المطلوب لمنطق الـ Threshold)
class VIPMember(Customer):
    threshold = 1000.0 # هذه هي العتبة التي سألت عنها
    def __init__(self, ID, name, value=0.0):
        super().__init__(ID, name, value)

    def get_discount(self, total_price):
        # إذا تجاوز السعر الـ Threshold يأخذ 15% وإلا 10%
        rate = 0.15 if total_price > VIPMember.threshold else 0.10
        return rate, total_price * (1 - rate)

# --- Call the products and the customers ---

def load_products():
    products = []
    try:
        with open("products.txt", "r") as file:
            lines = file.readlines()
            # تحميل المنتجات العادية أولاً
            for line in lines:
                data = line.strip().split(",")
                if data[0].lower().startswith('p'):
                    products.append(Product(data[0], data[1], data[2], data[3]))
            # تحميل الـ Bundles
            for line in lines:
                data = line.strip().split(",")
                if data[0].lower().startswith('b'):
                    products.append(Bundle(data[0], data[1], data[2:-1], data[-1], products))
    except FileNotFoundError:
        print("System Error: products.txt not found!")
    return products

def load_customers():
    customers = []
    try:
        with open("customers.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) >= 3:
                    c_id, c_name, c_type = data[0], data[1], data[2].strip().upper()
                    c_val = float(data[3]) if len(data) > 3 else 0.0
                    
                    if "VIP" in c_type:
                        customers.append(VIPMember(c_id, c_name, c_val))
                    elif "MEMBER" in c_type:
                        customers.append(Member(c_id, c_name, c_val))
                    else:
                        customers.append(Customer(c_id, c_name, c_val))
    except FileNotFoundError:
        print("System Error: customers.txt not found!")
    return customers

all_products = load_products()
all_customers = load_customers()

# --- SALES LOGIC (Place Order) ---

def place_order():
    print("\nNEW ORDER PROCESS")
    c_name = input("Enter Customer Name: ").strip()
    customer = next((c for c in all_customers if c.name.lower() == c_name.lower()), None)
    
    if not customer:
        print("Result: Customer not found.")
        return

    p_name = input("Enter Product/Bundle Name: ").strip()
    product = next((p for p in all_products if p.name.lower() == p_name.lower() or p.ID.lower() == p_name.lower()), None)
    
    if not product:
        print("Result: Product not found.")
        return

    try:
        qty = int(input(f"Enter quantity (Stock: {product.stock}): "))
        if qty <= 0 or qty > product.stock:
            print("Error: Invalid quantity.")
            return
    except ValueError:
        print("Error: Please enter a number.")
        return

    # الحسابات باستخدام منطق الخصم الجديد
    subtotal = product.price * qty
    rate, final_price = customer.get_discount(subtotal)

    product.update_stock(qty)
    customer.value += final_price # تحديث إجمالي ما صرفه العميل

    # الاوتبوت المرتب (نفس تنسيقك)
    print("\n" + "="*35)
    print("         SALES RECEIPT")
    print(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*35)
    print(f"Customer Name : {customer.name} ({type(customer).__name__})")
    print(f"Product Item  : {product.name} (x{qty})")
    print(f"Subtotal      : {subtotal:.2f} SAR")
    print(f"Discount ({rate*100}%): {(subtotal*rate):.2f} SAR")
    print("-" * 35)
    print(f"FINAL TOTAL   : {final_price:.2f} SAR")
    print("="*35)
    print("Order completed successfully!")

# --- SYSTEM INTERFACE (Main Menu) ---

def main_menu():
    while True:
        print("\nWelcome to our electronic store")
        print("1. View All Products")
        print("2. View All Customers")
        print("3. Place a New Order")
        print("4. Adjust VIP Threshold")
        print("0. Exit System")
        
        choice = input("Action (0-4): ")

        if choice == '1':
            print("\nID\tName\t\tPrice\tStock")
            print("-" * 45)
            for p in all_products:
                print(f"{p.ID}\t{p.name:10}\t{p.price:.2f}\t{p.stock}")

        elif choice == '2':
            print("\nID\tName\t\tType\t\tTotal Spent")
            print("-" * 55)
            for c in all_customers:
                role = type(c).__name__
                print(f"{c.ID}\t{c.name:10}\t{role:12}\t{c.value:.2f} SAR")

        elif choice == '3':
            place_order()

        elif choice == '4':
            try:
                new_val = float(input(f"Current Threshold is {VIPMember.threshold}. Enter new value: "))
                VIPMember.threshold = new_val
                print(f"Threshold updated to {new_val} SAR")
            except ValueError:
                print("Invalid input.")

        elif choice == '0':
            print("Closing system... Have a great day!")
            break
        else:
            print("Error: Invalid selection.")

all_products = load_products()
all_customers = load_customers()

if __name__ == "__main__":
    main_menu()