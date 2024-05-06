import tkinter as tk
from tkinter import font
# from tkfontawesome import tfa_init
import tkfontawesome as tkfa
from tkinter.colorchooser import askcolor
from tkinter import filedialog
import xml.etree.ElementTree as ET

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
    def __init__(self, *args, title,icon=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.title = title
        self.icon=icon
        self.hover_text = tk.Label(self.master, font=("Arial", 10), relief=tk.FLAT)
        self.hover_text.pack(side="top", fill="x")
        if icon:
            icon_font = font.Font(family="FontAwesome", size=16)
            self.config(text=icon, font=icon_font)
        # elif title:
        else:
            self.config(text=title)
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

class DrawingObject:
    def __init__(self, start_x, start_y, end_x, end_y, fill_color):
        # self.tk_object = object
        self.fill_color = fill_color
        self.type = "object"

    def convert_to_xml():
        pass

class Line(DrawingObject):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tk_object = master.create_line(*args, **kwargs)
        self.type = "line"

class Rectangle(DrawingObject):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tk_object = master.create_rectangle(*args, **kwargs)
        self.corner_style = "square"
        self.type = "rectangle"

class GroupComposite(DrawingObject):
    def __init__(self, master, canvas, *args, **kwargs):
        self.objects = []
        self.type = "group"
        self.canvas = canvas

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    def recurse_object(self, func, group):
        for obj in group.objects:
            if type(obj) == int:
                func(obj)
            else:
                self.recurse_object(func, obj)

    def get_bounding_box(self):
        # Calculate the bounding box of the group based on the objects it contains
        if not self.objects:
            return None
        
        self.coordinates = []
        self.recurse_object(lambda obj: self.coordinates.append((self.canvas.coords(obj)[0], self.canvas.coords(obj)[1])), self)
        self.recurse_object(lambda obj: self.coordinates.append((self.canvas.coords(obj)[2], self.canvas.coords(obj)[3])), self)
        # for i in range(4):
        #     for obj in self.objects:
        #         if type(obj) != int:
                    # coordinates.append((self.canvas.coords(obj)[0], self.canvas.coords(obj)[1]))
                    # coordinates.append((self.canvas.coords(obj)[2], self.canvas.coords(obj)[3]))

        min_x = min(self.coordinates, key=lambda x: x[0])[0]
        min_y = min(self.coordinates, key=lambda x: x[1])[1]
        max_x = max(self.coordinates, key=lambda x: x[0])[0]
        max_y = max(self.coordinates, key=lambda x: x[1])[1]


        return min_x, min_y, max_x, max_y

class DrawingEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Drawing Editor")
        
        self.canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack(side=tk.RIGHT)

        self.selected_type = None
        self.selected_objects = []
        self.clipboard_objects = []
        self.objects = []
        self.groups = []

        # Toolbar or menu creation
        self.create_toolbar()

        self.start_x = None
        self.start_y = None
        self.drawing = False
        self.current_object = None
        self.select = True

        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0

        self.bounding_rect = None
        self.proximity_threshold = 10
        
        # self.rect_type=None
        # self.rect_type=tk.StringVar(self.master)
        self.rect_type=[]
    
    def pick_color(self):
        color = askcolor(title="Choose line color")[1]  
        if color:
            rgb_color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            self.color_variable.set(rgb_color)
            # self.canvas.create_line(50, 100, 250, 100, fill=color, width=2)

    def dehighlight_object(self):
        print(self.selected_objects)
        for selected_object in self.selected_objects:
            if type(selected_object) != int:
                func = lambda obj: self.canvas.itemconfig(obj, width=1)
                selected_object.recurse_object(func, selected_object)
                # for object in selected_object.objects:
                #     self.canvas.itemconfig(object, width=1)
                if self.bounding_rect:
                    self.canvas.delete(self.bounding_rect)
                    self.bounding_rect = None
            self.canvas.itemconfig(selected_object, width=1)
        self.selected_objects = []

    def highlight_object(self, object):
        # parent_group = self.parent_group(object)
        if type(object) != int:
            self.canvas.delete(self.bounding_rect)
            coords = object.get_bounding_box()
            self.bounding_rect = self.canvas.create_rectangle(*coords, outline="black", dash=(2,4))
            self.selected_objects.append(object)
            print(self.selected_objects)
            func = lambda obj: self.canvas.itemconfig(obj, width = 5)
            object.recurse_object(func, object)
            # for object in object.objects:
            #     self.canvas.itemconfig(object, width=5)

        else:
            self.canvas.itemconfig(object, width=5)
            if object not in self.selected_objects:
                self.selected_objects.append(object)

    def get_closest_object(self, event):
        closest_element = self.get_closest_element(event)
        parent_group = self.parent_group(closest_element)
        if parent_group:
            return parent_group
        else:
            return closest_element
    
    def get_closest_element(self, event):
        closest_objects = self.canvas.find_overlapping(
            event.x - self.proximity_threshold, event.y - self.proximity_threshold,
            event.x + self.proximity_threshold, event.y + self.proximity_threshold
        )

        if closest_objects: 
            return closest_objects[0]
        return None
    
    def on_canvas_right_click(self, event):
        
        obj = self.get_closest_element(event)
        if not obj:
            return
        
        # Create a context menu for editing object properties
        menu = tk.Menu(self.master, tearoff=0)

        # Color submenu
        color_menu = tk.Menu(menu, tearoff=0)
        colors = ["black", "red", "blue", "green", "yellow"]  # Add more colors as needed
        for color in colors:
            color_menu.add_command(label=color, command=lambda c=color: self.change_object_color(obj, c))
        menu.add_cascade(label="Color", menu=color_menu)

        # Other options
        menu.add_command(label="Select", command=lambda: self.select_object(obj))
        # menu.add_command(label="Copy", command=lambda: self.copy_object(obj))
        menu.add_command(label="Duplicate", command=lambda: self.duplicate_object(obj))
        menu.add_command(label="Delete", command=lambda: self.delete_object(obj))
        
        # print(self.selected_type)
        if (self.selected_type=="rectangle"):
            types_menu=tk.Menu(menu,tearoff=0)
            types=["rounded","square"]
            for type1 in types:
                types_menu.add_command(label=type1,command=lambda t=type1:self.change_type(obj,t))
            menu.add_cascade(label="Type",menu=types_menu)
        # if self.selected_type == "line":
        #     self.rect_type[obj] = None  # None indicates it's not a rectangle
        # elif self.selected_type == "rectangle":
        #     # self.rect_type[obj] = "square"  
        menu.tk_popup(event.x_root, event.y_root)

    def change_object_color(self, obj, color):
        # Change the color of the selected object
        self.canvas.itemconfig(obj, fill=color)

    def change_type(self, obj, type1):
    # Change the type of the selected object
        # self.rect_type[obj] = type1
       if self.selected_type == "rectangle" and type1 == "rounded":
            # Get the coordinates of the rectangle
            print(self.canvas.coords(obj))
            coords= self.canvas.coords(obj)
            # self.canvas.delete(obj)
            # self.canvas.update()

    def set_current_object(self, object_type):
        self.selected_type = object_type

    def duplicate_object(self, obj):
        # Get the type and properties of the object
        obj_type = self.canvas.type(obj)
        coords = self.canvas.coords(obj)
        color = self.canvas.itemcget(obj, "fill")
        print(coords)
        offset = 20
        translated_coords = [coord + offset for coord in coords]
        if obj_type == "line":
            print("hi")
            new_obj = self.canvas.create_line(translated_coords, fill=color)
        elif obj_type == "rectangle":
            new_obj = self.canvas.create_rectangle(translated_coords, fill=color)
        self.objects.append(new_obj)


    def create_toolbar(self):
        # Create toolbar buttons or menu here
        self.left_panel = tk.Frame(self.master, width=150)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.left_panel.pack_propagate(False)
        # self.color_picker_label = tk.Label(self.left_panel, text="Select Color:", **button_style)
        # self.color_picker_label.pack(fill=tk.X)
        self.color_picker_button = Button(self.left_panel, title="Select Color", command=self.pick_color)
        self.color_picker_button.pack(fill=tk.X)

        self.color_variable = tk.StringVar(self.master)
        self.color_variable.set("(0,0,0)");  # Default color

        colors = ["black", "red", "blue", "green", "yellow"]  # Add more colors as needed

        # self.color_picker = tk.OptionMenu(self.left_panel, self.color_variable, *colors)
        # self.color_picker.config(width=20, **button_style)
        # self.color_picker.pack(fill=tk.X)
        # Add buttons with styling
        # self.line_button = Button(self.left_panel, title="Draw Line", command=lambda: self.set_current_object("line"), **button_style)
        # self.line_button = Button(self.left_panel, title="Draw Line",icon="fa-long-arrow-right", command=lambda: self.set_current_object("line"), **button_style)
        
        self.line_button = Button(self.left_panel, title="Draw Line", icon="\u2014", command=lambda: self.set_current_object("line"), **button_style)
        self.line_button.pack(side=tk.TOP, fill=tk.X)

        self.rect_button = Button(self.left_panel, title="Draw Rectangle",icon="\uf0c8", command=lambda: self.set_current_object("rectangle"), **button_style)
        self.rect_button.pack(fill=tk.X)

        self.rect_button = Button(self.left_panel, title="Open File", command=lambda: self.open_drawing("1.txt"), **button_style)
        self.rect_button.pack(fill=tk.X)

        self.rect_button = Button(self.left_panel, title="Save File", command=lambda: self.save_drawing("1.txt"), **button_style)
        self.rect_button.pack(fill=tk.X)

        # XML button
        self.rect_button = Button(self.left_panel, title="XML", command=lambda: self.export_to_xml("4"), **button_style)
        self.rect_button.pack(fill=tk.X)
        
        # Select button
        self.rect_button = Button(self.left_panel, title="Select", command=lambda: self.set_current_object(None), **button_style)
        self.rect_button.pack(fill=tk.X)

        # Select button
        self.rect_button = Button(self.left_panel, title="Group", command=lambda: self.group_objects(), **button_style)
        self.rect_button.pack(fill=tk.X)
        
        # Select button
        self.rect_button = Button(self.left_panel, title="Ungroup", command=lambda: self.ungroup_objects(), **button_style)
        self.rect_button.pack(fill=tk.X)
        
        # Event bindings
        self.canvas.bind("<Control-c>", self.copy_object_shortcut)
        self.canvas.bind("<Control-v>", self.paste_object_shortcut)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<Button-3>",self.on_canvas_right_click)
        self.canvas.focus_set()

    def on_canvas_click(self, event):
        # Handle canvas click event
        
        nearest_object = self.get_closest_object(event)
        if nearest_object in self.selected_objects:
            self.dragging = True
        else:
            self.canvas.delete(self.bounding_rect)
            self.drawing = True

        self.start_x = event.x
        self.start_y = event.y

        if self.current_object and self.select:
            self.canvas.delete(self.current_object)
        self.current_object = None

        if (not (event.state & 0x4)) and not self.dragging:
            self.dehighlight_object()

    def on_canvas_release(self, event):
        # Handle canvas release event
        if self.drawing:
            self.end_x=event.x
            self.end_y=event.y
            if self.current_object:
                self.canvas.delete(self.current_object)  # Delete the temporary line
                self.current_object = self.draw_object(self.selected_type, self.start_x, self.start_y, event.x, event.y, realObject=True)
                self.select = (self.selected_type == None)
            self.drawing = False

        if not self.selected_type:
            if event.x == self.start_x and event.y == self.start_y:
                drawing_object = self.get_closest_object(event)
                self.highlight_object(drawing_object)
        
        self.dragging = False

    def on_mouse_drag(self, event):
        # Handle mouse drag event
        if self.drawing:
            if self.current_object and self.select:
                self.canvas.delete(self.current_object)  # Delete previous temporary line
            self.current_object = self.draw_object(self.selected_type, self.start_x, self.start_y, event.x, event.y, fill="black")
            self.select = True

        elif self.dragging and self.selected_objects:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.start_x = event.x
            self.start_y = event.y

            for selected_object in self.selected_objects:
                if type(selected_object) != int:
                    for object in selected_object.objects:
                        self.canvas.move(object, dx, dy)
                    
                    if self.bounding_rect:
                        self.canvas.move(self.bounding_rect, dx, dy)

                else:
                    self.canvas.move(selected_object, dx, dy)
    
    def create_rectangle(self, x1, y1, x2, y2, radius,type_rect, **kwargs):
        points = [x1 + radius, y1,
                x1 + radius, y1,
                x2 - radius, y1,
                x2 - radius, y1,
                x2, y1,
                x2, y1 + radius,
                x2, y1 + radius,
                x2, y2 - radius,
                x2, y2 - radius,
                x2, y2,
                x2 - radius, y2,
                x2 - radius, y2,
                x1 + radius, y2,
                x1 + radius, y2,
                x1, y2,
                x1, y2 - radius,
                x1, y2 - radius,
                x1, y1 + radius,
                x1, y1 + radius,
                x1, y1]

        if (type_rect=="rounded"):
            # print("rounded")
            self.canvas.create_polygon(points,**kwargs,smooth=True)
        else:
            print("square")
            print(points)
            self.canvas.create_polygon(points,**kwargs)


    def draw_object(self, object_type, start_x, start_y, end_x, end_y, realObject=False, **kwargs):
        # Draw object on canvas based on type and coordinates
        color = self.color_variable.get()
        hex_color = self.rgb_to_hex(color)
        kwargs['fill'] = hex_color
        # type_rect=self.canvas.itemcget("tag")
        # tags=self.canvas.gettags()
        # Store reference to drawn object
        drawn_object = None
        if object_type == "line":
            line_object = Line(self.canvas, start_x, start_y, end_x, end_y, kwargs)
            if realObject:
                self.objects.append(line_object)
            return line_object.tk_object
        
        elif object_type == "rectangle":
            kwargs['fill'] = None
            rect_object = Rectangle(self.canvas, start_x, start_y, end_x, end_y, kwargs)
            if realObject:
                self.objects.append(rect_object)
            return rect_object.tk_object
        else:
            kwargs["fill"] = None
            return self.canvas.create_rectangle(start_x, start_y, end_x, end_y, dash=(2,4), **kwargs)

    def rgb_to_hex(self, rgb_color):
        rgb_values = tuple(map(int, rgb_color.strip('()').split(',')))
        r = max(0, min(int(rgb_values[0]), 255))
        g = max(0, min(int(rgb_values[1]), 255))
        b = max(0, min(int(rgb_values[2]), 255))
        
        # Convert each component to hexadecimal format
        hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
        # print("value",hex_color);
        return str(hex_color)

    def select_object(self, object):
        # Select object on canvas
        pass

    def delete_object(self, object):
        # Delete object from canvas
        self.canvas.delete(object)
        pass

    def map_object(self, object):
        for obj in self.objects:
            if obj.tk_object == object:
                return obj
        return None

    def copy_object_shortcut(self,event):
    # Copy the selected object to clipboard when Ctrl+C is pressed
        self.clipboard_objects = []
        for selected_object in self.selected_objects:
            self.clipboard_objects.append(self.map_object(selected_object))

    def paste_object_shortcut(self, event):
        # Paste the object from clipboard when Ctrl+P is pressed
        self.dehighlight_object()
        for clipboard_object in self.clipboard_objects:
            # Get the coordinates of the cursor
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            
            # Get the fill color of the clipboard object
            fill_color = self.color_variable.get();
            fill_color = self.rgb_to_hex(fill_color)
            
            coords = self.canvas.coords(clipboard_object.tk_object)
            new_coords = [x, y, x + (coords[2] - coords[0]), y + coords[3] - coords[1]]
            new_object = self.draw_object(clipboard_object.type, *new_coords, fill=fill_color)
            
            self.highlight_object(new_object)

    def move_object(self, object, new_x, new_y):
        # Move object to new coordinates
        pass

    def edit_object(self, object):
        # Open dialog box to edit object properties
        pass

    def parent_group(self, object):
        for group in self.groups:
            if object in group.objects:
                return group
        
        return None

    def group_objects(self):
        group = GroupComposite(self.master, self.canvas)
        for obj in self.selected_objects:
            group.add_object(obj)
        self.groups.append(group)

    def ungroup_objects(self):
        self.selected_objects = []
        for obj in self.selected_objects:
            if type(obj) != int:
                for object in obj.objects:
                    self.selected_objects.append(object)
                self.groups.remove(obj)

    def save_drawing(self, filename):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                # print(self.objects)
                for obj in self.objects:
                    print(obj)
                    coords = self.canvas.coords(obj)
                    color = self.canvas.itemcget(obj, "fill")
                    
                    file.write(f"{self.selected_type} {coords[0]} {coords[1]} {coords[2]} {coords[3]} {color} \n")
    def clear_canvas(self):
    # Clear all objects on the canvas
        self.canvas.delete("all")
        # Clear the list of stored objects
        self.objects = []

    def open_drawing(self, filename):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.clear_canvas()
            with open(file_path, "r") as file:
                for line in file:
                    parts = line.strip().split()
                    print(parts)
                    if len(parts) < 5:
                        continue  # Skip lines that don't have enough elements
                    shape = parts[0]  # Get the shape type (e.g., line, rect)
                    if shape == 'line' and len(parts) == 6:
                        x1, y1, x2, y2 = map(float, parts[1:5])
                        color=parts[5]
                        self.set_current_object("line");
                        self.draw_object(self.selected_type,x1, y1, x2, y2)
                    elif shape == 'rect' and len(parts) == 7:
                        x1, y1, x2, y2, color, style = map(float, parts[1:6])
                        self.set_current_object("rectangle");
                        self.draw_object(self.selected_type,x1, y1, x2, y2)
                    else:
                        print("Invalid line:", line.strip())

    def export_to_xml(self, filename):
        root = ET.Element("objects")
        for obj in self.canvas.find_all():
            print(self.canvas.type(obj))
            if self.canvas.type(obj) == "polygon":
                self.export_rectangle_to_xml(root, obj)
            elif self.canvas.type(obj) == "line":
                self.export_line_to_xml(root, obj)
        
        tree = ET.ElementTree(root)
        tree.write(filename + ".xml")

    def export_rectangle_to_xml(self, parent, obj):
        coords = self.canvas.coords(obj)
        upper_left_x = min(coords[0], coords[4])
        upper_left_y = min(coords[1], coords[3])
        lower_right_x = max(coords[0], coords[4])
        lower_right_y = max(coords[1], coords[3])
        color = self.canvas.itemcget(obj, "fill")
        rectangle = ET.SubElement(parent, "rectangle")
        upper_left = ET.SubElement(rectangle, "upper-left")
        upper_left_x_el = ET.SubElement(upper_left, "x")
        upper_left_x_el.text = str(upper_left_x)
        upper_left_y_el = ET.SubElement(upper_left, "y")
        upper_left_y_el.text = str(upper_left_y)
        lower_right = ET.SubElement(rectangle, "lower-right")
        lower_right_x_el = ET.SubElement(lower_right, "x")
        lower_right_x_el.text = str(lower_right_x)
        lower_right_y_el = ET.SubElement(lower_right, "y")
        lower_right_y_el.text = str(lower_right_y)
        color_el = ET.SubElement(rectangle, "color")
        color_el.text = color

    def export_line_to_xml(self, parent, obj):
        x1, y1, x2, y2 = self.canvas.coords(obj)
        color = self.canvas.itemcget(obj, "fill")
        line = ET.SubElement(parent, "line")
        begin = ET.SubElement(line, "begin")
        begin_x = ET.SubElement(begin, "x")
        begin_x.text = str(x1)
        begin_y = ET.SubElement(begin, "y")
        begin_y.text = str(y1)
        end = ET.SubElement(line, "end")
        end_x = ET.SubElement(end, "x")
        end_x.text = str(x2)
        end_y = ET.SubElement(end, "y")
        end_y.text = str(y2)
        color_el = ET.SubElement(line, "color")
        color_el.text = color

def main():
    root = tk.Tk()
    app = DrawingEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
