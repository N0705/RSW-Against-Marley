import tkinter as tk

window = tk.Tk()
window.title("Pianto")


label = tk.Label(window, text="Your system has been encrypted by Pianto.", font=("Arial",12))
label.pack(pady=20)

button = tk.Button(window,text="Close", command=window.destroy)
button.pack()

window.mainloop()