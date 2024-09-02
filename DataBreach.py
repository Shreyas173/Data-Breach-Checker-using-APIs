import tkinter as tk
from tkinter import messagebox
import requests
import hashlib

# Function to check password
def check_password():
    password = entry.get()
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password.")
        return

    hashed_password = hashlib.sha1(password.encode()).hexdigest()
    password_prefix = hashed_password[:5]
    password_suffix = hashed_password[5:].upper()

    url = f"https://api.pwnedpasswords.com/range/{password_prefix}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Error making request: {e}")
        return

    breached_dict = {}
    breached_list = response.text.splitlines()

    for breached_password in breached_list:
        breached_hash = breached_password.split(":")
        if len(breached_hash) == 2:
            breached_dict[breached_hash[0]] = breached_hash[1]

    if password_suffix in breached_dict:
        messagebox.showinfo("Result", f"Password has been compromised {breached_dict[password_suffix]} times.")
    else:
        messagebox.showinfo("Result", "Password has never been compromised and is safe to use.")

# Create the main window
root = tk.Tk()
root.title("Password Checker")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size and position it in the center
window_width = 400
window_height = 200
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create a label
label = tk.Label(root, text="Enter your password:")
label.pack(pady=10)

# Create an entry widget
entry = tk.Entry(root, show='*', width=40)
entry.pack(pady=5)

# Create a button to check the password
button = tk.Button(root, text="Check Password", command=check_password)
button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
