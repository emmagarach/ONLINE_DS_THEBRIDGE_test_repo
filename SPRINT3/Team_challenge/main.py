from colorama import Fore
import numpy as np
import random
import textwrap 
from tablero import Tablero
from variables import dim_tablero, barcos, simbolo_agua, simbolo_barco, simbolo_tocado, simbolo_agua_disparada


#FUNCIONES JUEGO
#funciones juego
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


#Novedad, selector de dificultades (la máquina hace 1,2 o 3 turnos dentro de su turno)
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

        if not tablero_jugador.disparar_usuario(tablero_maquina, x, y):
            return False  #Cambiamos el turno si fallamos

    elif opcion == "2":
        print("\nEstos son los disparos que has hecho hasta ahora: \n")
        tablero_maquina.mostrar_disparos()

    elif opcion == "3":
        print("\nTu tablero actual: \n")
        tablero_jugador.mostrar()  #Para ver cómo va la máquina

    elif opcion == "4":
        print("Saliendo del juego...")
        exit()

    else:
        print("Opción no válida. Inténtalo de nuevo.")

    return True  #Mantenemos turno si no se disparó (por ejemplo, si hemos elegido mostrar uno de los tableros)


def turno_maquina(tablero_jugador, tablero_maquina, registro_disparos_maquina, dificultad_maquina):

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

        acierto = tablero_maquina.disparar_maquina(tablero_jugador, (x, y))

        if acierto:
            print("¡La máquina te ha dado!\n")
        else:
            turnos_restantes -= 1  #Si falla, descuenta un turno interno

    print("Tu turno.\n")  #Solo se muestra esto cuando la máquina termina su turno global (el que ve el usuario digamos)
    return True  #Cuando ha llegado hasta aqui se acaban todos los turnos internos, devolvemos False y ya le toca al usuario

#JUEGO
def jugar(dificultad_maquina):

    """
    Desarrollo completo del juego con los módulos ya creados
    """

    #Set vacío al que iremos añadiendo los disparos de la máquina para que no los repita (pues se generan aleatorios, podría pasar)
    registro_disparos_maquina = set() 

    #Inicializamos los tableros con los barcos para el usuario y para la máquina
    nombre_usuario = input("Introduce tu nombre: ")

    # Crear los tableros
    tablero_jugador = Tablero(nombre_usuario)
    tablero_maquina = Tablero("Máquina")

    print("¡Bienvenido a la Batalla Naval!")

    tablero_jugador.mostrar()
    tablero_jugador.generar_barcos_aleatorios()  # Para pruebas, colocar barcos automáticamente
    tablero_maquina.generar_barcos_aleatorios()
    
    print("Ambos jugadores tienen los barcos colocados.")
    
    turno = True  #Comienza el usuario

    while True:

        #Aquí gestionamos los cambios de turno con el booleano que devuelven turno_jugador y turno_maquina(véanse las funciones en el módulo correspondiente)
        if turno:
            turno = turno_jugador(tablero_jugador, tablero_maquina)
        else:
            turno = turno_maquina(tablero_jugador, registro_disparos_maquina, dificultad_maquina)


        #Verificamos si alguien ganó
        if not np.any(tablero_jugador == simbolo_barco):  #Si no quedan barcos en el tablero del jugador la máquina ha ganado
            print(Fore.RED + "\n¡La máquina ha hundido todos tus barcos! GAME OVER\n")
            break
        if not np.any(tablero_maquina == simbolo_barco):  #Si no quedan barcos en el tablero de la máquina el jugador ha ganado
            print(Fore.GREEN + "\n¡Has hundido todos los barcos de la máquina! ¡Felicidades!\n")
            break


#Este bloque asegura que el juego solo se ejecute si este script se ejecuta directamente
#y no si se importa como un módulo en otro archivo (se incluye para hacer todo más robusto)
if __name__ == "__main__":
    dificultad = menu_principal()  #Recogemos la dificultad elegida
    if dificultad: #Si se ha recogido un valor dificultad si o si es 1,2 o 3, que siempre devuelve True
        jugar(dificultad)  #Se pasa la dificultad a jugar()


