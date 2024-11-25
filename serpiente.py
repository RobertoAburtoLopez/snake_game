import copy

from colorama import Style, Cursor

class ObservadorObservable:
    def notificar(self):
        self.observador.actualizar()
        
    def actualizar(self):
        pass

    def agregarObservador(self, observador):
        self.observador = observador
        #print(f"[{self}]: Agregando observador {observador}.")

class Nodo(ObservadorObservable):
    CABEZA      = 'cabeza'
    CUERPO      = 'cuerpo'

    def __init__(self, rol, observado, idx) -> None:
        self.rol = rol
        self.x = 0
        self.y = 0
        self.idx = idx
        self.observador = None
        self.observado = observado
        self.observado.agregarObservador(self)
        #print(f"[{self}]: Nuevo nodo {rol=}.")

    def actualizar(self):
        if self.observador:
            self.observador.actualizar()

        self.x = self.observado.x
        self.y = self.observado.y
        #print(f"[{self}]: Moviento nodo {self.rol}.")

    def __str__(self) -> str:
        return f"Nodo[{self.idx}](x={self.x}, y={self.y})"

class Serpiente(ObservadorObservable):
    AVANZAR     = 1
    RETROCEDER  = -1

    maxX = 10
    maxY = 10

    def __init__(self, color, x, y, println) -> None:
        self.println = println
        self.x = x
        self.y = y
        self.color = color
        self.nodos = list()
        self.cabeza = f"Nodo({x=}, {y=})"
        self.cabeza = Nodo(Nodo.CABEZA, self, 0)
        self.nodos.append(self.cabeza)
        self.muerto = False
        print(f"[{self}]: Nueva serpiente.")

    def moverX(self, avanza) -> bool:
        if(
            (avanza and self.x >= self.maxX) or
            (not avanza and self.x <= 0)
        ):
            return False

        self.x += Serpiente.AVANZAR if avanza else Serpiente.RETROCEDER
        self.notificar()
        print(f"{Cursor.POS(1, self.println)}[{self}]: Moviento serpiente en X.")
        return True

    def moverY(self, avanza) -> bool:
        if(
            (avanza and self.y >= self.maxY) or
            (not avanza and self.y <= 0)
        ):
            return False

        self.y += Serpiente.AVANZAR if avanza else Serpiente.RETROCEDER
        self.notificar()
        print(f"{Cursor.POS(1, self.println)}[{self}]: Moviento serpiente en Y.")
        return True

    def agrandar(self) -> None:
        self.nodos.append(Nodo(Nodo.CUERPO, self.nodos[-1], len(self.nodos)))
        self.notificar()
        print(f"{Cursor.POS(1, self.println)}[{self}]: Agrandando serpiente.")

    def obtenerCuerpo(self) -> list:
        return copy.deepcopy(self.nodos)

    def __str__(self) -> str:
        return f"{self.color}Serpiente({self.cabeza}, tamano={len(self.nodos)}){Style.RESET_ALL}"