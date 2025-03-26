import random
import textwrap
import numpy as np
from colorama import Fore,Style
from variables import dim_tablero, simbolo_barco


def menu_principal():

    """
    Despliega un menú principal sencillo que se muestra al ejecutar el módulo principal
    """

    while True:

        print("\n--- HUNDIR LA FLOTA ---")
        print("1. Jugar")
        print("2. Información")
        print("3. Salir del juego")

        opcion = input("Elige una opción: ")  #Novedad .strip() para eliminar espacios involuntarios al principio y/o final de la cadena que se recibe con el input
        
        if opcion == "1":
            dificultad = seleccionar_dificultad()
            return dificultad
        elif opcion == "2":
            texto = """\
            Esto es una simplificación del clásico hundir la flota.
            Jugarás contra la máquina y el objetivo es hundir todos sus barcos antes de que hunda los tuyos.
            En cada turno podrás darme las coordenadas donde quieras disparar y también comprobar cuáles han sido tus disparos.
            Si aciertas, sigues disparando, si no, le tocará a la máquina. Puedes salir del juego en cualquier momento.
            ¡SUERTE!
            """
            print(textwrap.dedent(texto))  #Novedad .dedent de textwrap para que el texto quede cuadrado en la terminal. No cambia nada es solo para embellecer el formateo
        elif opcion == "3":
            print("Saliendo del juego...")
            exit()
        else:
            print("Opción no válida. Inténtalo de nuevo.")


#Novedad, selector de dificultades
def seleccionar_dificultad():

    """
    Permite seleccionar la dificultad del juego.
    Internamente según si el usuario escoge fácil intermedio o difícil la máquina hará 3*(1, 2 o 3) turnos en lo que sería su turno normal.
    """

    while True:
        print("\nSelecciona la dificultad:")
        print("1. Fácil")
        print("2. Intermedio")
        print("3. Difícil")

        opcion = input("Elige una opción: ").strip()
        if opcion == "1":
            return 1
        elif opcion == "2":
            return 2
        elif opcion == "3":
            return 3
        else:
            print("Opción no válida. Inténtalo de nuevo.")


def turno_jugador(tablero_jugador, tablero_maquina):

    """
    Desarrolla el turno del jugador, desplegando un menú con 4 opciones diferentes
    """

    print("\nTu turno. Opciones:")
    print("1. Disparar")
    print("2. Mostrar tablero de disparos")
    print("3. Mostrar mi tablero")
    print("4. Salir del juego")
    
    opcion = input("Elige una opción: ").strip()  #Novedad .strip() para eliminar espacios involuntarios al principio y/o final de la cadena que se recibe con el input

    if opcion == "1":
        while True:  #Novedad para hacerlo más robusto (evita entradas inesperadas del usuario)
            try:
                x = int(input("Introduce la fila (0-9): ").strip())
                y = int(input("Introduce la columna (0-9): ").strip())
                
                if 0 <= x < dim_tablero and 0 <= y < dim_tablero:
                    break
                else:
                    print("Las coordenadas deben estar entre 0 y 9. Inténtalo de nuevo.")
            except ValueError:
                print("Entrada no válida. Introduce solo números entre 0 y 9.")

        if tablero_jugador.disparar_usuario(tablero_maquina, x, y):
            #O mantenemos turno por acertar o hemos ganado (por dar al ultimo barco)
            if not np.any(tablero_maquina.matriz == simbolo_barco):
                print(Fore.GREEN + "\n¡Has hundido todos los barcos de la máquina! ¡Felicidades!\n" + Style.RESET_ALL)
                exit()
            return True  #Mantiene turno si acierta
        else:
            return False  #Cambia turno si falla

    elif opcion == "2":
        print("\nEstos son los disparos que has hecho hasta ahora: \n")
        tablero_maquina.mostrar_disparos()

    elif opcion == "3":
        print("\nTu tablero actual: \n")
        tablero_jugador.mostrar(tablero_jugador)  #Para ver cómo va la máquina

    elif opcion == "4":
        print("Saliendo del juego...")
        exit()

    else:
        print("Opción no válida. Inténtalo de nuevo.")

    return True  #Mantenemos turno si no se disparó (por ejemplo, si hemos elegido mostrar uno de los tableros)


def turno_maquina(tablero_maquina, tablero_jugador, registro_disparos_maquina, dificultad_maquina):

    """
    Función más sencilla que desarrolla el turno de la máquina, que es aleatorio, internamente.
    No permite que la máquina repita disparo y muestra solo si nos ha impactado o no.
    Novedad: implementa el selector de dificultad.
    """

    print("\nTurno de la máquina.")

    #Novedad, multiplicamos por tres los turnos internos, dificultad 1, facil, tres turnos, 2 intermedia 6...
    #Hacemos esto porque nosotros seguimos una lógica, si impactamos seguimos disparando en horizontal o vertical
    #a esa coordenada buscando barcos, la máquina es siempre aleatoria, así que para hacerlo algo complicado lo tenemos
    #que implementar así.

    turnos_restantes = dificultad_maquina * 3

    while turnos_restantes > 0:
        while True:
            x = random.randint(0, dim_tablero - 1)
            y = random.randint(0, dim_tablero - 1)
            if (x, y) not in registro_disparos_maquina:
                break

        registro_disparos_maquina.add((x, y))  #Guardamos el disparo de la máquina en el set para no repetirlo
        acierto = tablero_maquina.disparar_maquina(tablero_jugador, x, y)

        if acierto:
            print(Fore.RED + "¡La máquina te ha dado!\n" + Style.RESET_ALL)

            #¡¡COMPROBACIÓN DE FIN DE PARTIDA AQUÍ!! Sino no acaba nunca
            if not np.any(tablero_jugador.matriz == simbolo_barco):
                print(Fore.RED + "\n¡La máquina ha hundido todos tus barcos! GAME OVER\n" + Style.RESET_ALL)
                exit()
        else:
            turnos_restantes -= 1  #Si falla, descuenta un turno interno

    print("Tu turno.\n")  #Solo se muestra esto cuando la máquina termina su turno global (el que ve el usuario digamos)
    return True  #Cuando ha llegado hasta aqui se acaban todos los turnos internos, devolvemos False y ya le toca al usuario

