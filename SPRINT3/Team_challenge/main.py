from variables import dimensiones_tablero, barcos, cantidad_barcos, simbolo_agua, simbolo_barco, simbolo_tocado, simbolo_disparo_agua 
from tablero import Tablero
import numpy as np

#JUEGO

def jugar():
    jugador = Tablero(input("Nombre de jugador:"))
    maquina = Tablero("Máquina")

    print("¡Bienvenido a la Batalla Naval!")
    jugador.mostrar_tablero()
    jugador.colocar_barcos_usuario()  # Para pruebas, colocar barcos automáticamente
    maquina.colocar_barcos_maquina()
    
    print("Ambos jugadores tienen los barcos colocados.")
    
    turno_jugador = True
    while True:
        if turno_jugador:
            print("Tu turno")
            jugador.disparos_usuario()
            jugador.mostrar_tablero()

        else:
            print("Turno de la máquina")
            maquina.disparos_maquina()
            maquina.mostrar_tablero_maquina()

        
        # Verificar si alguien ha ganado
        if np.count(jugador.tablero == simbolo_tocado) == 20:
            print("¡La máquina gana!")
            break
        elif np.count_nonzero(maquina.tablero == simbolo_tocado) == 20:
            print("¡Felicidades, has ganado!")
            break
        
        turno_jugador = not turno_jugador  # Cambiar de turno
