from Line import Line
import math
class DrawingCanvas:
    def __init__(self, canvas, scale=50, anchor_threshold=10):
        self.canvas = canvas
        self.SCALE = scale
        self.ANCHOR_THRESHOLD = anchor_threshold
        self.lines = []
        self.selected_point = None
        self.dragging = False
        self.fixed_movement_mode = False

        # Vincular eventos del canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.move_point)
        self.canvas.bind("<ButtonRelease-1>", self.release_point)

    def draw_line(self, start_point, length):
        # Crear una nueva línea utilizando la clase Line
        new_line = Line(self.canvas, start_point, length, self.SCALE)
        self.lines.append(new_line)
        return new_line.end_point

    def on_canvas_click(self, event):
        print(f"Clic en: ({event.x}, {event.y})")
        for line in self.lines:
            if line.is_within_point(event.x, event.y, *line.start_point):
                self.selected_point = ("start", line)
                self.dragging = True
                print(f"Seleccionado punto de inicio de la línea en: {line.start_point}")
            elif line.is_within_point(event.x, event.y, *line.end_point):
                self.selected_point = ("end", line)
                self.dragging = True
                print(f"Seleccionado punto final de la línea en: {line.end_point}")


    def is_within_point(self, x, y, px, py, threshold=10):
        """Verifica si el punto (x, y) está dentro de un umbral de distancia del punto (px, py)."""
        return abs(x - px) <= threshold and abs(y - py) <= threshold

    def move_point(self, event):
        if self.dragging and self.selected_point is not None:
            point_type, line = self.selected_point
            new_x, new_y = event.x, event.y

            if self.fixed_movement_mode:
                start_x, start_y = line.start_point if point_type == "end" else line.end_point
                angle_radians = math.atan2(new_y - start_y, new_x - start_x)
                angle_degrees = math.degrees(angle_radians)
                snap_angle = round(angle_degrees / 45) * 45
                snap_radians = math.radians(snap_angle)
                length = math.sqrt((new_x - start_x) ** 2 + (new_y - start_y) ** 2)
                new_x = start_x + length * math.cos(snap_radians)
                new_y = start_y + length * math.sin(snap_radians)

            for other_line in self.lines:
                if line != other_line:
                    if self.is_within_point(new_x, new_y, *other_line.start_point):
                        new_x, new_y = other_line.start_point
                    elif self.is_within_point(new_x, new_y, *other_line.end_point):
                        new_x, new_y = other_line.end_point

            if point_type == "end":
                line.end_point = (new_x, new_y)
                self.canvas.coords(line.line, *line.start_point, new_x, new_y)
                self.canvas.coords(line.end_anchor, new_x-5, new_y-5, new_x+5, new_y+5)  # Actualiza el anclaje
            elif point_type == "start":
                line.start_point = (new_x, new_y)
                self.canvas.coords(line.line, new_x, new_y, *line.end_point)
                self.canvas.coords(line.start_anchor, new_x-5, new_y-5, new_x+5, new_y+5)  # Actualiza el anclaje

            line.length = self.calculate_length(line.start_point, line.end_point)
            self.update_line_label(line)
            self.redraw_canvas()

    def release_point(self, event):
        if self.dragging:
            print(f"Soltado en: ({event.x}, {event.y})")
        self.dragging = False
        self.selected_point = None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.lines.clear()
    def calculate_length(self, start_point, end_point):
        """Calcula la longitud de la línea en metros."""
        start_x, start_y = start_point
        end_x, end_y = end_point
        # Calcula la longitud en unidades del sistema de dibujo
        length_in_units = math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
        # Verifica que la escala se aplique correctamente
        length_in_meters = length_in_units * (1 / self.SCALE)
        print(f"Start: {start_point}, End: {end_point}, Length in units: {length_in_units}, Length in meters: {length_in_meters}")
        return length_in_meters

    def update_line_label(self, line):
        """Actualiza la etiqueta de la línea con la longitud actual en metros."""
        if hasattr(line, 'label'):
            new_length = round(line.length, 2)
            self.canvas.itemconfig(line.label, text=f" {new_length} m")
            mid_x = (line.start_point[0] + line.end_point[0]) / 2
            mid_y = (line.start_point[1] + line.end_point[1]) / 2
            self.canvas.coords(line.label, mid_x, mid_y)
