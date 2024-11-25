from serpiente import Serpiente
from manzana import Manzana
from bot import Bot

from colorama import Style, Cursor, Fore

import time
import sys  # Para terminar la ejecución del programa

class Juego:
    LINEA_BASE = 7
    def __init__(self, w, h, serpiente: Serpiente) -> None:
        self.w = w
        self.h = h
        self.serpiente = serpiente
        self.serpiente.maxX = w
        self.serpiente.maxY = h
        self.anterior = list()
        self.manzana = Manzana(self.anterior, self.w, self.h)
        self.bot = Bot(self.serpiente, self.manzana, self.w, self.h)
        print(f"[{self}] Nuevo juego iniciado.")

    def dibujarTablero(self):
        for i in range(self.h + 3):
            print(f"{Cursor.POS(1, Juego.LINEA_BASE + i)} *", end='')
            for _ in range(self.w + 1):
                print(f"{"**" if(i == 0 or i == self.h + 2) else "  "}", end='')
            print("*")
    
    def dibujarManzana(self):
        print(f"{Cursor.POS((self.manzana.x * 2) + 3, Juego.LINEA_BASE + self.manzana.y + 1)}{Fore.RED}(){Style.RESET_ALL}")
        print(f"{Cursor.POS(1, 4)}{self.manzana}                            ")

    def dibujarSerpiente(self):
        nodos = self.serpiente.obtenerCuerpo()
        
        # Limpiar la posición anterior del último nodo (cola)
        if len(self.anterior) > 0:
            print(f"{Cursor.POS((self.anterior[-1].x * 2) + 3, Juego.LINEA_BASE + self.anterior[-1].y + 1)}  ")
        
        # Dibujar el cuerpo de la serpiente (sin cabeza ni cola)
        for nodo in nodos[1:-1]:
            print(f"{Cursor.POS((nodo.x * 2) + 3, Juego.LINEA_BASE + nodo.y + 1)}{self.serpiente.color}[]{Style.RESET_ALL}")
        
        # Dibujar la cabeza en amarillo
        if len(nodos) > 0:
            print(f"{Cursor.POS((nodos[0].x * 2) + 3, Juego.LINEA_BASE + nodos[0].y + 1)}{Fore.YELLOW}[]{Style.RESET_ALL}")
        
        # Dibujar la cola en rojo
        if len(nodos) > 1:
            print(f"{Cursor.POS((nodos[-1].x * 2) + 3, Juego.LINEA_BASE + nodos[-1].y + 1)}{Fore.RED}[]{Style.RESET_ALL}")
        
        # Actualizar las posiciones previas
        self.anterior = nodos


    def consumirManzana(self):
        print(f"{Cursor.POS(1, 6)}Consumiento manzana {self.manzana}")
        self.serpiente.agrandar()
        self.manzana = Manzana(self.anterior, self.w, self.h)
        self.bot.cambiarObjetivo(self.manzana)

    def revisarColision(self):
        cabeza = self.serpiente.cabeza
        if cabeza.x == self.manzana.x and cabeza.y == self.manzana.y:
            self.consumirManzana()

    def cicloJuego(self):
        self.dibujarTablero()
        self.dibujarSerpiente()
        self.dibujarManzana()
        while not self.serpiente.muerto:
            time.sleep(0.2)
            paso = self.bot.consumirPaso()
            if paso is None:
                print(f"{Cursor.POS(1, Juego.LINEA_BASE + self.h + 5)}{Fore.RED}YA NO HAY CAMINO POSIBLE{Style.RESET_ALL}")
                sys.exit(0)  # Termina la ejecución del programa
            if paso[0] == 'x':
                self.serpiente.moverX(paso[1])
            else:
                self.serpiente.moverY(paso[1])
            self.dibujarManzana()
            self.dibujarSerpiente()
            self.revisarColision()
            print(f"{Cursor.POS(1, 5)}{self.serpiente.cabeza} {self.manzana}")
        self.dibujarManzana()
        self.dibujarSerpiente()

    def __str__(self) -> str:
        return f"Juego(w={self.w}, h={self.h})"
