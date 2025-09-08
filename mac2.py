import sys
import tkinter as tk
from tkinter import messagebox

is_windows = sys.platform.startswith("win")

# Set your correct key here
CORRECT_KEY = "pianto123"  

if is_windows:
    import ctypes
    import ctypes.wintypes

    # Windows DPI awareness
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass

    from ctypes import POINTER, c_int, c_ulong

    # Get monitors
    def get_monitors():
        monitors = []

        def monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
            rct = lprcMonitor.contents
            monitors.append({
                "x": rct.left,
                "y": rct.top,
                "width": rct.right - rct.left,
                "height": rct.bottom - rct.top
            })
            return True

        MONITOR_ENUMPROC = ctypes.WINFUNCTYPE(
            c_int, c_ulong, c_ulong, POINTER(ctypes.wintypes.RECT), ctypes.c_double
        )
        try:
            ctypes.windll.user32.EnumDisplayMonitors(0, 0, MONITOR_ENUMPROC(monitor_enum_proc), 0)
        except Exception:
            user32 = ctypes.windll.user32
            monitors.append({
                "x": 0,
                "y": 0,
                "width": user32.GetSystemMetrics(0),
                "height": user32.GetSystemMetrics(1)
            })
        return monitors

    # Fade functions
    def fade_in_windows(windows, steps=20, delay=25):
        for i in range(steps + 1):
            alpha = i / steps
            for w in windows:
                try:
                    w.attributes("-alpha", alpha)
                    w.update()
                except tk.TclError:
                    pass
            if windows:
                windows[0].after(delay)

    def fade_out_windows(windows, steps=20, delay=25):
        if not windows:
            return
        for i in range(steps, -1, -1):
            alpha = i / steps
            for w in windows:
                try:
                    if w.winfo_exists():
                        w.attributes("-alpha", alpha)
                        w.update()
                except tk.TclError:
                    pass
            windows[0].after(delay)

    # Main window
    window = tk.Tk()
    window.overrideredirect(True)
    window.attributes("-topmost", True)
    window.attributes("-alpha", 0.0)
    window.configure(bg="red")

    monitors = get_monitors()
    primary = monitors[0]
    window.geometry(f"{primary['width']}x{primary['height']}+{primary['x']}+{primary['y']}")

    red_windows = []
    for m in monitors[1:]:
        red = tk.Toplevel()
        red.overrideredirect(True)
        red.geometry(f"{m['width']}x{m['height']}+{m['x']}+{m['y']}")
        red.configure(bg="red")
        red.attributes("-topmost", True)
        red.attributes("-alpha", 0.0)
        red.update()
        red_windows.append(red)

    # Labels
    title_label = tk.Label(window, text="Your System", font=("Arial", 30, "bold"),
                           bg="red", fg="white")
    title_label.place(relx=0.5, rely=0.2, anchor="center")

    greeting_label = tk.Label(window, text="", font=("Arial", 24),
                              bg="red", fg="white")
    greeting_label.place(relx=0.5, rely=0.5, anchor="center")

    # Keep window focused
    def refocus(event):
        try:
            window.lift()
            window.focus_force()
        except tk.TclError:
            pass
    window.bind("<FocusOut>", refocus)

    # Email popup
    name_var = tk.StringVar()
    popup = tk.Toplevel(window)
    popup.title("Enter Key")
    popup.configure(bg="black")
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)

    popup_width = 450
    popup_height = 200
    popup.geometry(f"{popup_width}x{popup_height}+{primary['x'] + primary['width']//2 - popup_width//2}+{primary['y'] + primary['height']//2 - popup_height//2}")

    tk.Label(popup, text="Enter Key", font=("Arial", 18, "bold"),
             bg="black", fg="white").pack(pady=(20, 10))

    entry = tk.Entry(popup, textvariable=name_var, font=("Arial", 16), width=25,
                     justify='center', bg="white", fg="black")
    entry.pack(pady=10)
    entry.focus_set()
    popup.grab_set()

    def submit():
        entered_key = name_var.get().strip()
        if entered_key == CORRECT_KEY:
            tk.Button(window, text="Unencrypt", command=window.destroy, font=("Arial", 16))\
                .place(relx=0.5, rely=0.8, anchor="center")
            fade_out_windows(red_windows)
            for w in red_windows:
                try:
                    if w.winfo_exists():
                        w.destroy()
                except tk.TclError:
                    pass
            try:
                if popup.winfo_exists():
                    popup.destroy()
            except tk.TclError:
                pass
        else:
            name_var.set("")
            entry.focus_set()
            messagebox.showerror("Invalid Key", "The key you entered is incorrect. Try again.")

    tk.Button(popup, text="Submit", command=submit, font=("Arial", 14),
              bg="#4CAF50", fg="black", width=12).pack(pady=15)

    window.after(100, lambda: popup.lift())
    fade_in_windows(red_windows + [window])
    window.mainloop()

else:
    # --- macOS version ---
    from screeninfo import get_monitors

    def get_name_on_all_monitors():
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

            x = monitor.x + (monitor.width // 2 - 225)
            y = monitor.y + (monitor.height // 2 - 100)
            popup.geometry(f"+{x}+{y}")

            tk.Label(
                popup, text="Enter Key", font=("Arial", 18, "bold"), bg="black", fg="white"
            ).pack(pady=(20, 10))

            entry = tk.Entry(popup, textvariable=name_var, font=("Arial", 16), width=25,
                             justify='center', bg="white", fg="black")
            entry.pack(pady=10)
            entry.focus_set()

            def submit(p=popup):
                entered_key = name_var.get().strip()
                if entered_key == CORRECT_KEY:
                    for w in popups:
                        w.destroy()
                else:
                    name_var.set("")
                    entry.focus_set()
                    messagebox.showerror("Invalid Key", "The key you entered is incorrect. Try again.")

            submit_btn = tk.Button(popup, text="Submit", command=submit,
                                   font=("Arial", 14), bg="#4CAF50", fg="Black", width=12)
            submit_btn.pack(pady=15)
            popups.append(popup)

        popup.wait_window()
        window.attributes("-topmost", True)
        return name_var.get().strip()

    window = tk.Tk()
    window.title("Pianto")
    window.attributes("-fullscreen", True)
    window.overrideredirect(True)
    window.configure(bg="red")
    window.attributes("-topmost", True)
    window.protocol("WM_DELETE_WINDOW", lambda: None)

    center_frame = tk.Frame(window, bg="red")
    center_frame.pack(expand=True)

    title_label = tk.Label(center_frame, text="Your System", font=("Arial", 30, "bold"), bg="red", fg="white")
    title_label.pack(pady=20)

    greeting_label = tk.Label(center_frame, text="", font=("Arial", 24), bg="red", fg="white")
    greeting_label.pack(pady=20)

    def refocus(event):
        window.lift()
        window.focus_force()
    window.bind("<FocusOut>", refocus)

    def ask_name():
        name = ""
        while not name:
            name = get_name_on_all_monitors()
        close_btn = tk.Button(center_frame, text="Close", command=window.destroy, font=("Arial", 16))
        close_btn.pack(pady=30)

    window.after(500, ask_name)
    window.mainloop()
