import json

class SurfaceAreaCalculator:
    def __init__(self, json_data):
        """
        Inicializa la clase con el JSON que contiene las coordenadas.
        """
        self.points = self.parse_json(json_data)
    
    def parse_json(self, json_data):
        """
        Parsea el JSON y extrae los puntos de anclaje.
        """
        data = json.loads(json_data)
        return [(point['x'], point['y']) for point in data['points']]
    
    def calculate_area(self):
        """
        Calcula el área usando la fórmula del 'shoelace'.
        """
        n = len(self.points)
        area = 0.0
        
        for i in range(n):
            x1, y1 = self.points[i]
            x2, y2 = self.points[(i + 1) % n]  # Siguiente punto, con wrap-around al inicio
            
            area += x1 * y2
            area -= y1 * x2
        
        area = abs(area) / 2.0
        return area

# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo de un JSON con puntos
    # json_data = '''
    # {
    #     "points": [
    #         {"x": 0, "y": 0},
    #         {"x": 4, "y": 0},
    #         {"x": 4, "y": 3},
    #         {"x": 0, "y": 3}
    #     ]
    # }
    # '''
    
    # calculator = SurfaceAreaCalculator(json_data)
    # area = calculator.calculate_area()
    
    print(f"Área de la superficie: {area}")
