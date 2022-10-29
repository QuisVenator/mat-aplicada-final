from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

class Regla:
    def __init__(self, humor, f_externos, v_precio, salida):
        self.humor = humor
        self.f_externos = f_externos
        self.v_precio = v_precio
        self.salida = salida
    
    def evaluar(self, pertenencias):
        val = min(pertenencias["humor"][self.humor], pertenencias["f_externos"][self.f_externos], pertenencias["v_precio"][self.v_precio])
        return (self.salida, val if val > 0 else None)

class FuzzySet:
    def __init__(self, min, c1, c2, max, val_extremo_neg=0, val_extremo_pos=0):
        self.min = min
        self.c1 = c1
        self.c2 = c2
        self.max = max
        self.val_extremo_neg = val_extremo_neg
        self.val_extremo_pos = val_extremo_pos
    
    def pertenencia(self, x):
        if x <= self.min:
            return self.val_extremo_neg
        elif x >= self.max:
            return self.val_extremo_pos
        elif x >= self.c1 and x <= self.c2:
            return 1
        elif x > self.min and x < self.c1:
            return (x - self.min) / (self.c1 - self.min)
        elif x > self.c2 and x < self.max:
            return (x - self.c2) / (self.max - self.c2) * -1 + 1
    
    def poligono(self, y):
        puntos = [(self.min if self.min != float('-inf') else self.start, 0)]
        puntos.append((y * (self.c1 - self.min) + self.min, y))
        puntos.append((y * (self.max - self.c2) + self.c2, y))
        puntos.append((self.max, 0) if self.min != float('inf') else self.stop)

        return Polygon(puntos)

def main():
    sets = {
        "humor": {
            "panico": FuzzySet(-1, -1, -0.8, -0.2, val_extremo_neg=1),
            "ansiedad": FuzzySet(-0.8, -0.2, 0, 0.01),
            "alegria": FuzzySet(-0.01, 0, 0.2, 0.8),
            "euforia": FuzzySet(0.3, 0.8, 1, 1, val_extremo_pos=1)
        },
        "f_externos": {
            "muy_negativo": FuzzySet(-1, -1, -0.8, -0.2, val_extremo_neg=1),
            "poco_negativo": FuzzySet(-0.8, -0.2, 0, 0.01),
            "poco_positivo": FuzzySet(-0.01, 0, 0.2, 0.8),
            "muy_positivo": FuzzySet(0.3, 0.8, 1, 1, val_extremo_pos=1)
        },
        "v_precio": {
            "muy_negativo": FuzzySet(-12, -12, -9, -1, val_extremo_neg=1),
            "poco_negativo": FuzzySet(-9, -2, 0, 0.01),
            "poco_positivo": FuzzySet(0.01, 0, 2, 9),
            "muy_positivo": FuzzySet(1, 9, 12, 12, val_extremo_pos=1)
        },
        "salida": {
            "pesimista": FuzzySet(-1, -1, -0.8, -0.2, val_extremo_neg=1),
            "poco_pesimista": FuzzySet(-0.8, -0.2, 0, 0.01),
            "poco_optimista": FuzzySet(-0.01, 0, 0.2, 0.8),
            "optimista": FuzzySet(0.3, 0.8, 1, 1, val_extremo_pos=1)
        }
    }

    reglas = [
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
        Regla("ansiedad", "muy_negativo", "poco_positivo", "poco_pesimista"),
        Regla("ansiedad", "muy_negativo", "muy_positivo", "poco_pesimista"),
        Regla("ansiedad", "poco_negativo", "muy_negativo", "pesimista"),
        Regla("ansiedad", "poco_negativo", "poco_negativo", "pesimista"),
        Regla("ansiedad", "poco_negativo", "poco_positivo", "poco_pesimista"),
        Regla("ansiedad", "poco_negativo", "muy_positivo", "poco_optimista"),
        Regla("ansiedad", "poco_positivo", "muy_negativo", "poco_pesimista"),
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
        Regla("alegria", "muy_negativo", "muy_positivo", "poco_optimista"),
        Regla("alegria", "poco_negativo", "muy_negativo", "pesimista"),
        Regla("alegria", "poco_negativo", "poco_negativo", "poco_pesimista"),
        Regla("alegria", "poco_negativo", "poco_positivo", "poco_optimista"),
        Regla("alegria", "poco_negativo", "muy_positivo", "poco_optimista"),
        Regla("alegria", "poco_positivo", "muy_negativo", "poco_optimista"),
        Regla("alegria", "poco_positivo", "poco_negativo", "poco_optimista"),
        Regla("alegria", "poco_positivo", "poco_positivo", "optimista"),
        Regla("alegria", "poco_positivo", "muy_positivo", "optimista"),
        Regla("alegria", "muy_positivo", "muy_negativo", "poco_optimista"),
        Regla("alegria", "muy_positivo", "poco_negativo", "poco_optimista"),
        Regla("alegria", "muy_positivo", "poco_positivo", "poco_optimista"),
        Regla("alegria", "muy_positivo", "muy_positivo", "optimista"),
        Regla("euforia", "muy_negativo", "muy_negativo", "poco_pesimista"),
        Regla("euforia", "muy_negativo", "poco_negativo", "poco_pesimista"),
        Regla("euforia", "muy_negativo", "poco_positivo", "poco_optimista"),
        Regla("euforia", "muy_negativo", "muy_positivo", "poco_optimista"),
        Regla("euforia", "poco_negativo", "muy_negativo", "poco_pesimista"),
        Regla("euforia", "poco_negativo", "poco_negativo", "poco_pesimista"),
        Regla("euforia", "poco_negativo", "poco_positivo", "poco_optimista"),
        Regla("euforia", "poco_negativo", "muy_positivo", "poco_optimista"),
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

    pertenencias = {
        "humor": {
            "panico": sets["humor"]["panico"].pertenencia(humor),
            "ansiedad": sets["humor"]["ansiedad"].pertenencia(humor),
            "alegria": sets["humor"]["alegria"].pertenencia(humor),
            "euforia": sets["humor"]["euforia"].pertenencia(humor),
        },
        "f_externos": {
            "muy_negativo": sets["f_externos"]["muy_negativo"].pertenencia(f_externos),
            "poco_negativo": sets["f_externos"]["poco_negativo"].pertenencia(f_externos),
            "poco_positivo": sets["f_externos"]["poco_positivo"].pertenencia(f_externos),
            "muy_positivo": sets["f_externos"]["muy_positivo"].pertenencia(f_externos),
        },
        "v_precio": {
            "muy_negativo": sets["v_precio"]["muy_negativo"].pertenencia(v_precio),
            "poco_negativo": sets["v_precio"]["poco_negativo"].pertenencia(v_precio),
            "poco_positivo": sets["v_precio"]["poco_positivo"].pertenencia(v_precio),
            "muy_positivo": sets["v_precio"]["muy_positivo"].pertenencia(v_precio),
        }
    }

    res = [regla.evaluar(pertenencias) for regla in reglas]
    res_poly = [sets["salida"][r[0]].poligono(r[1]) for r in res if r[1]]
    fuzzy_result = unary_union(res_poly)
    print(fuzzy_result)
    scalar_result = fuzzy_result.centroid.x
    print("Resultado: ", scalar_result)

if __name__ == "__main__":
    main()
