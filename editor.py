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
        self.line_button = Button(self.left_panel, title="Draw Line", command=self.draw_object, **button_style)
        self.line_button.config(width=20)
        self.line_button.pack(side=tk.TOP, fill=tk.X)

        self.rect_button = Button(self.left_panel, title="Draw Rectangle", command=self.select_object, **button_style)
        self.rect_button.config(width=20)
        self.rect_button.pack(fill=tk.X)


        self.selected_object = None
        self.objects = []

        # Toolbar or menu creation
        self.create_toolbar()

        # Event bindings
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

    def create_toolbar(self):
        # Create toolbar buttons or menu here
        pass

    def on_canvas_click(self, event):
        # Handle canvas click event
        print(event.x, event.y)
        return 
    
    def on_canvas_release(self, event):
        # Handle canvas release event
        print(event.x, event.y)
        pass

    def on_mouse_drag(self, event):
        # Handle mouse drag event
        pass

    def draw_object(self, object_type, start_x, start_y, end_x, end_y, **kwargs):
        # Draw object on canvas based on type and coordinates
        pass

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
