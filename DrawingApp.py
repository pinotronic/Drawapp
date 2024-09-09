import tkinter as tk
from tkinter import Canvas, Button
from tkinter.simpledialog import askstring
import math
from tkinter import filedialog
from DrawingCanvas import DrawingCanvas
from LabelManager import LabelManager
from FileExporter import FileExporter
from Line import *
class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")

        self.canvas = tk.Canvas(root, width=1335, height=660, bg="white")
        self.canvas.pack()
        self.start_point = None
        self.drawing_canvas = DrawingCanvas(self.canvas)
        self.label_manager = LabelManager(self.canvas)
        #self.legend_entry = tk.Entry(root)
        #self.legend_entry.pack()
        self.file_exporter = FileExporter(self.canvas)

        self.current_y_offset = 0
        self.adding_label_mode = False

        self.setup_ui()
        #self.root.bind("<Button-1>", self.test_event_capture)
    def test_event_capture(self, event):
        print(f"Root capturó clic en: ({event.x}, {event.y})")
    def setup_ui(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Caja de texto para la longitud de la línea
        self.length_var = tk.DoubleVar(value=1.0)
        length_entry = tk.Entry(toolbar, textvariable=self.length_var)
        length_entry.pack(side=tk.LEFT)

        # Botón para dibujar la línea
        draw_button = tk.Button(toolbar, text="Dibujar Línea", command=self.execute_draw_line)
        draw_button.pack(side=tk.LEFT)

        # Botón para establecer punto de inicio
        set_start_button = tk.Button(toolbar, text="Punto de Inicio", command=self.set_start_point)
        set_start_button.pack(side=tk.LEFT)

        # Botón para limpiar el canvas
        clear_button = tk.Button(toolbar, text="Limpiar", command=self.execute_clear_canvas)
        clear_button.pack(side=tk.LEFT)
        # Botón para activar/desactivar modo de movimiento fijo
        self.fixed_movement_button = tk.Button(toolbar, text="Fijo", command=self.toggle_fixed_movement_mode)
        self.fixed_movement_button.pack(side=tk.LEFT)

        # Caja de texto para leyenda adicional
        self.legend_entry = tk.Entry(toolbar)  # Ahora se incluye en el toolbar
        self.legend_entry.pack(side=tk.LEFT)
        # Botón para agregar la etiqueta adicional
        add_legend_button = tk.Button(toolbar, text="Agregar Eti", command=self.add_legend_label)
        add_legend_button.pack(side=tk.LEFT)

        # Botón para rotar la etiqueta seleccionada
        rotate_button = tk.Button(toolbar, text="Rotar", command=self.rotate_selected_label)
        rotate_button.pack(side=tk.LEFT)

        # Botón para incrementar el tamaño de la fuente de la etiqueta seleccionada
        self.increase_font_button = tk.Button(toolbar, text="Aumentar F", command=self.increase_font_size)
        self.increase_font_button.pack(side=tk.LEFT)

        # Botón para disminuir el tamaño de la fuente de la etiqueta seleccionada
        decrease_font_button = tk.Button(toolbar, text="Disminuir F", command=self.decrease_font_size)
        decrease_font_button.pack(side=tk.LEFT)
        # Botón para exportar a SVG
        export_button = tk.Button(toolbar, text="SVG", command=self.execute_export_to_svg)
        export_button.pack(side=tk.LEFT)


        self.label_manager = LabelManager(self.canvas)
    def set_start_point(self):
        self.start_point = None
        self.canvas.bind("<Button-1>", self.on_canvas_click)
    def toggle_fixed_movement_mode(self):
        self.drawing_canvas.fixed_movement_mode = not self.drawing_canvas.fixed_movement_mode
        print(f"Modo de movimiento fijo {'activado' if self.drawing_canvas.fixed_movement_mode else 'desactivado'}")
        if self.drawing_canvas.fixed_movement_mode:
            self.fixed_movement_button.config(bg="green", text="Movimiento Fijo Activado")
            print("Modo de movimiento fijo activado.")
        else:
            self.fixed_movement_button.config(bg="SystemButtonFace", text="Activar Movimiento Fijo")
            print("Modo de movimiento fijo desactivado.")
    def enable_add_label_mode(self):
        # Activar el modo de agregar etiqueta
        self.adding_label_mode = True
        # Vincular el evento de clic para agregar la etiqueta a través de LabelManager

        self.canvas.bind("<Button-1>", self.add_legend_label)
        print("Modo para agregar etiqueta de leyenda activado. Haga clic en el canvas para colocar la etiqueta.")
        # Crear el contenido SVG
        svg_content = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1">\n'
        for line in self.lines:
            start_x, start_y = line["start"]
            end_x, end_y = line["end"]
            svg_content += f'  <line x1="{start_x}" y1="{start_y}" x2="{end_x}" y2="{end_y}" style="stroke:black;stroke-width:2" />\n'

        # Agregar etiquetas de líneas al SVG
        for label, index in self.line_labels:
            coords = self.canvas.coords(label)
            if coords:  # Asegurarse de que las coordenadas se obtienen correctamente
                x, y = coords
                text = self.canvas.itemcget(label, "text")
                svg_content += f'  <text x="{x}" y="{y}" font-family="Arial" font-size="12" fill="black">{text}</text>\n'

        # Exportar etiquetas de leyenda
        for label in self.legend_labels:
            text, (x, y) = label
            angle = self.label_rotation.get(label, 0)
            font_size = self.label_font_size.get(label, 12)
            svg_content += f'  <text x="{x}" y="{y}" font-family="Arial" font-size="{font_size}" fill="blue" transform="rotate({angle},{x},{y})">{text}</text>\n'

        svg_content += '</svg>'

        # Escribir el contenido SVG en el archivo
        try:
            with open(file_path, "w") as svg_file:
                svg_file.write(svg_content)
            print(f"Archivo SVG guardado correctamente en {file_path}")
        except Exception as e:
            print(f"Error al guardar el archivo SVG: {e}")
    def execute_draw_line(self):
        if self.start_point is None:
            self.start_point = (50, self.current_y_offset + 50)
        else:
            length = self.length_var.get()
            self.start_point = self.drawing_canvas.draw_line(self.start_point, length)
            self.current_y_offset += 30
    def execute_clear_canvas(self):
        self.drawing_canvas.clear_canvas()
        self.current_y_offset = 0  # Opcional: Reiniciar el desplazamiento vertical si es necesario
        self.start_point = None  # Opcional: Reiniciar el punto de inicio
    def execute_export_to_svg(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG files", "*.svg")])
        if file_path:
            self.file_exporter.export_to_svg(self.drawing_canvas.lines, self.drawing_canvas.line_labels, self.label_manager.legend_labels, file_path)
    def execute_rotate_selected_label(self):
        self.label_manager.rotate_selected_label()
    def execute_increase_font_size(self):
        self.label_manager.increase_font_size()
    def execute_decrease_font_size(self):
        self.label_manager.decrease_font_size()
    def add_legend_label(self):
        text = self.legend_entry.get()
        if text:
            # Suponiendo una posición predeterminada, se puede ajustar según sea necesario
            x, y = 100, 100
            self.label_manager.add_legend_label(text, x, y)
    def rotate_selected_label(self):
        print("Rotate button pressed")  # Log para verificar la acción del botón
        self.label_manager.rotate_selected_label()
    def increase_font_size(self):
        self.label_manager.increase_font_size()
    def decrease_font_size(self):
        self.label_manager.decrease_font_size()

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()