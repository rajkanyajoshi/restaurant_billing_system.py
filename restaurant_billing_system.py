import tkinter as tk
from tkinter import messagebox
import os                    

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Billing System")
        self.root.geometry("800x800")
        self.root.configure(bg="#e6f7ff")

        self.customer_name = tk.StringVar()
        self.customer_mobile = tk.StringVar()
        self.items = {
            "Pizza": 120,
            "Burger": 80,
            "Pasta": 100,
            "Fries": 60,
            "Coke": 40,
            "Salad": 50,
            "Ice Cream": 70
        }
        self.item_vars = {}
        self.quantity_vars = {}

        self.bill_folder = "bills"
        if not os.path.exists(self.bill_folder):
            os.makedirs(self.bill_folder)

        self.create_widgets()

    def create_widgets(self):
        # Header
        tk.Label(self.root, text="Billing System", font=("Helvetica", 20, "bold"), bg="#e6f7ff", fg="#003366").pack(pady=10)

        # Customer Details
        frame = tk.Frame(self.root, bg="#e6f7ff")
        frame.pack(pady=10)
        tk.Label(frame, text="Customer Name:", font=("Arial", 12), bg="#e6f7ff", fg="#003366").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(frame, textvariable=self.customer_name, font=("Arial", 12), width=30).grid(row=0, column=1, padx=10, pady=10)
        tk.Label(frame, text="Mobile Number:", font=("Arial", 12), bg="#e6f7ff", fg="#003366").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(frame, textvariable=self.customer_mobile, font=("Arial", 12), width=30).grid(row=1, column=1, padx=10, pady=10)

        # Item Selection Header
        tk.Label(self.root, text="Select Items, Prices, and Quantities:", font=("Arial", 14, "bold"), bg="#e6f7ff", fg="#003366").pack(pady=10)
        items_frame = tk.Frame(self.root, bg="#e6f7ff")
        items_frame.pack()
        for idx, (item, price) in enumerate(self.items.items()):
            var = tk.IntVar()
            qty_var = tk.IntVar(value=0)
            self.item_vars[item] = var
            self.quantity_vars[item] = qty_var
            tk.Checkbutton(items_frame, text=f"{item}", variable=var, font=("Arial", 12), bg="#e6f7ff", fg="#003366", onvalue=1, offvalue=0).grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            tk.Label(items_frame, text=f"Price: {price}", font=("Arial", 12), bg="#e6f7ff", fg="#003366").grid(row=idx, column=1, padx=5)
            tk.Label(items_frame, text="Qty:", font=("Arial", 12), bg="#e6f7ff", fg="#003366").grid(row=idx, column=2, padx=5)
            tk.Entry(items_frame, textvariable=qty_var, font=("Arial", 12), width=5).grid(row=idx, column=3, padx=5)

        # Buttons
        buttons_frame = tk.Frame(self.root, bg="#e6f7ff")
        buttons_frame.pack(pady=10)
        tk.Button(buttons_frame, text="Generate Bill", command=self.generate_bill, font=("Arial", 12), bg="#99ccff", fg="#003366", width=15).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(buttons_frame, text="Clear", command=self.clear, font=("Arial", 12), bg="#99ccff", fg="#003366", width=15).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(buttons_frame, text="Search Bill", command=self.search_bill, font=("Arial", 12), bg="#99ccff", fg="#003366", width=15).grid(row=0, column=2, padx=10, pady=10)
        tk.Button(buttons_frame, text="Exit", command=self.exit_app, font=("Arial", 12), bg="#ff6666", fg="#ffffff", width=15).grid(row=0, column=3, padx=10, pady=10)

        # Bill Display
        tk.Label(self.root, text="Bill Details:", font=("Arial", 14), bg="#e6f7ff", fg="#003366").pack(pady=10)
        self.bill_text = tk.Text(self.root, width=70, height=20, bg="#f4f4f4", fg="#333", font=("Arial", 12))
        self.bill_text.pack(pady=10)

    def generate_bill(self):
        customer = self.customer_name.get()
        mobile = self.customer_mobile.get()
        if not customer and not mobile:
            messagebox.showerror("Error", "Either Customer name or mobile number is required.")
            return

        selected_items = {}
        for item, var in self.item_vars.items():
            if var.get() == 1:
                quantity = self.quantity_vars[item].get()
                if quantity > 0:
                    selected_items[item] = (self.items[item], quantity)

        if not selected_items:
            messagebox.showerror("Error", "Please select at least one item with a valid quantity.")
            return

        total = sum(price * qty for price, qty in selected_items.values())
        bill_content = f"Customer Name: {customer if customer else 'N/A'}\n"
        bill_content += f"Mobile Number: {mobile if mobile else 'N/A'}\n"
        bill_content += "\n"
        bill_content += "Item                 Price     Quantity   Total\n"
        bill_content += "-" * 50 + "\n"
        
        for item, (price, qty) in selected_items.items():
            total_item = price * qty
            bill_content += f"{item:<20} {price:<10} {qty:<10} {total_item:<10}\n"

        bill_content += "-" * 50 + "\n"
        bill_content += f"Total Amount: {total}\n"
        bill_content += "\nThank you for visiting! Please come again."

        # Save the bill
        bill_file = os.path.join(self.bill_folder, f"{customer if customer else 'Unknown'}_{mobile if mobile else 'Unknown'}.txt")
        with open(bill_file, "w") as file:
            file.write(bill_content)

        self.bill_text.delete(1.0, tk.END)
        self.bill_text.insert(tk.END, bill_content)
        messagebox.showinfo("Success", f"Bill generated and saved as {os.path.basename(bill_file)}")

    def clear(self):
        self.customer_name.set("")
        self.customer_mobile.set("")
        for var in self.item_vars.values():
            var.set(0)
        for qty_var in self.quantity_vars.values():
            qty_var.set(0)
        self.bill_text.delete(1.0, tk.END)

    def search_bill(self):
        customer = self.customer_name.get()
        mobile = self.customer_mobile.get()
        if not customer and not mobile:
            messagebox.showerror("Error", "Please provide either Customer name or mobile number to search.")
            return

        bill_file = os.path.join(self.bill_folder, f"{customer if customer else 'Unknown'}_{mobile if mobile else 'Unknown'}.txt")
        if os.path.exists(bill_file):
            with open(bill_file, "r") as file:
                content = file.read()
            self.bill_text.delete(1.0, tk.END)
            self.bill_text.insert(tk.END, content)
        else:
            messagebox.showerror("Error", f"No bill found for {customer if customer else 'N/A'} with mobile number {mobile if mobile else 'N/A'}.")

    def exit_app(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BillingApp(root)
    root.mainloop()
