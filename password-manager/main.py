import tkinter as tk
from tkinter import messagebox
import random
import pyperclip
import json
CadetBlue = "#9898F5"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    #Password Generator Project
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_list += [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_list += [random.choice(numbers) for _ in range(random.randint(2, 4))]

    random.shuffle(password_list)

    password = "".join(password_list)
    # password = ""
    # for char in password_list:
    #     password += char

    password_entry.insert(0, password)
    pyperclip.copy(text=password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please do not leave any fields empty!")
    else:
        # with open(file="passwords.txt", mode="a") as file:
        #     file.write(f"{website} | {email} | {password}\n")
        #     website_entry.delete(0, "end")
        #     password_entry.delete(0, "end")
        try:
            with open("data.json", "r") as data_file:
                #Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            #Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                #Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, "end")
            password_entry.delete(0, "end")


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(message="No data file found.")

    else:
        if website in data:
            messagebox.showinfo(title=website, message=f"Email: {data[website]['email']}\n"
                                                       f"Password: {data[website]['password']}")
        else:
            messagebox.showwarning(message=f"No details for the {website} exits.")


# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.title("Password Manager")
window.config(bg="white", padx=50, pady=50)

#canvas
canvas = tk.Canvas(width=200, height=200, bg="white", highlightthickness=0)
password_image = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=password_image)
canvas.grid(column=1, row=0)

#labels
website_label = tk.Label(text="Website:", bg="white", fg="black")
website_label.grid(column=0, row=1)
email_label = tk.Label(text="Email/Username:", bg="white", fg="black")
email_label.grid(column=0, row=2)
password_label = tk.Label(text="Password:", bg="white", fg="black")
password_label.grid(column=0, row=3)

#Entries
website_entry = tk.Entry(width=20, bg="white", fg="black", highlightthickness=1,
                         highlightcolor=CadetBlue, highlightbackground="white")
website_entry.grid(column=1, row=1, sticky="EW")
website_entry.focus()
email_entry = tk.Entry(width=38, bg="white", fg="black", highlightthickness=1,
                       highlightcolor=CadetBlue, highlightbackground="white")
email_entry.grid(column=1, row=2, sticky="WE", columnspan=2)
email_entry.insert(0, "@email.com")
password_entry = tk.Entry(width=20, bg="white", fg="black", highlightthickness=1,
                          highlightcolor=CadetBlue, highlightbackground="white")
password_entry.grid(column=1, row=3, sticky="EW")

#Buttons
search_button = tk.Button(text="Search", highlightbackground="white", command=find_password)
search_button.grid(column=2, row=1, sticky="WE")
generate_password_button = tk.Button(text="Generate Password", highlightbackground="white", command=generate_password)
generate_password_button.grid(column=2, row=3, sticky="we")
add_button = tk.Button(text="Add", width=36, highlightbackground="white", command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
