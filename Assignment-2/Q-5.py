import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import re


# ---------------- DATABASE ----------------

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Sm@2/11/2006",
    "database": "College"
}


def connect_db():
    return mysql.connector.connect(**DB_CONFIG)


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Contact (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL UNIQUE,
            phone VARCHAR(20),
            category VARCHAR(30),
            notes TEXT,
            INDEX idx_name (name),
            INDEX idx_email (email),
            INDEX idx_phone (phone)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


# ---------------- VALIDATION ----------------

def valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email) is not None


# ---------------- DATABASE OPERATIONS ----------------

def add_contact():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    category = category_var.get()
    notes = notes_text.get("1.0", tk.END).strip()

    if not name or not email:
        messagebox.showerror("Error", "Name and email are required.")
        return

    if not valid_email(email):
        messagebox.showerror("Error", "Invalid email address.")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Contact
            (name, email, phone, category, notes)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, phone, category, notes))

        conn.commit()

        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Record inserted.")
        clear_fields()
        load_contacts()

    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Email already exists.")

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))


def update_contact():
    selected = contact_list.selection()

    if not selected:
        messagebox.showerror("Error", "Select a contact first.")
        return

    contact_id = contact_list.item(selected[0])["values"][0]

    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    category = category_var.get()
    notes = notes_text.get("1.0", tk.END).strip()

    if not name or not email:
        messagebox.showerror("Error", "Name and email are required.")
        return

    if not valid_email(email):
        messagebox.showerror("Error", "Invalid email address.")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Contact
            SET name=%s, email=%s, phone=%s,
                category=%s, notes=%s
            WHERE id=%s
        """, (name, email, phone, category, notes, contact_id))

        conn.commit()

        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Record updated.")
        clear_fields()
        load_contacts()

    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Email already exists.")

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))


def delete_contact():
    selected = contact_list.selection()

    if not selected:
        messagebox.showerror("Error", "Select a contact first.")
        return

    contact_id = contact_list.item(selected[0])["values"][0]

    if not messagebox.askyesno("Confirm", "Delete this contact?"):
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM Contact WHERE id=%s",
            (contact_id,)
        )

        conn.commit()

        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Record deleted.")
        clear_fields()
        load_contacts()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))


# ---------------- SEARCH ----------------

def search_contacts():
    keyword = search_entry.get().strip()

    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = """
            SELECT id, name, email, phone, category, notes
            FROM Contact
            WHERE name LIKE %s
               OR email LIKE %s
               OR phone LIKE %s
            ORDER BY name ASC
        """

        value = "%" + keyword + "%"

        cursor.execute(query, (value, value, value))

        display_results(cursor.fetchall())

        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))


def load_contacts():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, email, phone, category, notes
            FROM Contact
            ORDER BY name ASC
        """)

        display_results(cursor.fetchall())

        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))


def display_results(rows):
    for item in contact_list.get_children():
        contact_list.delete(item)

    for row in rows:
        contact_list.insert("", tk.END, values=row)


# ---------------- GUI HELPERS ----------------

def select_contact(event):
    selected = contact_list.selection()

    if not selected:
        return

    values = contact_list.item(selected[0])["values"]

    clear_fields()

    name_entry.insert(0, values[1])
    email_entry.insert(0, values[2])
    phone_entry.insert(0, values[3] or "")
    category_var.set(values[4] or "")
    notes_text.insert("1.0", values[5] or "")


def clear_fields():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)

    category_var.set("Friend")

    notes_text.delete("1.0", tk.END)

    for item in contact_list.selection():
        contact_list.selection_remove(item)


# ---------------- GUI ----------------

root = tk.Tk()
root.title("MySQL Contact Manager")
root.geometry("1000x650")


# Name
tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=5)

name_entry = tk.Entry(root, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)


# Email
tk.Label(root, text="Email").grid(row=1, column=0, padx=10, pady=5)

email_entry = tk.Entry(root, width=30)
email_entry.grid(row=1, column=1, padx=10, pady=5)


# Phone
tk.Label(root, text="Phone").grid(row=2, column=0, padx=10, pady=5)

phone_entry = tk.Entry(root, width=30)
phone_entry.grid(row=2, column=1, padx=10, pady=5)


# Category - Combobox
tk.Label(root, text="Category").grid(row=3, column=0, padx=10, pady=5)

category_var = tk.StringVar(value="Friend")

category_box = ttk.Combobox(
    root,
    textvariable=category_var,
    values=["Friend", "Faculty", "Student", "Family", "Work"],
    state="readonly"
)

category_box.grid(row=3, column=1, padx=10, pady=5)


# Notes - Text
tk.Label(root, text="Notes").grid(row=4, column=0, padx=10, pady=5)

notes_text = tk.Text(root, width=30, height=5)
notes_text.grid(row=4, column=1, padx=10, pady=5)


# Buttons
tk.Button(
    root,
    text="Add",
    command=add_contact
).grid(row=5, column=0, pady=10)

tk.Button(
    root,
    text="Update",
    command=update_contact
).grid(row=5, column=1, pady=10)

tk.Button(
    root,
    text="Delete",
    command=delete_contact
).grid(row=5, column=2, pady=10)


# Search
tk.Label(root, text="Search").grid(row=6, column=0, padx=10)

search_entry = tk.Entry(root, width=30)
search_entry.grid(row=6, column=1)

tk.Button(
    root,
    text="Search",
    command=search_contacts
).grid(row=6, column=2)

tk.Button(
    root,
    text="Show All",
    command=load_contacts
).grid(row=6, column=3)


# Listbox/Treeview
columns = (
    "ID",
    "Name",
    "Email",
    "Phone",
    "Category",
    "Notes"
)

contact_list = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

for column in columns:
    contact_list.heading(column, text=column)
    contact_list.column(column, width=140)

contact_list.grid(
    row=7,
    column=0,
    columnspan=4,
    padx=10,
    pady=20
)

contact_list.bind(
    "<Double-1>",
    select_contact
)


# ---------------- START ----------------

try:
    create_table()
    load_contacts()
    root.mainloop()

except mysql.connector.Error as e:
    messagebox.showerror("Database Error", str(e))