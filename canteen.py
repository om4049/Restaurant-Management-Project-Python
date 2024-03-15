import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import pymysql

# Create the main window
root = tk.Tk()
root.title("CANTEEN")
root.geometry("1000x800")
root.configure(bg="deep sky blue")

# Define a custom font
custom_font = ("Helvetica", 14)

# Create a frame for the header with the same background color
header_frame = tk.Frame(root, bg="deep sky blue")
header_frame.pack(fill="x")

# Create a label for the window title with white text
title_label = tk.Label(header_frame, text="CANTEEN", font=("Arial", 30, "bold"), bg="deep sky blue", fg="white")
title_label.pack(side="top", padx=10)

# Create a black line as an underline to the header
line = tk.Frame(header_frame, height=2, bg="black")
line.pack(fill="x", side="top")

# Create the main content area with the same background
content_frame = tk.Frame(root, bg="deep sky blue")
content_frame.pack(fill="both", expand=True)

# Create a white-colored rounded rectangle on the left side for the menu
menu_frame = tk.Frame(content_frame, bg="white")
menu_frame.place(relx=0.01, rely=0.05, relwidth=0.25, relheight=0.9)

# Create a label for the menu
menu_label = tk.Label(menu_frame, text="MENU", font=("custom_font", 30, "bold"), bg="white", fg="brown")
menu_label.pack(pady=10)

# Create a list of menu items with their prices
menu_items = [
    ("Veg Thali", 80),
    ("Dal Bhat", 150),
    ("Mutton Thali", 250),
    ("Anda Thali", 120),
    ("Veg Biryani", 100),
    ("medu vada", 150),
    ("Dosa", 50),
    ("Idli-sambar", 40),
    ("Pohe", 25),
    ("Water Bottle", 20)
]

# Create a dictionary to track selected items and their quantities
selected_items = {}

def add_item(item, price, label):
    if item in selected_items:
        selected_items[item]["quantity"] += 1
    else:
        selected_items[item] = {"price": price, "quantity": 1}
    update_bill()
    label.config(text=f"{item} {price}/- Added")

def remove_item(item, price, label):
    if item in selected_items and selected_items[item]["quantity"] > 1:
        selected_items[item]["quantity"] -= 1
    else:
        del selected_items[item]
    update_bill()
    label.config(text=f"{item} {price}/- Removed")

for item, price in menu_items:
    item_frame = tk.Frame(menu_frame, bg="white")
    item_frame.pack(fill="x")

    item_label = tk.Label(item_frame, text=f"{item} {price}/-", font=custom_font, bg="white")
    item_label.pack(side="left", padx=10, pady=5, expand=True)

    button_frame = tk.Frame(item_frame, bg="white")
    button_frame.pack(side="right")

    add_button = tk.Button(button_frame, text="+", width=2, height=1, relief="solid", bg="green", font=custom_font)
    add_button.grid(row=0, column=0)
    
    remove_button = tk.Button(button_frame, text="-", width=2, height=1, relief="solid", bg="red", font=custom_font)
    remove_button.grid(row=0, column=1)

    add_button.config(command=lambda item=item, price=price, label=item_label: add_item(item, price, label))
    remove_button.config(command=lambda item=item, price=price, label=item_label: remove_item(item, price, label))

# Create a white-colored rectangle on the right side for billing
bill_frame = tk.Frame(content_frame, bg="white")
bill_frame.place(relx=0.28, rely=0.05, relwidth=0.7, relheight=0.9)

# Create a label for the billing header
bill_header = tk.Label(bill_frame, text="Bill", font=("Arial", 30, "bold"), bg="white", fg="brown")
bill_header.pack(pady=10)

# Create a label for the welcome message
welcome_label = tk.Label(bill_frame, text="Welcome to ADYPSOE CANTEEN", font=custom_font, bg="white")
welcome_label.pack()

# Create a label for the date and time
datetime_label = tk.Label(bill_frame, text=f"Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", font=custom_font, bg="white")
datetime_label.pack()

# Create a frame for student details
student_details_frame = tk.Frame(bill_frame, bg="white")
student_details_frame.pack(fill="x")

# Create labels for student name, PRN no, and Department
student_name_label = tk.Label(student_details_frame, text="Student Name:", font=custom_font, bg="white")
student_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

student_name_entry = tk.Entry(student_details_frame)
student_name_entry.grid(row=0, column=1, padx=10, pady=5)

prn_no_label = tk.Label(student_details_frame, text="PRN No:", font=custom_font, bg="white")
prn_no_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

