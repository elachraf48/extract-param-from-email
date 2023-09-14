import tkinter as tk
from tkinter import ttk
import json
import imaplib
import datetime  # Add this import for time-based search

root = tk.Tk()
root.title("Email Search Tool")

# Calculate the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y coordinates for the center of the screen
x = (screen_width - root.winfo_reqwidth()) / 2
y = (screen_height - root.winfo_reqheight()) / 2

# Set the initial size and position of the window
root.geometry(f'+{int(x)}+{int(y)}')

import os

# Initialize data.json with an empty JSON array if it doesn't exist
if not os.path.exists("data.json"):
    with open("data.json", "w") as json_file:
        json_file.write("[]")
# Function to add a new email and password
def add_new_email():
    # Calculate the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the x and y coordinates for the center of the screen
    x = (screen_width - root.winfo_reqwidth()) / 2
    y = (screen_height - root.winfo_reqheight()) / 2

    # Set the initial size and position of the root window
    root.geometry(f'+{int(x)}+{int(y)}')

    # Create a new window for adding email
    add_email_window = tk.Toplevel(root)
    add_email_window.title("Add New Email")

    # Get the width of the root window
    root_width = root.winfo_width()

    # Set the width of the add_email_window to be the same as the root window
    add_email_window.geometry(f'{root_width}x300')  # Adjust the height as needed

    # Calculate the x and y coordinates for the center of the screen
    x = (screen_width - add_email_window.winfo_reqwidth()) / 2
    y = (screen_height - add_email_window.winfo_reqheight()) / 2

    # Set the position of the add_email_window to the center
    add_email_window.geometry(f'+{int(x)}+{int(y)}')






    # Label and input field for 'Email'
    email_label = ttk.Label(add_email_window, text="Email:")
    email_label.pack()

    email_entry = ttk.Entry(add_email_window)
    email_entry.pack()

    # Label and input field for 'Password'
    password_label = ttk.Label(add_email_window, text="Password:")
    password_label.pack()

    password_entry = ttk.Entry(add_email_window, show="*")  # Show asterisks for password input
    password_entry.pack()

    # Button to save the email and password
    def save_email():
        email = email_entry.get()
        password = password_entry.get()
        if email and password:
            # Read existing data from data.json (if it exists)
            existing_data = []

            try:
                with open("data.json", "r") as json_file:
                    existing_data = json.load(json_file)
            except (FileNotFoundError, json.JSONDecodeError):
                pass  # If the file doesn't exist or is empty

            # Add the new email and password to the existing data
            new_entry = {"email": email, "password": password}
            existing_data.append(new_entry)

            # Save the updated data to data.json
            with open("data.json", "w") as json_file:
                json.dump(existing_data, json_file, indent=4)

            # Update the email dropdown menu
            email_var.set("")  # Clear the selection
            update_email_dropdown()

            add_email_window.destroy()


    save_button = ttk.Button(add_email_window, text="Save", command=save_email)
    save_button.pack()


# Function to update the email dropdown with email addresses
def update_email_dropdown():
    try:
        with open("data.json", "r") as json_file:
            email_data = json.load(json_file)
            emails = [entry["email"] for entry in email_data]
            email_dropdown["values"] = emails
    except FileNotFoundError:
        pass  # Handle file not found gracefully
    except json.JSONDecodeError:
        pass  # Handle JSON decode error gracefully





# Label for 'Email'
email_label = ttk.Label(root, text="Email:")
email_label.pack()

# Dropdown for selecting email
email_var = tk.StringVar()
email_dropdown = ttk.Combobox(root, textvariable=email_var)
email_dropdown.pack()

# Button for 'Add New Email'
add_email_button = ttk.Button(root, text="Add New Email", command=add_new_email)
add_email_button.pack()

# Label for 'Select Search By'
search_label = ttk.Label(root, text="Select Search By:")
search_label.pack()

# Dropdown list for 'Subject', 'From', 'Last 1h'
search_var = tk.StringVar()
search_dropdown = ttk.Combobox(root, textvariable=search_var, values=["Subject", "From", "all"])
search_dropdown.pack()

# Entry widget for entering search text
search_entry = ttk.Entry(root)
search_entry.pack()

