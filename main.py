import sqlite3
import tkinter
from tkinter import ttk, END
from tkinter.tix import Tk

connection = sqlite3.connect('marvel1.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
                    id INTEGER PRIMARY KEY,
                    movie TEXT,
                    date TEXT,
                    mcu_phase TEXT
                )''')
connection.commit()


with open('Marvel.txt', 'r') as file:
    lines = file.readlines()
    for line in lines[1:]:
        data = line.split()
        movie_id = int(data[0])
        movie = data[1]
        date = data[2]
        mcu_phase = data[3]
        cursor.execute("INSERT INTO movies VALUES (?, ?, ?, ?)", (movie_id, movie, date, mcu_phase))
    connection.commit()


def add_button_clicked():
    popup = tkinter.Toplevel()
    popup.title("Add Movie")

    def add_to_database():
        new_id = int(new_id_entry.get())
        new_movie = new_movie_entry.get()
        new_date = new_date_entry.get()
        new_phase = new_phase_entry.get()
        cursor.execute("INSERT INTO movies VALUES (?, ?, ?, ?)", (new_id, new_movie, new_date, new_phase))
        connection.commit()
        popup.destroy()

    new_id_label = ttk.Label(popup, text="ID:")
    new_id_label.pack()
    new_id_entry = ttk.Entry(popup)
    new_id_entry.pack()

    new_movie_label = ttk.Label(popup, text="Movie:")
    new_movie_label.pack()
    new_movie_entry = ttk.Entry(popup)
    new_movie_entry.pack()

    new_date_label = ttk.Label(popup, text="Date:")
    new_date_label.pack()
    new_date_entry = ttk.Entry(popup)
    new_date_entry.pack()

    new_phase_label = ttk.Label(popup, text="Phase:")
    new_phase_label.pack()
    new_phase_entry = ttk.Entry(popup)
    new_phase_entry.pack()

    ok_button = ttk.Button(popup, text="Ok", command=add_to_database)
    ok_button.pack(side=ttk.LEFT)

    cancel_button = ttk.Button(popup, text="Cancel", command=popup.destroy)
    cancel_button.pack(side=ttk.LEFT)


def list_all_button_clicked():
    cursor.execute("SELECT * FROM movies")
    data = cursor.fetchall()
    text_box.delete(1.0, END)
    for row in data:
        text_box.insert(END, f"ID: {row[0]}, Movie: {row[1]}, Date: {row[2]}, MCU Phase: {row[3]}\n")


root = Tk()
root.title("Marvel Movies")
root.geometry("400x300")

add_button = ttk.Button(root, text="Add", command=add_button_clicked)
add_button.pack(pady=10)

list_all_button = ttk.Button(root, text="LIST ALL", command=list_all_button_clicked)
list_all_button.pack(pady=10)

id_list = [row[0] for row in cursor.execute("SELECT id FROM movies")]
dropdown_var = tkinter.StringVar()
dropdown = tkinter.OptionMenu(root, dropdown_var, *id_list)
dropdown.pack()

text_box = tkinter.Text(root, height=10, width=50)
text_box.pack()

root.mainloop()