prn_no_entry = tk.Entry(student_details_frame)
prn_no_entry.grid(row=1, column=1, padx=10, pady=5)

department_label = tk.Label(student_details_frame, text="Department:", font=custom_font, bg="white")
department_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

department_entry = tk.Entry(student_details_frame)
department_entry.grid(row=2, column=1, padx=10, pady=5)

# Create a Checkbutton to mark bill as paid or not paid
bill_paid_var = tk.IntVar()
bill_paid_checkbox = tk.Checkbutton(student_details_frame, text="Bill Paid", variable=bill_paid_var, font=custom_font, bg="white")
bill_paid_checkbox.grid(row=3, column=0, padx=10, pady=5, sticky="w")

# Create a separator
separator = tk.Frame(bill_frame, height=2, bg="black")
separator.pack(fill="x")

# Create a label for the billing items
billing_items_label = tk.Label(bill_frame, text="items               quantity               price", font=custom_font, bg="white")
billing_items_label.pack(pady=10)

# Create a frame for billing items with a scrollbar
billing_items_frame = tk.Frame(bill_frame, bg="white")
billing_items_frame.pack()

scrollbar = ttk.Scrollbar(billing_items_frame, orient="vertical")
scrollbar.grid(row=0, column=1, sticky="ns")

billing_items_canvas = tk.Canvas(billing_items_frame, bg="white", yscrollcommand=scrollbar.set)
billing_items_canvas.grid(row=0, column=0, sticky="nsew")

scrollbar.config(command=billing_items_canvas.yview)

billing_items_inner_frame = tk.Frame(billing_items_canvas, bg="white")
billing_items_canvas.create_window((0, 0), window=billing_items_inner_frame, anchor="nw")

billing_items_inner_frame.bind("<Configure>", lambda event, canvas=billing_items_canvas: on_frame_configure(billing_items_canvas))

def on_frame_configure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Function to update the bill
def update_bill():
    for widget in billing_items_inner_frame.winfo_children():
        widget.destroy()

    total_price = 0

    for i, (item, details) in enumerate(selected_items.items()):
        item_label = tk.Label(billing_items_inner_frame, text=item, font=custom_font, bg="white")
        item_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        quantity_label = tk.Label(billing_items_inner_frame, text=details["quantity"], font=custom_font, bg="white")
        quantity_label.grid(row=i, column=1, padx=10, pady=5)

        price_label = tk.Label(billing_items_inner_frame, text=f"{details['price']}/-", font=custom_font, bg="white")
        price_label.grid(row=i, column=2, padx=10, pady=5)

        total_price += details['price'] * details['quantity']

    total_label = tk.Label(billing_items_inner_frame, text=f"Total: {total_price}/-", font=custom_font, bg="white")
    total_label.grid(row=len(selected_items), column=0, columnspan=3, padx=10, pady=5)

# Function to store the billing data in MySQL
def store_billing_data():
    db_host = "127.0.0.1"
    db_user = "root"
    db_password = "ganesh"
    db_name = "canteen"

    # Connect to the database
    db = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = db.cursor()

    student_name = student_name_entry.get()
    prn_no = prn_no_entry.get()
    department = department_entry.get()
    ordered_items = "\n".join([f"{item}: {details['quantity']} @ {details['price']} each" for item, details in selected_items.items()])
    total_amount = sum(details['quantity'] * details['price'] for details in selected_items.values())
    order_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    bill_paid = "Paid" if bill_paid_var.get() == 1 else "Not Paid"

    insert_query = "INSERT INTO bills (student_name, prn_no, department, ordered_items, total_amount, order_datetime, bill_paid) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    data = (student_name, prn_no, department, ordered_items, total_amount, order_datetime, bill_paid)
    cursor.execute(insert_query, data)
    db.commit()

    db.close()

    messagebox.showinfo("Data Stored", "Billing data has been successfully stored in the database")

# Create a button to store the billing data
store_data_button = tk.Button(bill_frame, text="Generate Bill", command=store_billing_data, bg="deep sky blue", font=custom_font)
store_data_button.pack(pady=10)

# Create a separator2
separator2 = tk.Frame(bill_frame, height=2, bg="black")
separator2.pack(fill="x")

# Create a label for the thank you message
thank_you_label = tk.Label(bill_frame, text="Thank you visit again!!BY GANESH", font=custom_font, bg="white")
thank_you_label.pack()

# developed by Ganesh Bodakhe
root.mainloop()
