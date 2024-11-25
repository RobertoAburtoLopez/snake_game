from serpiente import Serpiente
from juego import Juego

import subprocess

from colorama import Fore, Cursor, init

def main():
    init()
    h = 10
    w = 15

    subprocess.run("clear")
    serpiente = Serpiente(Fore.GREEN, 0, 0, println=3)
    juego = Juego(w, h, serpiente)
    juego.cicloJuego()
    print(f"{Cursor.POS(1, Juego.LINEA_BASE + h + 4)} FIN DEL JUEGO, NO HAY SALIDA")

if __name__ == '__main__':
    main()