# Function to handle changes in the dropdown
def handle_dropdown_change(event):
    selected_option = search_var.get()
    if selected_option == "all":
        search_entry.delete(0, "end")  # Clear
        search_entry.configure(state="disabled")

    else:
        search_entry.configure(state="normal")

# Bind the function to the dropdown's <<ComboboxSelected>> event
search_dropdown.bind("<<ComboboxSelected>>", handle_dropdown_change)

def fetch_email_counts():
    email = email_var.get()
    if not email:
        return  # No email selected

    # Get the email and password from the data.json file
    try:
        with open("data.json", "r") as json_file:
            email_data = json.load(json_file)
            for entry in email_data:
                if entry["email"] == email:
                    password = entry["password"]
                    break
            else:
                return  # Email not found in data.json
    except (FileNotFoundError, json.JSONDecodeError):
        return  # File not found or JSON decode error

    # Connect to the IMAP server
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    # Log in to the email account
    try:
        imap.login(email, password)
    except imaplib.IMAP4.error:
        text_area.delete(1.0, tk.END)  # Clear previous results
        text_area.insert(tk.END, "Invalid email or password.")
        return

    # Fetch the counts of emails based on the selected search option
    search_option = search_var.get()
    search_text = search_entry.get()
    time_value = time_entry.get()

        # Construct the criteria based on the selected search option
    # Construct the criteria based on the selected search option
    if search_option == "all":
        # Search for emails received within the specified time (e.g., 10 minutes)
        time_threshold = (datetime.datetime.now() - datetime.timedelta(minutes=int(time_value)))
        criteria = f'newer_than:{time_value}h '
        print(criteria)
    elif search_option == "Subject":
        criteria = f'Subject :{search_text} newer_than:{time_value}h '
        print(criteria)
    elif search_option == "From":
        criteria = f'From :"{search_text}" newer_than:{time_value}h '
        print(criteria)
    else:
        # Handle invalid search_option
        text_area.delete(1.0, tk.END)  # Clear previous results
        text_area.insert(tk.END, "Invalid search option selected.")
        return



    try:
        imap.select("inbox")
        _, search_data = imap.search(None, criteria)
        email_count = len(search_data[0].split())
    except Exception as e:
        # Handle the error gracefully
        text_area.delete(1.0, tk.END)  # Clear previous results
        text_area.insert(tk.END, f"Error: {str(e)}")
    else:
        text_area.delete(1.0, tk.END)  # Clear previous results
        text_area.insert(tk.END, f"Total Emails matching criteria: {email_count}\n")

    # Close the mailbox and log out
    imap.logout()








# Create a frame for the checkboxes
checkbox_frame = tk.Frame(root)
checkbox_frame.pack()

# Checkboxes for 'DKIM,' 'SCL,' 'SPF' (inside the checkbox_frame)
dkim_var = tk.IntVar(value=1)  # Set the default value to 1 (checked)
scl_var = tk.IntVar(value=1)  
spf_var = tk.IntVar()

dkim_checkbox = ttk.Checkbutton(checkbox_frame, text="DKIM", variable=dkim_var)
scl_checkbox = ttk.Checkbutton(checkbox_frame, text="SCL", variable=scl_var)
spf_checkbox = ttk.Checkbutton(checkbox_frame, text="SPF", variable=spf_var)

dkim_checkbox.pack(side=tk.LEFT, padx=10, pady=5)
scl_checkbox.pack(side=tk.LEFT, padx=10, pady=5)
spf_checkbox.pack(side=tk.LEFT, padx=10, pady=5)




# Label and input field for 'Time of Search by Min'
time_label = ttk.Label(root, text="Time of Search by heure:")
time_label.pack()

time_entry = ttk.Entry(root)
time_entry.insert(0, "1")  # Set the initial text

time_entry.pack()

# Button for 'Check'
check_button = ttk.Button(root, text="Check", command=fetch_email_counts)
check_button.pack()


# Text area for displaying results
text_area = tk.Text(root, wrap=tk.WORD, width=40, height=10)
text_area.pack()


# Initialize the email dropdown
update_email_dropdown()

# Start the main loop
root.mainloop()
