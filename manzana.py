import random

class Manzana:
    def __init__(self, nodos: list, w, h) -> None:
        if(len(nodos) == 0):
            self.x = random.randint(0, w)
            self.y = random.randint(0, h)
            if(self.x == 0 and self.y == 0):
                self.x = 1
            pass
        
        xy = set([(n.x, n.y) for n in nodos])
        self.x = random.randint(0, w)
        self.y = random.randint(0, h)
        while (self.x, self.y) in xy:
            self.x = random.randint(0, w)
            self.y = random.randint(0, h)
    
    def __str__(self) -> str:
        return f"Manzana(x={self.x}, y={self.y})"