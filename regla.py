class Regla:
    def __init__(self, humor, f_externos, v_precio, salida):
        self.humor = humor
        self.f_externos = f_externos
        self.v_precio = v_precio
        self.salida = salida
    
    def disparo(self, pertenencias):
        return (self.salida, min(pertenencias[self.humor], pertenencias[self.f_externos], pertenencias[self.v_precio]))

class FuzzySet:
    def __init__(self, nombre, min, c1, c2, max):
        self.nombre = nombre
        self.min = min
        self.c1 = c1
        self.c2 = c2
        self.max = max
    
    def pertenencia(self, x):
        if x <= self.min or x >= self.max:
            return 0
        elif x >= self.c1 and x <= self.c2:
            return 1
        elif x > self.min and x < self.c1:
            return (x - self.min) / (self.c1 - self.min)
        elif x > self.c2 and x < self.max:
            return (x - self.c2) / (self.max - self.c2) * -1 + 1

# main function
def main():
    sets = {
        "humor": [
            FuzzySet("panico", float('-inf'), float('-inf'), -0.8, -0.2),
            FuzzySet("ansiedad", -0.8, -0.2, 0, 0.01),
            FuzzySet("alegria", -0.01, 0, 0.2, 0.8),
            FuzzySet("euforia", 0.3, 0.8, float('inf'), float('inf'))
        ],
        "f_externos": [
            FuzzySet("muy_negativo", float('-inf'), float('-inf'), -0.8, -0.2),
            FuzzySet("poco_negativo", -0.8, -0.2, 0, 0.01),
            FuzzySet("poco_positivo", -0.01, 0, 0.2, 0.8),
            FuzzySet("muy_positivo", 0.3, 0.8, float('inf'), float('inf'))
        ],
        "v_precio": [
            FuzzySet("muy_negativo", float('-inf'), float('-inf'), -9, -1),
            FuzzySet("poco_negativo", -9, -2, 0, 0.01),
            FuzzySet("poco_positivo", 0.01, 0, 2, 9),
            FuzzySet("muy_positivo", 1, 9, float('inf'), float('inf'))
        ],
        "salida": [
            FuzzySet("pesimista", float('-inf'), float('-inf'), -0.8, -0.2),
            FuzzySet("poco_pesimista", -0.8, -0.2, 0, 0.01),
            FuzzySet("poco_optimista", -0.01, 0, 0.2, 0.8),
            FuzzySet("optimista", 0.3, 0.8, float('inf'), float('inf'))
        ]
    }

    reglas = [
        # Regla(humor, f_externos, v_precio, salida)
        Regla("panico", "muy_negativo", "muy_negativo", "pesimista"),
        Regla("panico", "muy_negativo", "poco_negativo", "pesimista"),
        Regla("panico", "muy_negativo", "poco_positivo", "poco_pesimista"),
        Regla("panico", "muy_negativo", "muy_positivo", "poco_pesimista"),
        Regla("panico", "poco_negativo", "muy_negativo", "pesimista"),
        Regla("panico", "poco_negativo", "poco_negativo", "pesimista"),
        Regla("panico", "poco_negativo", "poco_positivo", "poco_pesimista"),
        Regla("panico", "poco_negativo", "muy_positivo", "poco_pesimista"),
        Regla("panico", "poco_positivo", "muy_negativo", "poco_pesimista"),
        Regla("panico", "poco_positivo", "poco_negativo", "poco_pesimista"),
        Regla("panico", "poco_positivo", "poco_positivo", "poco_optimista"),
        Regla("panico", "poco_positivo", "muy_positivo", "poco_optimista"),
        Regla("panico", "muy_positivo", "muy_negativo", "poco_pesimista"),
        Regla("panico", "muy_positivo", "poco_negativo", "poco_pesimista"),
        Regla("panico", "muy_positivo", "poco_positivo", "poco_optimista"),
        Regla("panico", "muy_positivo", "muy_positivo", "poco_optimista"),
        Regla("ansiedad", "muy_negativo", "muy_negativo", "pesimista"),
        Regla("ansiedad", "muy_negativo", "poco_negativo", "pesimista"),
        Regla("ansiedad", "muy_negativo", "poco_positivo", "pesimista"),
        Regla("ansiedad", "muy_negativo", "muy_positivo", "poco_pesimista"),
        Regla("ansiedad", "poco_negativo", "muy_negativo", "pesimista"),
        Regla("ansiedad", "poco_negativo", "poco_negativo", "pesimista"),
        Regla("ansiedad", "poco_negativo", "poco_positivo", "poco_pesimista"),
        Regla("ansiedad", "poco_negativo", "muy_positivo", "poco_optimista"),
        Regla("ansiedad", "poco_positivo", "muy_negativo", "pesimista"),
        Regla("ansiedad", "poco_positivo", "poco_negativo", "poco_pesimista"),
        Regla("ansiedad", "poco_positivo", "poco_positivo", "poco_optimista"),
        Regla("ansiedad", "poco_positivo", "muy_positivo", "poco_optimista"),
        Regla("ansiedad", "muy_positivo", "muy_negativo", "poco_pesimista"),
        Regla("ansiedad", "muy_positivo", "poco_negativo", "poco_pesimista"),
        Regla("ansiedad", "muy_positivo", "poco_positivo", "poco_optimista"),
        Regla("ansiedad", "muy_positivo", "muy_positivo", "poco_optimista"),
        Regla("alegria", "muy_negativo", "muy_negativo", "pesimista"),
        Regla("alegria", "muy_negativo", "poco_negativo", "poco_pesimista"),
        Regla("alegria", "muy_negativo", "poco_positivo", "poco_pesimista"),
        Regla("alegria", "muy_negativo", "muy_positivo", "poco_positivo"),
        Regla("alegria", "poco_negativo", "muy_negativo", "pesimista"),
        Regla("alegria", "poco_negativo", "poco_negativo", "poco_pesimista"),
        Regla("alegria", "poco_negativo", "poco_positivo", "poco_optimista"),
        Regla("alegria", "poco_negativo", "muy_positivo", "optimista"),
        Regla("alegria", "poco_positivo", "muy_negativo", "poco_optimista"),
        Regla("alegria", "poco_positivo", "poco_negativo", "optimista"),
        Regla("alegria", "poco_positivo", "poco_positivo", "optimista"),
        Regla("alegria", "poco_positivo", "muy_positivo", "optimista"),
        Regla("alegria", "muy_positivo", "muy_negativo", "poco_optimista"),
        Regla("alegria", "muy_positivo", "poco_negativo", "optimista"),
        Regla("alegria", "muy_positivo", "poco_positivo", "poco_optimista"),
        Regla("alegria", "muy_positivo", "muy_positivo", "optimista"),
        Regla("euforia", "muy_negativo", "muy_negativo", "poco_pesimista"),
        Regla("euforia", "muy_negativo", "poco_negativo", "poco_pesimista"),
        Regla("euforia", "muy_negativo", "poco_positivo", "poco_optimista"),
        Regla("euforia", "muy_negativo", "muy_positivo", "poco_optimista"),
        Regla("euforia", "poco_negativo", "muy_negativo", "poco_pesimista"),
        Regla("euforia", "poco_negativo", "poco_negativo", "poco_pesimista"),
        Regla("euforia", "poco_negativo", "poco_positivo", "poco_optimista"),
        Regla("euforia", "poco_negativo", "muy_positivo", "poco_pesimista"),
        Regla("euforia", "poco_positivo", "muy_negativo", "poco_optimista"),
        Regla("euforia", "poco_positivo", "poco_negativo", "poco_optimista"),
        Regla("euforia", "poco_positivo", "poco_positivo", "optimista"),
        Regla("euforia", "poco_positivo", "muy_positivo", "optimista"),
        Regla("euforia", "muy_positivo", "muy_negativo", "poco_optimista"),
        Regla("euforia", "muy_positivo", "poco_negativo", "poco_optimista"),
        Regla("euforia", "muy_positivo", "poco_positivo", "optimista"),
        Regla("euforia", "muy_positivo", "muy_positivo", "optimista"),
    ]

    v_precio = float(input("V. precio: "))
    humor = float(input("Humor: "))
    f_externos = float(input("F. externos: "))

if __name__ == "__main__":
    main()
