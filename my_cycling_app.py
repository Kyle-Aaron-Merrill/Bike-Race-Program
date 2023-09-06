import sqlite3
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from tkinter import messagebox

# Function to submit participant data to the database
def submit_participant():
    # Retrieve values from the input fields
    name = entry_name.get()
    weekly_pace = entry_weekly_pace.get()
    avg_pace = entry_avg_pace.get()
    bike_type = selected_bike_type.get()
    gender = selected_gender.get()

    # Null checks
    if not name or not name.strip():
        messagebox.showerror("Error", "Please enter a valid name.")
        return

    # Additional null checks for weekly pace and average pace
    if not weekly_pace:
        messagebox.showerror("Error", "Please enter your weekly mileage.")
        return
    if not avg_pace:
        messagebox.showerror("Error", "Please enter your average pace.")
        return

    # Numeric checks for weekly pace and average pace
    if not weekly_pace.isdigit() or int(weekly_pace) < 1 or int(weekly_pace) > 500:
        messagebox.showerror("Error", "Please enter a valid weekly mileage (1-500 miles).")
        return
    if not avg_pace.isdigit() or int(avg_pace) < 1 or int(avg_pace) > 30:
        messagebox.showerror("Error", "Please enter a valid average pace (1-30 mph).")
        return

    # If all checks pass, you can proceed with submitting the data to the database
    # Insert participant data into the database
    cursor.execute("""
        INSERT INTO participants (name, weekly_pace, avg_pace, bike_type, gender)
        VALUES (?, ?, ?, ?, ?)
    """, (name, int(weekly_pace), int(avg_pace), bike_type, gender))

    conn.commit()

    # Assign a unique participant number (ID)
    participant_id = cursor.lastrowid

    # Optionally, clear the entry fields after successful submission
    entry_name.delete(0, tk.END)
    entry_weekly_pace.delete(0, tk.END)
    entry_avg_pace.delete(0, tk.END)

    # Inform the user that the data was successfully submitted
    messagebox.showinfo("Success", f"Participant {participant_id} data submitted successfully!")

# Function to switch between screens
def show_screen(screen_frame):
    signup_frame.pack_forget()
    waves_frame.pack_forget()
    results_frame.pack_forget()
    screen_frame.pack(fill="both", expand=True)

# Connect to the SQLite database
conn = sqlite3.connect("bike_race.db")
cursor = conn.cursor()

# Create the main application window
root = tk.Tk()
root.title("Cycling Wave Organizer")
root.attributes('-fullscreen', True)

# Apply a modern theme
style = ThemedStyle(root)
style.set_theme("plastik")

font_style = ("Segoe UI", 18)
padx_value = 10
pady_value = 5

signup_frame = ttk.Frame(root, padding=20)
waves_frame = ttk.Frame(root, padding=20)
results_frame = ttk.Frame(root, padding=20)

title_label = tk.Label(root, text="Cycling Wave Organizer", font=("Segoe UI", 36))
title_label.pack(padx=20, pady=20, fill="x")

breadcrumb_label = tk.Label(root, text="Home > Registration", font=("Segoe UI", 14))
breadcrumb_label.pack(padx=20, pady=10, anchor="w")

meatball_menu = tk.Menu(root)
meatball_menu.add_command(label="Registration", command=lambda: show_screen(signup_frame))
meatball_menu.add_command(label="Generate Waves", command=lambda: show_screen(waves_frame))
meatball_menu.add_command(label="Results", command=lambda: show_screen(results_frame))
root.config(menu=meatball_menu)

# Create labels and entry fields for participant signup screen
label_name = tk.Label(signup_frame, text="Name:", font=font_style)
label_name.pack(padx=10, pady=5, anchor="w")
entry_name = tk.Entry(signup_frame, font=font_style, bd=0)
entry_name.pack(padx=10, pady=5, fill="x")

label_weekly_pace = tk.Label(signup_frame, text="Average Weekly Mileage:", font=font_style)
label_weekly_pace.pack(padx=10, pady=5, anchor="w")
entry_weekly_pace = tk.Entry(signup_frame, font=font_style, bd=0)
entry_weekly_pace.pack(padx=10, pady=5, fill="x")

label_avg_pace = tk.Label(signup_frame, text="Average Pace:", font=font_style)
label_avg_pace.pack(padx=10, pady=5, anchor="w")
entry_avg_pace = tk.Entry(signup_frame, font=font_style, bd=0)
entry_avg_pace.pack(padx=10, pady=5, fill="x")

label_bike_type = tk.Label(signup_frame, text="Bike Type:", font=font_style)
label_bike_type.pack(padx=10, pady=5, anchor="w")
bike_types = ["Mountain Bike", "Road/Gravel", "Hybrid", "BMX", "Touring", "Other"]
selected_bike_type = tk.StringVar()
entry_bike_type = ttk.Combobox(signup_frame, textvariable=selected_bike_type, values=bike_types, font=font_style)
entry_bike_type.pack(padx=10, pady=5, fill="x")

label_gender = tk.Label(signup_frame, text="Gender:", font=font_style)
label_gender.pack(padx=10, pady=5, anchor="w")
genders = ["Male", "Female", "Other"]
selected_gender = tk.StringVar()
entry_gender = ttk.Combobox(signup_frame, textvariable=selected_gender, values=genders, font=font_style)
entry_gender.pack(padx=10, pady=5, fill="x")

# Button to submit participant data
submit_button_signup = ttk.Button(signup_frame, text="Submit", command=submit_participant)
submit_button_signup.pack(pady=10)

# Create content for the "Generate Waves" screen
label_waves = tk.Label(waves_frame, text="Generate Waves", font=("Segoe UI", 24))
label_waves.pack(padx=20, pady=20)

stage_wave_button = ttk.Button(waves_frame, text="Stage Next Wave", command=lambda: show_screen(results_frame))
stage_wave_button.pack(pady=10)

# Create content for the "Results" screen
label_results = tk.Label(results_frame, text="Results", font=("Segoe UI", 24))
label_results.pack(padx=20, pady=20)

back_button_results = ttk.Button(results_frame, text="Back to Signup", command=lambda: show_screen(signup_frame))
back_button_results.pack(pady=10)

results_display = tk.Text(results_frame, height=10, width=40, font=("Segoe UI", 16), bd=0, bg="#F0F0F0")
results_display.pack(padx=20, pady=20, fill="both", expand=True)

close_button = ttk.Button(results_frame, text="Close", command=root.destroy)
close_button.pack(pady=10)

show_screen(signup_frame)

root.mainloop()
