import tkinter as tk

class ColorPicker(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.selected_color = "black"

        self.color_display = tk.Label(self, text="#000000", font=("Arial", 12), bg="white")
        self.color_display.pack(pady=5)

        self.line_canvas = tk.Canvas(self, width=150, height=20, bg="white", bd=0, highlightthickness=0)
        self.line_canvas.pack()

        self.circle = self.line_canvas.create_oval(0, 0, 20, 20, fill=self.selected_color, outline=self.selected_color)
        self.line_canvas.bind("<B1-Motion>", self.move_circle)
        self.line_canvas.bind("<ButtonRelease-1>", self.pick_color)

    def move_circle(self, event):
        x = event.x
        if x < 0:
            x = 0
        elif x > 150:
            x = 150
        self.line_canvas.coords(self.circle, x - 10, 0, x + 10, 20)
        self.update_color(x)

    def update_color(self, x):
        r = int((x / 150) * 255)
        color_hex = "#{:02x}{:02x}{:02x}".format(r, 0, 0)
        self.color_display.config(text=color_hex)
        self.selected_color = color_hex

    def pick_color(self, event=None):
        # You can add custom logic here to use the selected color
        print("Selected color:", self.selected_color)

def main():
    root = tk.Tk()
    root.title("Color Picker")
    color_picker = ColorPicker(root)
    color_picker.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
