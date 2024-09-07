
import math
import tkinter as tk

class Line:
    def __init__(self, canvas, start_point, length, scale=50):
        self.canvas = canvas
        self.start_point = start_point
        self.length = length
        self.scale = scale
        self.fixed_movement = False  # Nuevo atributo para el modo de movimiento fijo

        # Calcular el punto final basado en la longitud
        self.end_point = (self.start_point[0] + self.length * self.scale, self.start_point[1])

        # Dibujar la línea y puntos de anclaje
        self.line = self.canvas.create_line(self.start_point, self.end_point, fill="black", width=2)
        self.start_anchor = self.canvas.create_oval(self.start_point[0]-5, self.start_point[1]-5,
                                                    self.start_point[0]+5, self.start_point[1]+5, fill="red")
        self.end_anchor = self.canvas.create_oval(self.end_point[0]-5, self.end_point[1]-5,
                                                  self.end_point[0]+5, self.end_point[1]+5, fill="red")
        self.label = self.create_label()

        # Añadir la funcionalidad de arrastre a los puntos de anclaje
        self.canvas.tag_bind(self.start_anchor, "<B1-Motion>", self.drag_start_anchor)
        self.canvas.tag_bind(self.end_anchor, "<B1-Motion>", self.drag_end_anchor)
        
        # Registrar la línea en el canvas para su uso posterior
        if not hasattr(self.canvas, 'lines'):
            self.canvas.lines = []
        self.canvas.lines.append(self)

    def create_label(self):
        mid_x = (self.start_point[0] + self.end_point[0]) / 2
        mid_y = (self.start_point[1] + self.end_point[1]) / 2
        return self.canvas.create_text(mid_x, mid_y, text=str(self.length), font=("Arial", 12))
    
    def update_length(self, new_end_point):
        self.end_point = new_end_point
        self.length = self.calculate_length(self.start_point, self.end_point)
        self.canvas.coords(self.line, *self.start_point, *self.end_point)
        self.update_label()
    
    def update_label(self):
        mid_x = (self.start_point[0] + self.end_point[0]) / 2
        mid_y = (self.start_point[1] + self.end_point[1]) / 2
        self.canvas.coords(self.label, mid_x, mid_y - 10)
        self.canvas.itemconfig(self.label, text=f"{self.length:.2f} m")

    def drag_start_anchor(self, event):
        self.move_anchor('start', event.x, event.y)

    def drag_end_anchor(self, event):
        self.move_anchor('end', event.x, event.y)

    def move_anchor(self, anchor_type, x, y):
        # Si el movimiento fijo está activado, mover solo en la dirección horizontal o vertical
        if self.fixed_movement:
            if anchor_type == 'start':
                y = self.start_point[1]
            else:
                y = self.end_point[1]
        
        # Mover el punto de anclaje
        if anchor_type == 'start':
            self.canvas.coords(self.start_anchor, x-5, y-5, x+5, y+5)
            self.start_point = (x, y)
        else:
            self.canvas.coords(self.end_anchor, x-5, y-5, x+5, y+5)
            self.end_point = (x, y)
        
        # Redibujar la línea
        self.canvas.coords(self.line, self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1])
        self.canvas.coords(self.label, (self.start_point[0] + self.end_point[0]) / 2,
                                        (self.start_point[1] + self.end_point[1]) / 2)
        
        # Verificar si está cerca de otro anclaje y activar el "imán"
        self.check_anchor_snap()

    def check_anchor_snap(self):
        threshold = 10  # Distancia mínima para activar el imán

        for line in self.canvas.lines:
            if line is self:
                continue

            for anchor in [line.start_point, line.end_point]:
                if self.distance(self.start_point, anchor) < threshold:
                    self.snap_to_anchor(self.start_anchor, anchor)
                if self.distance(self.end_point, anchor) < threshold:
                    self.snap_to_anchor(self.end_anchor, anchor)
    
    def calculate_length(self, start, end):
        dx = (end[0] - start[0]) / self.scale
        dy = (end[1] - start[1]) / self.scale
        return math.sqrt(dx ** 2 + dy ** 2)

    def snap_to_anchor(self, anchor, target):
        # Mover el anclaje al objetivo más cercano
        self.canvas.coords(anchor, target[0]-5, target[1]-5, target[0]+5, target[1]+5)
        
        # Actualizar las coordenadas de la línea
        if anchor == self.start_anchor:
            self.start_point = target
        else:
            self.end_point = target
        
        # Redibujar la línea
        self.canvas.coords(self.line, self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1])
        self.canvas.coords(self.label, (self.start_point[0] + self.end_point[0]) / 2,
                                        (self.start_point[1] + self.end_point[1]) / 2)

    def set_fixed_movement(self, fixed):
        self.fixed_movement = fixed
    
    def redraw(self):
        self.canvas.coords(self.line, *self.start_point, *self.end_point)
        self.update_label()
        self.canvas.coords(self.start_anchor, self.start_point[0]-5, self.start_point[1]-5,
                           self.start_point[0]+5, self.start_point[1]+5)
        self.canvas.coords(self.end_anchor, self.end_point[0]-5, self.end_point[1]-5,
                           self.end_point[0]+5, self.end_point[1]+5)
    
    def is_within_point(self, click_x, click_y, point_x, point_y):
        return (
            click_x >= point_x - self.scale and
            click_x <= point_x + self.scale and
            click_y >= point_y - self.scale and
            click_y <= point_y + self.scale
        )
    
    @staticmethod
    def distance(point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
