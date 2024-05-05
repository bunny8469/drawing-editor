import tkinter as tk

WIDTH = 1280
HEIGHT = 720

button_style = {
    "bg": "lightgray",
    "fg": "black",
    "font": ("Arial", 12),
    "relief": tk.FLAT,
    "padx": 10,
    "pady": 5
}

class Button(tk.Button):
    def __init__(self, *args, title, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = title
        self.hover_text = tk.Label(self.master, font=("Arial", 10), relief=tk.FLAT)
        self.hover_text.pack(side="top", fill="x")

        # Bind events for hover effect
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.hover_text.configure(text=self.title)

    def on_leave(self, enter):
        self.hover_text.configure(text="")

import random
def random_color():
    # Generate random values for red, green, and blue components
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    # Format the color in hexadecimal format
    color_hex = "#{:02x}{:02x}{:02x}".format(red, green, blue)
    return color_hex

# class DrawingObject:
#     def __init__(self):
#         pass

# class Line:
#     def __init__(self):


class DrawingEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Drawing Editor")
        
        self.canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack(side=tk.RIGHT)

        # Add Left Panel
        self.left_panel = tk.Frame(self.master, width=150)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)

        # Add buttons with styling
        self.line_button = Button(self.left_panel, title="Draw Line", command=lambda: self.set_current_object("line"), **button_style)
        self.line_button.config(width=20)
        self.line_button.pack(side=tk.TOP, fill=tk.X)

        self.rect_button = Button(self.left_panel, title="Draw Rectangle", command=lambda: self.set_current_object("rectangle"), **button_style)
        self.rect_button.config(width=20)
        self.rect_button.pack(fill=tk.X)
        
        self.rect_button = Button(self.left_panel, title="Select", command=lambda: self.set_current_object(None), **button_style)
        self.rect_button.config(width=20)
        self.rect_button.pack(fill=tk.X)

        self.selected_object = None
        self.objects = []

        # Toolbar or menu creation
        self.create_toolbar()

        # Event bindings
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        self.start_x = None
        self.start_y = None
        self.drawing = False
        self.current_object = None
        self.select = False

    def set_current_object(self, object_type):
        self.selected_object = object_type

    def create_toolbar(self):
        # Create toolbar buttons or menu here
        pass

    def on_canvas_click(self, event):
        # Handle canvas click event
        self.start_x = event.x
        self.start_y = event.y
        self.drawing = True

        if self.current_object and not self.selected_object:
            self.canvas.delete(self.current_object)

    def on_canvas_release(self, event):
        # Handle canvas release event
        if self.drawing:
            if self.current_object:
                self.canvas.delete(self.current_object)  # Delete the temporary line
                self.current_object = self.draw_object(self.selected_object, self.start_x, self.start_y, event.x, event.y)
                self.select = self.selected_object
            self.drawing = False

    def on_mouse_drag(self, event):
        # Handle mouse drag event
        if self.drawing:
            if self.current_object and not self.select:
                self.canvas.delete(self.current_object)  # Delete previous temporary line
            self.current_object = self.draw_object(self.selected_object, self.start_x, self.start_y, event.x, event.y, fill="black")
            self.select = True
            

    def draw_object(self, object_type, start_x, start_y, end_x, end_y, **kwargs):
        # Draw object on canvas based on type and coordinates
        if object_type == "line":
            return self.canvas.create_line(start_x, start_y, end_x, end_y, fill=random_color())
        elif object_type == "rectangle":
            return self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=random_color())
        else:
            return self.canvas.create_rectangle(start_x, start_y, end_x, end_y, outline=random_color(), dash=(4, 2))

    def select_object(self, object):
        # Select object on canvas
        pass

    def delete_object(self, object):
        # Delete object from canvas
        pass

    def copy_object(self, object):
        # Copy object on canvas
        pass

    def move_object(self, object, new_x, new_y):
        # Move object to new coordinates
        pass

    def edit_object(self, object):
        # Open dialog box to edit object properties
        pass

    def group_objects(self, objects):
        # Group selected objects
        pass

    def ungroup_objects(self, group):
        # Ungroup selected group
        pass

    def save_drawing(self, filename):
        # Save drawing to file
        pass

    def open_drawing(self, filename):
        # Open drawing from file
        pass

    def export_to_xml(self, filename):
        # Export drawing to XML format
        pass

def main():
    root = tk.Tk()
    app = DrawingEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
