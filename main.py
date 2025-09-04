import tkinter as tk

def get_name():
    # Temporarily remove topmost so popup can appear
    window.attributes("-topmost", False)

    # Create modal popup
    popup = tk.Toplevel(window)
    popup.title("Enter Your Name To Unlock Your System")
    popup.geometry("450x200")
    popup.configure(bg="black")  # black background
    popup.transient(window)
    popup.grab_set()
    popup.focus_force()

    # Center popup relative to main window
    window.update_idletasks()
    window_x = window.winfo_rootx()
    window_y = window.winfo_rooty()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    popup.geometry("+%d+%d" % (window_x + window_width//2 - 225, window_y + window_height//2 - 100))

    # Title label
    tk.Label(
        popup, text="Enter Your Name", font=("Arial", 18, "bold"), bg="black", fg="white"
    ).pack(pady=(20,10))

    # Entry box
    name_var = tk.StringVar()
    entry = tk.Entry(popup, textvariable=name_var, font=("Arial", 16), width=25, justify='center', bg="white", fg="black")
    entry.pack(pady=10)
    entry.focus_set()

    # Submit button
    def submit():
        if name_var.get().strip():  # only accept non-empty input
            popup.destroy()

    submit_btn = tk.Button(popup, text="Submit", command=submit, font=("Arial", 14), bg="#4CAF50", fg="Black", width=12)
    submit_btn.pack(pady=15)

    popup.wait_window()  # wait until user submits

    # Restore topmost on main window
    window.attributes("-topmost", True)
    return name_var.get().strip()


# Main window
window = tk.Tk()
window.title("Pianto")
window.attributes("-fullscreen", True)
window.overrideredirect(True)
window.configure(bg="red")
window.attributes("-topmost", True)
window.protocol("WM_DELETE_WINDOW", lambda: None)

# Center frame
center_frame = tk.Frame(window, bg="red")
center_frame.pack(expand=True)

# Title label
title_label = tk.Label(center_frame, text="Your System Has Been Encrypted By Pianto", font=("Arial", 30, "bold"), bg="red", fg="white")
title_label.pack(pady=20)

# Greeting label
greeting_label = tk.Label(center_frame, text="", font=("Arial", 24), bg="red", fg="white")
greeting_label.pack(pady=20)

# Refocus if window loses focus
def refocus(event):
    window.lift()
    window.focus_force()

window.bind("<FocusOut>", refocus)

# Ask for name until valid input
def ask_name():
    name = ""
    while not name:
        name = get_name()
    greeting_label.config(text=f"Hello, {name}! I am Pianto.")
    close_btn = tk.Button(center_frame, text="Close", command=window.destroy, font=("Arial", 16))
    close_btn.pack(pady=30)

window.after(500, ask_name)
window.mainloop()
