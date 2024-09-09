from tkinter.simpledialog import askstring

class LabelManager:
    def __init__(self, canvas):
        self.canvas = canvas
        self.labels = []
        self.legend_labels = []
        self.label_rotation = {}
        self.label_font_size = {}
        self.moving_label = None
        self.selected_label_id = None
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.dragging = False

        self.canvas.tag_bind("legend_label", "<Button-1>", self.on_label_click)
        self.canvas.tag_bind("legend_label", "<B1-Motion>", self.on_label_drag)
        self.canvas.tag_bind("legend_label", "<ButtonRelease-1>", self.on_label_release)

    def add_legend_label(self, text, x, y):
        label_id = self.canvas.create_text(x, y, text=text, anchor="nw", font=("Arial", 12), tags="legend_label")
        self.labels.append({"id": label_id, "text": text, "x": x, "y": y, "font_size": 12, "angle": 0})

    def select_label(self, event):
        self.selected_label_id = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["item"] = self.selected_label_id
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def move_legend_label(self, event, label):
        if self.moving_label:
            x, y = event.x, event.y
            self.canvas.coords(self.moving_label, x, y)
            # Actualiza la posición en legend_labels
            for i, (text, coords) in enumerate(self.legend_labels):
                if coords == self.canvas.coords(label):
                    self.legend_labels[i] = (text, (x, y))
                    break
    def edit_legend_label(self, event, label):
        new_text = askstring("Editar Leyenda", "Introduce el nuevo texto para la leyenda:")
        if new_text:
            self.canvas.itemconfig(label, text=new_text)
            # Actualiza el texto en legend_labels
            for i, (text, coords) in enumerate(self.legend_labels):
                if coords == self.canvas.coords(label):
                    self.legend_labels[i] = (new_text, coords)
                    break

    def increase_font_size(self):
        if self.selected_label_id:
            for label in self.labels:
                if label["id"] == self.selected_label_id:
                    new_font_size = label["font_size"] + 2
                    label["font_size"] = new_font_size
                    self.canvas.itemconfig(label["id"], font=("Arial", new_font_size))
                    break
    def decrease_font_size(self):
        if self.selected_label_id:
            for label in self.labels:
                if label["id"] == self.selected_label_id and label["font_size"] > 6:  # Limit the minimum font size
                    new_font_size = label["font_size"] - 2
                    label["font_size"] = new_font_size
                    self.canvas.itemconfig(label["id"], font=("Arial", new_font_size))
                    break
    def on_legend_label_click(self, event, label):
        self.moving_label = label
    def add_legend_label(self, text, x, y):
        label_id = self.canvas.create_text(x, y, text=text, anchor="nw", font=("Arial", 12), tags="legend_label")
        self.labels.append({"id": label_id, "text": text, "x": x, "y": y, "font_size": 12, "angle": 0})
    def on_label_drag(self, event):
        self.dragging = True  # Set dragging flag
        if self.drag_data["item"]:
            # Calculate the distance moved
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]

            # Move the selected label by the amount dragged
            self.canvas.move(self.drag_data["item"], dx, dy)

            # Update the drag data
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

            # Update the label's stored position
            for label in self.labels:
                if label["id"] == self.drag_data["item"]:
                    label["x"] += dx
                    label["y"] += dy
                    break    
    def on_label_release(self, event):
        if not self.dragging:  # If not dragging, consider it a click for rotation
            self.rotate_selected_label()
        self.drag_data["item"] = None
        self.dragging = False
    def on_label_click(self, event):
        self.selected_label_id = self.canvas.find_closest(event.x, event.y)[0]
        self.drag_data["item"] = self.selected_label_id
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.dragging = False  # Reset dragging flag

    def rotate_selected_label(self):
        if self.selected_label_id:
            current_angle = self.label_rotation.get(self.selected_label_id, 0)
            new_angle = (current_angle + 15) % 360
            self.label_rotation[self.selected_label_id] = new_angle
            self.canvas.itemconfig(self.selected_label_id, angle=new_angle) 
     
    def on_label_release(self, event):
        if not self.dragging:  # If not dragging, consider it a click for rotation
            self.rotate_selected_label()
        self.drag_data["item"] = None
        self.dragging = False