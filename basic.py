import tkinter as tk

window=tk.Tk();
label=tk.Label(window,text="Helloworld");
label.pack()

def Button_click():
    print("Button click");
button=tk.Button(window,text="Click Me",command=Button_click);
button.pack();

window.mainloop();