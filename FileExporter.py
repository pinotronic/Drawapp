from tkinter import filedialog
class FileExporter:
    def __init__(self, canvas):
        self.canvas = canvas
    def export_to_svg(self):
        # Abrir un cuadro de diálogo para guardar el archivo
        file_path = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG files", "*.svg")])
        if not file_path:
            return

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
