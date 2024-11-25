from serpiente import Serpiente
from manzana import Manzana

from heapq import heappop, heappush
from copy import deepcopy


class Bot:
    def __init__(self, serpiente: Serpiente, objetivo: Manzana, w, h) -> None:
        self.s = serpiente
        self.o = objetivo
        self.w = w
        self.h = h
        self.buscarRutaMasCorta()

    def cambiarObjetivo(self, objetivo: Manzana):
        print(f"NUEVO OBJETIVO {objetivo}")
        self.o = objetivo
        self.buscarRutaMasCorta()

    def consumirPaso(self):
        if len(self.camino) == 0:
            return None
        return self.camino.pop(0)

    def buscarRutaMasCorta(self):
        nodos = self.s.obtenerCuerpo()
        cuerpo = [(n.x, n.y) for n in nodos]
        x, y = self.s.x, self.s.y
        destino = (self.o.x, self.o.y)

        # Llama al método A*
        self.camino = self.siguientePasoAStar((x, y), destino, cuerpo)

        # Si no encuentra camino, intenta liberar espacio
        if not self.camino or not self.simularFuturo((x, y), cuerpo):
            print("Espacio futuro insuficiente. Evaluando espacio libre...")
            self.camino = self.explorarEspacioLibre((x, y), cuerpo)

        if not self.camino:
            self.s.muerto = True

    directions = [(-1, 0, ('x', False)), (1, 0, ('x', True)), (0, -1, ('y', False)), (0, 1, ('y', True))]

    def siguientePasoAStar(self, inicio, destino, cuerpo):
        cola = []
        heappush(cola, (0, 0, inicio, [], cuerpo[:]))

        visitados = set()
        visitados.add(inicio)

        while cola:
            f, g, (cx, cy), camino, cuerpo_actual = heappop(cola)

            if (cx, cy) == destino:
                return camino

            for dx, dy, direccion in self.directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx <= self.w and 0 <= ny <= self.h:
                    nueva_posicion = (nx, ny)
                    if nueva_posicion not in cuerpo_actual and nueva_posicion not in visitados:
                        cuerpo_predicho = cuerpo_actual[:]
                        cuerpo_predicho.insert(0, nueva_posicion)
                        cuerpo_predicho.pop()

                        h = abs(nx - destino[0]) + abs(ny - destino[1])
                        espacio_libre = self.calcularEspacioLibre(nueva_posicion, cuerpo_predicho)
                        penalizacion = 1 / (espacio_libre + 1)
                        nuevo_g = g + 1
                        nuevo_f = nuevo_g + h + penalizacion

                        heappush(cola, (nuevo_f, nuevo_g, nueva_posicion, camino + [direccion], cuerpo_predicho))
                        visitados.add(nueva_posicion)

        return None

    def explorarEspacioLibre(self, inicio, cuerpo):
        cola = []
        heappush(cola, (0, inicio, []))

        visitados = set()
        visitados.add(inicio)

        while cola:
            _, (cx, cy), camino = heappop(cola)

            for dx, dy, direccion in self.directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx <= self.w and 0 <= ny <= self.h:
                    nueva_posicion = (nx, ny)
                    if nueva_posicion not in cuerpo and nueva_posicion not in visitados:
                        visitados.add(nueva_posicion)
                        heappush(cola, (len(camino) + 1, nueva_posicion, camino + [direccion]))

        return camino

    def calcularEspacioLibre(self, posicion, cuerpo):
        cola = [posicion]
        visitados = set()
        visitados.add(posicion)
        espacio_libre = 0

        while cola:
            cx, cy = cola.pop(0)
            espacio_libre += 1

            for dx, dy, _ in self.directions:
                nx, ny = cx + dx, cy + dy
                nueva_posicion = (nx, ny)
                if 0 <= nx <= self.w and 0 <= ny <= self.h and nueva_posicion not in cuerpo and nueva_posicion not in visitados:
                    visitados.add(nueva_posicion)
                    cola.append(nueva_posicion)

        return espacio_libre

    def simularFuturo(self, posicion, cuerpo):
        """
        Simula si existe un camino seguro para el cuerpo de la serpiente
        considerando varias iteraciones en el futuro.
        """
        simulacion_cuerpo = deepcopy(cuerpo)
        simulacion_posicion = posicion

        for _ in range(5):  # Profundidad de simulación
            espacio_libre = self.calcularEspacioLibre(simulacion_posicion, simulacion_cuerpo)
            if espacio_libre == 0:
                return False

            for dx, dy, _ in self.directions:
                nx, ny = simulacion_posicion[0] + dx, simulacion_posicion[1] + dy
                nueva_posicion = (nx, ny)
                if 0 <= nx <= self.w and 0 <= ny <= self.h and nueva_posicion not in simulacion_cuerpo:
                    simulacion_cuerpo.insert(0, nueva_posicion)
                    simulacion_cuerpo.pop()
                    simulacion_posicion = nueva_posicion
                    break
        return True
