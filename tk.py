import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Connect to MySQL Database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Add your MySQL password if set
    database="musical_store"
)
cursor = conn.cursor()

# Create Table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        customer_name VARCHAR(255),
        phone_number VARCHAR(20),
        email VARCHAR(255),
        instruments VARCHAR(255),
        quantity INT,
        discount FLOAT,
        order_date DATE,
        delivery_date DATE,
        payment_method VARCHAR(50),
        payment_status VARCHAR(50)
    )
''')
conn.commit()




# GUI Application
root = tk.Tk()
root.title("Musical Instrument Store")
root.geometry("500x700")

font_style = ("Arial", 12)

# Labels & Entry Fields
tk.Label(root, text="Customer Name:", font=font_style).grid(row=0, column=0, sticky="w")
customer_name_entry = tk.Entry(root)
customer_name_entry.grid(row=0, column=1)

tk.Label(root, text="Phone Number:", font=font_style).grid(row=1, column=0, sticky="w")
phone_entry = tk.Entry(root)
phone_entry.grid(row=1, column=1)

tk.Label(root, text="Email:", font=font_style).grid(row=2, column=0, sticky="w")
email_entry = tk.Entry(root)
email_entry.grid(row=2, column=1)

# Instrument Selection
instrument_vars = {}
instruments = {"Veena": 50000, "Tabla": 30000, "Sitar": 71000, "Mridangam": 65000, "Flute": 15000}











tk.Label(root, text="Select Instrument:", font=font_style).grid(row=3, column=0, sticky="w")
row_index = 4
for instr, price in instruments.items():
    var = tk.IntVar()
    instrument_vars[instr] = var
    tk.Checkbutton(root, text=f"{instr} - ₹{price}", variable=var, font=font_style).grid(row=row_index, column=0, sticky="w")
    row_index += 1

# Quantity & Discount
tk.Label(root, text="Quantity:", font=font_style).grid(row=row_index, column=0, sticky="w")
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=row_index, column=1)
row_index += 1

tk.Label(root, text="Discount (%):", font=font_style).grid(row=row_index, column=0, sticky="w")
discount_entry = tk.Entry(root)
discount_entry.grid(row=row_index, column=1)
row_index += 1

# Order & Delivery Date
tk.Label(root, text="Order Date (YYYY-MM-DD):", font=font_style).grid(row=row_index, column=0, sticky="w")
order_date_entry = tk.Entry(root)
order_date_entry.grid(row=row_index, column=1)
row_index += 1







tk.Label(root, text="Delivery Date (YYYY-MM-DD):", font=font_style).grid(row=row_index, column=0, sticky="w")
delivery_date_entry = tk.Entry(root)
delivery_date_entry.grid(row=row_index, column=1)
row_index += 1

# Payment Method
tk.Label(root, text="Payment Method:", font=font_style).grid(row=row_index, column=0, sticky="w")
payment_method_var = ttk.Combobox(root, values=["Cash", "Card", "Online"])
payment_method_var.grid(row=row_index, column=1)
row_index += 1

# Payment Status
tk.Label(root, text="Payment Status:", font=font_style).grid(row=row_index, column=0, sticky="w")
payment_status_var = ttk.Combobox(root, values=["Pending", "Paid"])
payment_status_var.grid(row=row_index, column=1)
row_index += 1

# Bill Section
tk.Label(root, text="Bill:", font=font_style).grid(row=row_index, column=0, sticky="w")
bill_label = tk.Label(root, text="₹0.00", font=font_style)
bill_label.grid(row=row_index, column=1, sticky="w")
row_index += 1










# Database Operations
def add_order():
    selected_instruments = [instr for instr, var in instrument_vars.items() if var.get() == 1]
    if not selected_instruments:
        messagebox.showwarning("Warning", "Please select at least one instrument.")
        return

    cursor.execute("INSERT INTO orders (customer_name, phone_number, email, instruments, quantity, discount, order_date, delivery_date, payment_method, payment_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (customer_name_entry.get(), phone_entry.get(), email_entry.get(), ", ".join(selected_instruments),
                    quantity_entry.get(), discount_entry.get(), order_date_entry.get(), delivery_date_entry.get(),
                    payment_method_var.get(), payment_status_var.get()))
    conn.commit()
    messagebox.showinfo("Success", "Order placed successfully!")

def display_orders():
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()














    # Print header
    print("\n{:<3} | {:<15} | {:<12} | {:<25} | {:<20} | {:<3} | {:<8} | {:<12} | {:<12} | {:<10} | {:<8}".format(
        "ID", "Customer", "Phone", "Email", "Instruments", "Qty", "Discount", "Order Date", "Delivery Date", "Payment", "Status"
    ))
    print("-" * 140)

    # Print each order
    for order in orders:
        order = list(order)
        order[7] = str(order[7])  # Convert order_date to string
        order[8] = str(order[8])  # Convert delivery_date to string
        print("{:<3} | {:<15} | {:<12} | {:<25} | {:<20} | {:<3} | {:<8} | {:<12} | {:<12} | {:<10} | {:<8}".format(*order))

def update_order():
    cursor.execute("UPDATE orders SET payment_status='Paid' WHERE phone_number=%s", (phone_entry.get(),))
    conn.commit()
    messagebox.showinfo("Success", "Payment Status Updated!")

def delete_order():
    cursor.execute("DELETE FROM orders WHERE phone_number=%s", (phone_entry.get(),))
    conn.commit()
    messagebox.showinfo("Success", "Order Deleted!")








def clear_all_orders():
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete all orders?")
    if confirm:
        cursor.execute("DELETE FROM orders")
        conn.commit()
        messagebox.showinfo("Success", "All orders deleted successfully!")

# Calculate Bill
def calculate_bill():
    selected_instruments = [instr for instr, var in instrument_vars.items() if var.get() == 1]
    quantity = int(quantity_entry.get()) if quantity_entry.get() else 1
    discount = float(discount_entry.get()) if discount_entry.get() else 0

    # Calculate total price of selected instruments
    total_price = sum(instruments[instr] for instr in selected_instruments) * quantity

    # Apply discount
    total_price_after_discount = total_price - (total_price * (discount / 100))

    # Update the bill label
    bill_label.config(text=f"₹{total_price_after_discount:.2f}")











# Buttons
tk.Button(root, text="Place Order", command=add_order, font=font_style).grid(row=row_index, column=0, pady=10, padx=5)
tk.Button(root, text="View Orders", command=display_orders, font=font_style).grid(row=row_index, column=1, pady=10, padx=5)
row_index += 1

tk.Button(root, text="Update Order", command=update_order, font=font_style).grid(row=row_index, column=0, pady=10, padx=5)
tk.Button(root, text="Delete Order", command=delete_order, font=font_style).grid(row=row_index, column=1, pady=10, padx=5)
row_index += 1

tk.Button(root, text="Clear All Orders", command=clear_all_orders, font=font_style, bg="red", fg="white").grid(row=row_index, column=0, columnspan=2, pady=10, sticky="ew")
row_index += 1

tk.Button(root, text="Calculate Bill", command=calculate_bill, font=font_style).grid(row=row_index, column=0, columnspan=2, pady=10, sticky="ew")

# Close MySQL connection on exit
def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
