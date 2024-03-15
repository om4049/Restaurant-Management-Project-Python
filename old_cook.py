import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

# Create the main window for the cook's interface
cook_root = tk.Tk()
cook_root.title("Cook's Interface")
cook_root.geometry("800x600")
cook_root.configure(bg="light gray")

# Define a custom font
custom_font = ("Helvetica", 14)

# Create a frame for the cook's interface
cook_frame = tk.Frame(cook_root, bg="light gray")
cook_frame.pack(fill="both", expand=True)

# Create a label for the cook's interface
cook_label = tk.Label(cook_frame, text="Cook's Interface", font=("Arial", 30, "bold"), bg="light gray")
cook_label.pack(pady=10)

# Create a table or list to display billing data
columns = ("Sr. No.", "Name", "Order Details")
bill_tree = ttk.Treeview(cook_frame, columns=columns, show="headings")

for col in columns:
    bill_tree.heading(col, text=col)
    bill_tree.column(col, width=150, anchor="center")

# Increase the row height to accommodate order details
style = ttk.Style()
style.configure("Treeview", rowheight=30)

bill_tree.pack(padx=20, pady=10, fill="both", expand=True)

# Function to retrieve and display billing data
def show_order_details(event):
    selected_item = bill_tree.selection()
    if selected_item:
        item = bill_tree.item(selected_item)
        order_details = item["values"][2]
        messagebox.showinfo("Order Details", order_details)

def update_cook_interface():
    # Update these database connection parameters with the correct values
    db_host = "127.0.0.1"  # Replace with the actual host
    db_user = "root"  # Replace with the actual user
    db_password = "ganesh"  # Replace with the actual password
    db_name = "restaurant"

    # Connect to the MySQL database
    db = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = db.cursor()

    # Query to retrieve billing data
    query = "SELECT * FROM bills"
    cursor.execute(query)
    data = cursor.fetchall()

    # Clear existing data in the table
    for row in bill_tree.get_children():
        bill_tree.delete(row)

    # Insert retrieved data into the table with Sr. No., Name, and Order Details columns
    for i, (_, customer_name, _, ordered_items, _, _) in enumerate(data, 1):
        truncated_details = ordered_items[:50] + ("..." if len(ordered_items) > 50 else "")
        bill_tree.insert("", "end", values=(i, customer_name, truncated_details))

    db.close()

# Create a button to update the cook's interface with billing data
update_button = tk.Button(cook_frame, text="Update Cook's Interface", command=update_cook_interface, font=custom_font)
update_button.pack(pady=10)

# Bind a double-click event to show the full order details
bill_tree.bind("<Double-1>", show_order_details)

# Update the cook's interface initially
update_cook_interface()

cook_root.mainloop()
