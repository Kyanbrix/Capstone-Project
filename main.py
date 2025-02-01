import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.dialogs import Messagebox
import connection


def change_frame_content():
    stocks()
    for widget in target_frame.winfo_children():  # Clear existing widgets in the frame
        widget.destroy()

    # Add new content to the target frame
    search.place(x=880, y=80)

    search_btn = ttk.Button(target_frame, text="Search", command=searchBtn, width=10)
    search_btn.place(x=600, y=60)

    con = connection.ConnectionPool()
    cursor = con.connect()
    cursor.execute("SELECT * FROM items")

    data = cursor.fetchall()
    con.close()

    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 14), rowheight=30)
    style.configure("Treeview.Heading", font=("Arial", 16, "bold"))

    table = ttk.Treeview(target_frame, style="Treeview", columns=["Item ID", "Item Name"], show="headings", height=20,
                         padding=20)
    table.heading("Item ID", text="ITEM ID")
    table.heading("Item Name", text="ITEM NAME")
    table.column("Item ID", width=100, anchor=CENTER)
    table.column("Item Name", width=100, anchor=CENTER)
    table.pack(fill=BOTH, expand=YES, padx=50, pady=100)

    for row in data:
        table.insert("", "end", values=row)


def searchBtn():
    if search.get() == '':
        Messagebox.show_error(title="No Input!", alert=True, message='No Item ID Specified', parent=target_frame, )
        return

    search.place(x=880, y=80)

    con = connection.ConnectionPool()
    cursor = con.connect()
    cursor.execute(f"SELECT * FROM items WHERE item_id = {search.get()}")

    data = cursor.fetchall()

    con.close()

    rows = len(data)

    if rows == 0:
        Messagebox.show_error(alert=True, parent=target_frame, message='ID not Found!')
        return

    for widget in target_frame.winfo_children():  # Clear existing widgets in the frame
        widget.destroy()

    search_btn = ttk.Button(target_frame, text="Search", command=searchBtn, width=10)
    search_btn.place(x=600, y=60)

    table = ttk.Treeview(target_frame, style="Treeview", columns=["Item ID", "Item Name"], show="headings", height=20,
                         padding=20)
    table.heading("Item ID", text="ITEM ID")
    table.heading("Item Name", text="ITEM NAME")
    table.column("Item ID", width=100, anchor=CENTER)
    table.column("Item Name", width=100, anchor=CENTER)
    table.pack(fill=BOTH, expand=YES, padx=50, pady=100)

    for row in data:
        table.insert("", "end", values=row)


def stocks():
    stock_dictionary = {}
    con = connection.ConnectionPool()
    cursor = con.connect()
    cursor.execute("SELECT item_name FROM items")
    data = cursor.fetchall()
    con.close()
    for row in data:
        if row[0] in stock_dictionary:
            stock_dictionary[row[0]] = stock_dictionary.get(row[0]) + 1
        else:
            stock_dictionary[row[0]] = 1

    print(stock_dictionary)


def reset_frame_content():
    for widget in target_frame.winfo_children():
        widget.destroy()


def refreshBtn():
    for widget in target_frame.winfo_children():  # Clear existing widgets in the frame
        widget.destroy()

    back_button = ttk.Button(target_frame, text="Refresh", command=refreshBtn)
    back_button.pack(pady=10, padx=10)

    con = connection.ConnectionPool()
    cursor = con.connect()
    cursor.execute("SELECT * FROM items")
    data = cursor.fetchall()
    con.close()

    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 14), rowheight=30)
    style.configure("Treeview.Heading", font=("Arial", 16, "bold"))

    table = ttk.Treeview(target_frame, style="Treeview", columns=["Item ID", "Item Name"], show="headings", height=20,
                         padding=20)
    table.heading("Item ID", text="ITEM ID")
    table.heading("Item Name", text="ITEM NAME")
    table.column("Item ID", width=100, anchor=CENTER)
    table.column("Item Name", width=100, anchor=CENTER)
    table.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    for row in data:
        table.insert("", "end", values=row)


root = ttk.Window(themename="solar", title="Dynamic Frame Content", size=(1100, 600))

control_frame = ttk.Frame(root, padding=10, borderwidth=2, relief="ridge")
control_frame.pack(side=LEFT, fill=Y)

target_frame = ttk.Frame(root, padding=10, borderwidth=2, relief="ridge")
target_frame.pack(side=RIGHT, fill=BOTH, expand=YES, padx=10, pady=10)

control_label = ttk.Label(control_frame, text="Menu", font=("Arial", 14))
control_label.pack(pady=10)
change_button = ttk.Button(control_frame, text="Check Items", command=change_frame_content, width=12)
change_button.pack(pady=50, padx=20)

original_label = ttk.Label(target_frame, text="This is the original frame content", font=("Arial", 14))
original_label.pack(pady=20)

search = ttk.Entry(width=15, font=('arial', 12, 'bold'))

root.mainloop()
