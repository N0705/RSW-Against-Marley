import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Pianto")
window.geometry("600x400")


label = tk.Label(window, text="Your system has been encrypted by Pianto.", font=("Arial",12))
label.pack(pady=20)

button = tk.Button(window,text="Close", command=window.destroy)
button.pack()
window.attributes("-fullscreen", 1)

window.mainloop()

root = tk.Tk()
root.withdraw()

messagebox.showinfo("Notification","YOU HAVE 2 HOURS TO SEND PAYMENT")
messagebox.showinfo("")